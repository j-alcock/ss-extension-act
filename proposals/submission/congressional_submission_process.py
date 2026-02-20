"""
Congressional Submission Process — Social Security Extension Act
Automated and manual submission workflow for all 535 members of Congress.

SUBMISSION CHANNELS (ranked by effectiveness):

  HOUSE OF REPRESENTATIVES (435 members):
    1. CWC API (Communicating with Congress) — Bulk XML delivery
       - Vendor registration: CWCVendors@mail.house.gov
       - Requires: signed application, whitelisted IPs, XML schema compliance
       - Ref: house.gov/doing-business-with-the-house/communicating-with-congress-cwc
       - Delivers to House Constituent Service Systems directly
    2. Web contact forms — Browser automation via headless Chrome
       - Uses unitedstates/contact-congress YAML form specs
       - Ref: github.com/unitedstates/contact-congress
    3. USPS mail — Physical letters to DC offices
       - Most reliable for non-constituent policy proposals
       - Allow 2-4 weeks for security screening

  SENATE (100 members):
    1. SCWC / SOAPBox API — Standardized vendor delivery
       - Registration: soapbox.senate.gov/registration/
       - Delivers to Senate Constituent Service Systems (CSS)
       - Mandatory + optional fields, XML format
       - Ref: senate.gov/senators/scwc.htm
    2. Web contact forms — Browser automation via headless Chrome
       - Senate forms use dynamic JS (Forms_Builder.js)
       - Most have reCAPTCHA (requires manual solving or service)
    3. USPS mail — Physical letters to DC offices

EXISTING TOOLS:
  - democracy.io — Single interface for all 3 reps (2 senators + 1 rep)
  - github.com/EFForg/congress_forms — Ruby gem, Chrome headless
  - github.com/unitedstates/contact-congress — YAML form definitions
  - Phantom of the Capitol — Original form-filler (now uses CWC for House)

ARCHITECTURE:
  1. MessageGenerator — Creates personalized messages per member from templates
  2. SubmissionEngine — Multi-channel delivery (CWC/SCWC/web form/USPS)
  3. BatchOrchestrator — Manages 535 submissions with rate limiting
  4. StatusTracker — Logs results, schedules follow-ups
"""

import os
import json
import csv
import hashlib
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import Enum
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════
#  CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

# Sender information (MUST be filled in before running)
SENDER_CONFIG = {
    'prefix': 'Mr.',           # Mr., Mrs., Ms., Dr., etc.
    'first_name': '',          # REQUIRED
    'last_name': '',           # REQUIRED
    'email': '',               # REQUIRED
    'phone': '',               # REQUIRED for some forms
    'address_line_1': '',      # REQUIRED — street address
    'address_line_2': '',      # Optional — apt/suite
    'city': '',                # REQUIRED
    'state': '',               # REQUIRED — 2-letter abbreviation
    'zip_code': '',            # REQUIRED — 5-digit
    'zip_plus_4': '',          # Optional — 4-digit extension
    'organization': 'Independent Policy Research',  # For CWC campaign field
}

# Rate limiting to avoid being flagged
RATE_LIMITS = {
    'web_forms_per_hour': 10,           # Conservative for web form submissions
    'cwc_messages_per_batch': 50,       # CWC API batch size
    'scwc_messages_per_batch': 50,      # SCWC API batch size
    'delay_between_web_forms_sec': 360, # 6 minutes between web form submissions
    'delay_between_api_calls_sec': 2,   # 2 seconds between API messages
}

# Submission tracking database path
TRACKER_DB_PATH = Path(__file__).parent / 'submission_tracker.json'

# Output directory for generated letters
LETTERS_OUTPUT_DIR = Path(__file__).parent / 'generated_letters'


# ═══════════════════════════════════════════════════════════════════════
#  ENUMS AND DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════

class Chamber(Enum):
    SENATE = 'senate'
    HOUSE = 'house'

class SubmissionChannel(Enum):
    CWC_API = 'cwc_api'           # House CWC XML API
    SCWC_API = 'scwc_api'         # Senate SOAPBox API
    WEB_FORM = 'web_form'         # Browser automation
    USPS_MAIL = 'usps_mail'       # Physical letter
    DEMOCRACY_IO = 'democracy_io' # democracy.io interface
    MANUAL = 'manual'             # Manual submission by human

class SubmissionStatus(Enum):
    PENDING = 'pending'
    QUEUED = 'queued'
    SUBMITTED = 'submitted'
    CONFIRMED = 'confirmed'       # Got auto-reply or confirmation
    FAILED = 'failed'
    RETRY = 'retry'
    SKIPPED = 'skipped'           # Non-constituent, form blocked, etc.

class Stance(Enum):
    RECEPTIVE = 'RECEPTIVE'
    SKEPTICAL = 'SKEPTICAL'
    HOSTILE = 'HOSTILE'

class TopicCategory(Enum):
    """Common topic/subject categories found on congressional contact forms."""
    SOCIAL_SECURITY = 'Social Security'
    TAXES = 'Taxes'
    BUDGET = 'Budget/Spending'
    ECONOMY = 'Economy/Jobs'
    SENIOR_ISSUES = 'Senior Issues'
    OTHER = 'Other'

    @classmethod
    def best_match_for_stance(cls, stance):
        """Select topic that best frames the proposal for this stance."""
        if stance == Stance.RECEPTIVE:
            return cls.SOCIAL_SECURITY
        elif stance == Stance.SKEPTICAL:
            return cls.BUDGET  # Fiscal responsibility framing
        else:
            return cls.SOCIAL_SECURITY  # Constituent protection framing


@dataclass
class Recipient:
    """A member of Congress to receive our proposal."""
    name: str
    chamber: Chamber
    state: str
    district: Optional[str]    # None for senators
    party: str
    stance: Stance
    dc_office: str
    dc_phone: str
    website: str
    contact_form: str
    state_offices: list = field(default_factory=list)
    committees: list = field(default_factory=list)
    notes: str = ''


@dataclass
class SubmissionRecord:
    """Tracks a single submission attempt."""
    recipient_name: str
    chamber: str
    stance: str
    channel: str
    status: str
    timestamp: str
    message_hash: str           # SHA-256 of submitted message
    subject: str
    confirmation_id: str = ''   # Auto-reply or confirmation code
    error_message: str = ''
    retry_count: int = 0
    follow_up_date: str = ''    # ISO date for follow-up
    notes: str = ''


# ═══════════════════════════════════════════════════════════════════════
#  1. MESSAGE GENERATOR
# ═══════════════════════════════════════════════════════════════════════

class MessageGenerator:
    """
    Generates personalized messages for each member of Congress
    based on their stance classification and the appropriate letter template.

    Uses the letter templates from proposals/political_letters/ and
    customizes them with:
      - Member's name and title
      - State/district-specific data
      - Stance-appropriate framing and subject line
      - Appropriate topic category for form dropdowns
    """

    # Subject lines by stance — designed for web form subject fields
    SUBJECTS = {
        Stance.RECEPTIVE: 'Expanding Social Security: Revenue-Constrained Benefit Extension',
        Stance.SKEPTICAL: 'Strengthening Social Security Solvency — Bipartisan Framework',
        Stance.HOSTILE: 'Protecting Social Security for 67 Million Retirees — Market-Based Approach',
    }

    # Shortened subjects for forms with character limits
    SHORT_SUBJECTS = {
        Stance.RECEPTIVE: 'Social Security Expansion Proposal',
        Stance.SKEPTICAL: 'Social Security Solvency Framework',
        Stance.HOSTILE: 'Protecting Social Security Benefits',
    }

    def __init__(self, sender_config=None):
        self.sender = sender_config or SENDER_CONFIG

    def generate_web_form_message(self, recipient):
        """
        Generate a message suitable for a congressional web contact form.
        Web forms typically have a 2,000-10,000 character limit.
        This produces a concise ~2,000 character version.
        """
        stance = recipient.stance
        name = recipient.name
        title = 'Senator' if recipient.chamber == Chamber.SENATE else 'Representative'

        if stance == Stance.RECEPTIVE:
            message = self._receptive_web_message(name, title, recipient)
        elif stance == Stance.SKEPTICAL:
            message = self._skeptical_web_message(name, title, recipient)
        else:
            message = self._hostile_web_message(name, title, recipient)

        return {
            'subject': self.SUBJECTS[stance],
            'short_subject': self.SHORT_SUBJECTS[stance],
            'topic': TopicCategory.best_match_for_stance(stance).value,
            'message': message,
            'message_hash': hashlib.sha256(message.encode()).hexdigest()[:16],
        }

    def _receptive_web_message(self, name, title, recipient):
        return f"""Dear {title} {name},

I am writing to bring to your attention a comprehensive, revenue-constrained proposal to expand Social Security benefits to all American adults living below the living wage threshold — without adding a single dollar to the federal deficit.

THE PROPOSAL: The Social Security Extension Act would:

1. RESTRUCTURE FICA to fund a new Tier 2 benefit for 138 million eligible adults (67M current SS beneficiaries + 71M working-age adults below $2,200/month living wage)

2. IMPLEMENT mark-to-market taxation on economic income exceeding $1 billion in wealth, generating $210 billion in Year 1, growing to $578 billion by Year 10

3. ESTABLISH a sovereign equity fund (modeled on Alaska's Permanent Fund and Norway's Government Pension Fund) to provide stable, growing returns

KEY NUMBERS FROM OUR MODEL:
- Year 1 benefits: $198-249/month per eligible adult
- Year 30 benefits: $798-1,731/month (depending on wealth tax inclusion)
- Income Gini reduction: 0.39 to 0.32 (18% — moves US to Canada's level)
- GDP impact: +5.3% by Year 30 via consumption multiplier effects
- Billionaire impact: Wealth still grows from $8.8B average to $110B over 40 years (vs $157B without tax)
- Social Security solvency: Guaranteed by revenue-constrained design — benefits adjust automatically to available revenue

This proposal has been modeled with five behavioral response regimes, stress-tested under adverse conditions, and analyzed for general equilibrium effects. Full documentation including a working paper, policy brief, and technical appendix are available.

I respectfully request the opportunity to provide a staff briefing on this proposal, and ask that you consider co-sponsoring enabling legislation.

Respectfully,
{self.sender['first_name']} {self.sender['last_name']}
{self.sender['city']}, {self.sender['state']} {self.sender['zip_code']}
{self.sender['email']}"""

    def _skeptical_web_message(self, name, title, recipient):
        return f"""Dear {title} {name},

I am writing regarding the Social Security solvency crisis. The trust fund is projected to be depleted by 2034, at which point 67 million beneficiaries face an automatic 23% benefit cut. I wish to bring a fiscally responsible solution to your attention.

THE PROPOSAL: A revenue-constrained Social Security modernization that:

1. RESTRUCTURES FICA contributions to fund extended benefits — no new deficit spending
2. Uses a mathematical revenue constraint: benefits = available_revenue / eligible_population — solvency is guaranteed by construction
3. OPTIONALLY supplements with a mark-to-market tax on billionaire economic income ($210B/year from 935 individuals holding $8.2 trillion)
4. Creates a sovereign equity fund (Alaska Permanent Fund / Norway model) for stable returns

FISCAL DISCIPLINE FEATURES:
- Zero deficit impact — revenue-constrained formula prevents overspending
- Benefits ratchet down automatically if revenue declines (Dybvig 1995 mechanism)
- Reserve fund covers temporary shortfalls without borrowing
- Independent actuarial review built into governance structure
- 40-year projection shows sustainable growth under 5 behavioral scenarios

The base model (FICA restructuring alone) delivers $106/month in Year 1 growing to $442/month by Year 30 for eligible adults below the living wage threshold. With the optional billionaire income tax, benefits reach $249/month in Year 1 and $1,731/month by Year 30.

This has been modeled with stress tests including 50% capital flight scenarios. Even under the most pessimistic assumptions, the program remains solvent because spending cannot exceed revenue.

I would welcome the opportunity to provide a 20-minute staff briefing with fiscal impact documentation.

Respectfully,
{self.sender['first_name']} {self.sender['last_name']}
{self.sender['city']}, {self.sender['state']} {self.sender['zip_code']}
{self.sender['email']}"""

    def _hostile_web_message(self, name, title, recipient):
        return f"""Dear {title} {name},

Social Security faces a solvency crisis that will directly impact your constituents. By 2034, the trust fund will be depleted and 67 million Americans — including retirees, disabled veterans, and survivors — face an automatic 23% benefit cut. This affects every state and every district.

I am writing to share a market-based approach to protecting these benefits:

THE APPROACH:
- Modernize Social Security's revenue structure using market-based returns, similar to the Alaska Permanent Fund (which has paid dividends to every Alaskan since 1982) and Norway's Government Pension Fund ($1.7 trillion)
- Revenue-constrained design: benefits can NEVER exceed available revenue — no deficit spending, no unfunded mandates
- Solvency guaranteed by mathematical construction, not political promises

BY THE NUMBERS:
- 67 million Americans currently depend on Social Security
- 2034: projected trust fund depletion year
- 23%: automatic benefit cut at depletion
- $28.0 trillion: current US GDP
- The proposed revenue structure delivers $106/month in additional benefits from Year 1, growing with market returns

This is not an expansion of government. It is a restructuring of existing revenue flows to protect benefits your constituents have earned and depend on. The design prevents any spending beyond what revenue supports.

A brief (4-page) analysis is available for your review. I respectfully request 20 minutes with your staff to discuss how this framework protects {recipient.state} constituents.

Respectfully,
{self.sender['first_name']} {self.sender['last_name']}
{self.sender['city']}, {self.sender['state']} {self.sender['zip_code']}
{self.sender['email']}"""

    def generate_cwc_xml(self, recipient, campaign_id='SSExtAct2025'):
        """
        Generate CWC-compliant XML for House submission.
        CWC requires specific XML format with mandatory fields.
        """
        msg = self.generate_web_form_message(recipient)
        s = self.sender

        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<CWC>
  <CWCVersion>2.0</CWCVersion>
  <Delivery>
    <CampaignId>{campaign_id}</CampaignId>
    <Organization>{s['organization']}</Organization>
    <OrganizationContact>{s['email']}</OrganizationContact>
    <Recipient>
      <MemberCode>{recipient.district or recipient.state}</MemberCode>
    </Recipient>
    <Constituent>
      <Prefix>{s['prefix']}</Prefix>
      <FirstName>{s['first_name']}</FirstName>
      <LastName>{s['last_name']}</LastName>
      <Email>{s['email']}</Email>
      <Phone>{s['phone']}</Phone>
      <Address1>{s['address_line_1']}</Address1>
      <Address2>{s['address_line_2']}</Address2>
      <City>{s['city']}</City>
      <StateAbbreviation>{s['state']}</StateAbbreviation>
      <Zip>{s['zip_code']}</Zip>
      <Zip4>{s['zip_plus_4']}</Zip4>
    </Constituent>
    <Message>
      <Subject>{msg['subject']}</Subject>
      <LibraryOfCongressTopic>{msg['topic']}</LibraryOfCongressTopic>
      <Body><![CDATA[{msg['message']}]]></Body>
    </Message>
  </Delivery>
</CWC>"""
        return xml

    def generate_usps_letter(self, recipient):
        """
        Generate a formatted USPS letter with proper addressing.
        Returns dict with envelope_address and letter_body.
        """
        msg = self.generate_web_form_message(recipient)
        title = 'Senator' if recipient.chamber == Chamber.SENATE else 'Representative'

        envelope = (
            f"The Honorable {recipient.name}\n"
            f"United States {recipient.chamber.value.title()}\n"
            f"{recipient.dc_office}"
        )

        letter_body = (
            f"{datetime.now().strftime('%B %d, %Y')}\n\n"
            f"The Honorable {recipient.name}\n"
            f"United States {recipient.chamber.value.title()}\n"
            f"{recipient.dc_office}\n\n"
            f"RE: {msg['subject']}\n\n"
            f"{msg['message']}\n\n"
            f"Enclosures:\n"
        )

        if recipient.stance == Stance.RECEPTIVE:
            letter_body += (
                "  - Executive Brief: Social Security Extension Act\n"
                "  - Policy Brief: Revenue-Constrained Benefit Framework\n"
                "  - Key Model Outputs (1 page)\n"
            )
        elif recipient.stance == Stance.SKEPTICAL:
            letter_body += (
                "  - Executive Brief: Social Security Solvency Framework\n"
                "  - Fiscal Impact Summary (1 page)\n"
            )
        else:
            letter_body += (
                "  - Executive Brief: Protecting Social Security Benefits\n"
                "  - Alaska PFD Comparison (1 page)\n"
            )

        return {
            'envelope_address': envelope,
            'letter_body': letter_body,
            'message_hash': msg['message_hash'],
        }


# ═══════════════════════════════════════════════════════════════════════
#  2. SUBMISSION ENGINE
# ═══════════════════════════════════════════════════════════════════════

class SubmissionEngine:
    """
    Multi-channel submission engine.

    Handles the actual delivery of messages through:
      - CWC API (House)
      - SCWC/SOAPBox API (Senate)
      - Web form automation (both chambers)
      - USPS letter generation (both chambers)
    """

    def __init__(self, sender_config=None):
        self.generator = MessageGenerator(sender_config)
        self.tracker = StatusTracker()

    def submit_via_web_form(self, recipient):
        """
        Submit message via congressional web contact form.

        IMPLEMENTATION OPTIONS:
        A) democracy.io — Simplest, handles form mapping automatically
           - Open source: github.com/sinak/democracy.io
           - Sends to your 2 senators + 1 representative
           - Limitation: only works for YOUR representatives (constituent check)

        B) EFF congress_forms — Most capable, handles CWC for House
           - Ruby gem: github.com/EFForg/congress_forms
           - Uses headless Chrome for Senate forms
           - CWC API for House forms
           - Requires vendor registration for CWC

        C) Direct browser automation — Custom Selenium/Playwright
           - Most flexible but most maintenance
           - Must handle reCAPTCHA (manual or service)
           - Each member's form has different fields

        D) Manual submission — Human fills out each form
           - Slowest but most reliable
           - Use generated messages as clipboard paste source
           - Realistic throughput: 20-30 forms per hour
        """
        msg = self.generator.generate_web_form_message(recipient)

        record = SubmissionRecord(
            recipient_name=recipient.name,
            chamber=recipient.chamber.value,
            stance=recipient.stance.value,
            channel=SubmissionChannel.WEB_FORM.value,
            status=SubmissionStatus.QUEUED.value,
            timestamp=datetime.now().isoformat(),
            message_hash=msg['message_hash'],
            subject=msg['subject'],
        )

        # === ACTUAL SUBMISSION WOULD GO HERE ===
        # For now, we generate the message and queue it for manual submission
        # See the ManualSubmissionGuide class below for human-executed workflow

        self.tracker.record(record)
        return record

    def submit_via_cwc(self, recipient):
        """
        Submit to House member via CWC API.

        PREREQUISITES:
        1. Register as advocacy vendor: CWCVendors@mail.house.gov
        2. Download and complete CWC Application from house.gov
        3. Receive signed application + technical specs
        4. Whitelist your IP addresses
        5. Implement XML schema per CWC standards

        CWC ENDPOINT: Provided upon vendor approval
        FORMAT: XML per CWC 2.0 schema
        DELIVERY: Direct to House Constituent Service Systems
        """
        if recipient.chamber != Chamber.HOUSE:
            raise ValueError("CWC is only for House members")

        xml = self.generator.generate_cwc_xml(recipient)

        record = SubmissionRecord(
            recipient_name=recipient.name,
            chamber=recipient.chamber.value,
            stance=recipient.stance.value,
            channel=SubmissionChannel.CWC_API.value,
            status=SubmissionStatus.QUEUED.value,
            timestamp=datetime.now().isoformat(),
            message_hash=hashlib.sha256(xml.encode()).hexdigest()[:16],
            subject=self.generator.SUBJECTS[recipient.stance],
        )

        # === CWC API CALL WOULD GO HERE ===
        # import requests
        # response = requests.post(CWC_ENDPOINT, data=xml,
        #     headers={'Content-Type': 'application/xml'})
        # record.status = 'submitted' if response.ok else 'failed'
        # record.confirmation_id = response.headers.get('X-CWC-ID', '')

        self.tracker.record(record)
        return record

    def submit_via_scwc(self, recipient):
        """
        Submit to Senator via SCWC / SOAPBox API.

        PREREQUISITES:
        1. Register at soapbox.senate.gov/registration/
        2. Meet high-volume message-sending infrastructure requirements
        3. Comply with Senate message-format requirements
        4. Mandatory + optional fields in standardized format

        ENDPOINT: SOAPBox (Senate Office Advocacy Portal Box)
        FORMAT: Standardized XML with mandatory constituent fields
        DELIVERY: Direct to Senate Constituent Service Systems (CSS)
        """
        if recipient.chamber != Chamber.SENATE:
            raise ValueError("SCWC is only for Senate members")

        msg = self.generator.generate_web_form_message(recipient)

        record = SubmissionRecord(
            recipient_name=recipient.name,
            chamber=recipient.chamber.value,
            stance=recipient.stance.value,
            channel=SubmissionChannel.SCWC_API.value,
            status=SubmissionStatus.QUEUED.value,
            timestamp=datetime.now().isoformat(),
            message_hash=msg['message_hash'],
            subject=msg['subject'],
        )

        # === SCWC API CALL WOULD GO HERE ===
        self.tracker.record(record)
        return record

    def generate_usps_letter(self, recipient):
        """Generate printable USPS letter and track it."""
        letter = self.generator.generate_usps_letter(recipient)

        record = SubmissionRecord(
            recipient_name=recipient.name,
            chamber=recipient.chamber.value,
            stance=recipient.stance.value,
            channel=SubmissionChannel.USPS_MAIL.value,
            status=SubmissionStatus.QUEUED.value,
            timestamp=datetime.now().isoformat(),
            message_hash=letter['message_hash'],
            subject=self.generator.SUBJECTS[recipient.stance],
            notes='Letter generated — print, sign, and mail',
        )

        self.tracker.record(record)
        return letter, record


# ═══════════════════════════════════════════════════════════════════════
#  3. BATCH ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════

class BatchOrchestrator:
    """
    Manages submission of messages to all 535 members of Congress.

    RECOMMENDED EXECUTION ORDER:
    Phase 1: Champions (5-10 members) — Manual web forms + USPS
    Phase 2: Receptive members (~212) — Web forms in batches
    Phase 3: Skeptical members (~50) — Web forms in batches
    Phase 4: Hostile gatekeepers (6) — USPS with hand-signed letters
    Phase 5: Remaining hostile members (~267) — Web forms or USPS
    """

    def __init__(self, sender_config=None):
        self.engine = SubmissionEngine(sender_config)
        self.tracker = StatusTracker()

    def build_recipient_list(self):
        """
        Build the full recipient list from our data files.
        Cross-references recipients with contact directories.
        """
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))

        recipients = []

        # Load Senate data
        try:
            from proposals.recipients.senate_recipients import SENATORS
            from proposals.recipients.senate_contact_directory import SENATE_CONTACTS
            for s in SENATORS:
                contact = SENATE_CONTACTS.get(s['name'], {})
                if not contact:
                    continue
                recipients.append(Recipient(
                    name=s['name'],
                    chamber=Chamber.SENATE,
                    state=s['state'],
                    district=None,
                    party=s['party'],
                    stance=Stance(s['stance']),
                    dc_office=contact.get('suite', 'TBD') + ' Senate Office Building, Washington, DC 20510',
                    dc_phone=contact.get('dc_phone', ''),
                    website=contact.get('website', ''),
                    contact_form=contact.get('contact_form', ''),
                    state_offices=contact.get('state_offices', []),
                    committees=s.get('committees', []),
                    notes=s.get('notes', ''),
                ))
        except ImportError:
            print("WARNING: Could not load Senate data")

        # Load House data
        try:
            from proposals.recipients.house_recipients import REPRESENTATIVES
            from proposals.recipients.house_contact_directory import HOUSE_CONTACTS

            # Build name mapping (house_recipients uses different names than house.gov)
            for r in REPRESENTATIVES:
                # Try direct name match first
                contact = HOUSE_CONTACTS.get(r['name'])
                if not contact:
                    # Try finding by district
                    for cname, cinfo in HOUSE_CONTACTS.items():
                        if cinfo['district'] == r['district']:
                            contact = cinfo
                            break
                if not contact:
                    contact = {}

                recipients.append(Recipient(
                    name=r['name'],
                    chamber=Chamber.HOUSE,
                    state=r['district'][:2] if r.get('district') else '',
                    district=r.get('district', ''),
                    party=r['party'],
                    stance=Stance(r['stance']),
                    dc_office=contact.get('dc_office', 'TBD'),
                    dc_phone=contact.get('dc_phone', ''),
                    website=contact.get('website', ''),
                    contact_form=contact.get('contact_form', ''),
                    committees=r.get('committees', []),
                    notes=r.get('notes', ''),
                ))
        except ImportError:
            print("WARNING: Could not load House data")

        return recipients

    def prioritize(self, recipients):
        """
        Sort recipients by priority for submission.

        Priority order:
        1. Top Champions (RECEPTIVE + key committee positions)
        2. Bridge/Skeptical (persuadable, bipartisan potential)
        3. Critical Gatekeepers (HOSTILE but control process)
        4. Remaining RECEPTIVE
        5. Remaining SKEPTICAL
        6. Remaining HOSTILE
        """
        CHAMPIONS = {
            'Ron Wyden', 'Bernie Sanders', 'Elizabeth Warren',
            'Sheldon Whitehouse', 'Cory Booker',
            'John Larson', 'Pramila Jayapal', 'Hakeem Jeffries',
            'Alexandria Ocasio-Cortez', 'Brendan Boyle',
            'Don Beyer', 'Lloyd Doggett', 'Rosa DeLauro',
            'Katherine Clark',
        }

        GATEKEEPERS = {
            'John Thune', 'Mike Crapo', 'Lindsey Graham',
            'Mike Johnson', 'Jason Smith', 'Jodey Arrington',
            'French Hill', 'Tom Cole',
        }

        BRIDGE = {
            'Bill Cassidy', 'Angus King', 'Susan Collins',
            'Lisa Murkowski', 'Mark Warner', 'Michael Bennet',
            'Brian Fitzpatrick', 'Richard Neal', 'Jared Golden',
        }

        def priority_key(r):
            if r.name in CHAMPIONS:
                return (0, r.name)
            if r.name in BRIDGE:
                return (1, r.name)
            if r.name in GATEKEEPERS:
                return (2, r.name)
            if r.stance == Stance.RECEPTIVE:
                return (3, r.name)
            if r.stance == Stance.SKEPTICAL:
                return (4, r.name)
            return (5, r.name)

        return sorted(recipients, key=priority_key)

    def generate_all_messages(self, recipients=None):
        """Generate messages for all recipients and save to files."""
        if recipients is None:
            recipients = self.prioritize(self.build_recipient_list())

        output_dir = LETTERS_OUTPUT_DIR

        # Clean previous generation (remove stale files from prior runs)
        import shutil
        for subdir in ['web_form', 'usps', 'cwc_xml']:
            subpath = output_dir / subdir
            if subpath.exists():
                shutil.rmtree(subpath)

        output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories by channel
        (output_dir / 'web_form').mkdir(exist_ok=True)
        (output_dir / 'usps').mkdir(exist_ok=True)
        (output_dir / 'cwc_xml').mkdir(exist_ok=True)

        manifest = []

        for i, r in enumerate(recipients):
            msg = self.engine.generator.generate_web_form_message(r)
            safe_name = r.name.replace(' ', '_').replace('.', '').replace("'", '')

            # Web form message (for clipboard paste)
            web_path = output_dir / 'web_form' / f'{i+1:03d}_{safe_name}.txt'
            with open(web_path, 'w') as f:
                f.write(f"RECIPIENT: {r.name}\n")
                f.write(f"CHAMBER: {r.chamber.value.upper()}\n")
                f.write(f"STATE/DISTRICT: {r.district or r.state}\n")
                f.write(f"PARTY: {r.party}\n")
                f.write(f"STANCE: {r.stance.value}\n")
                f.write(f"CONTACT FORM: {r.contact_form}\n")
                f.write(f"DC PHONE: {r.dc_phone}\n")
                f.write(f"{'=' * 60}\n")
                f.write(f"SUBJECT: {msg['subject']}\n")
                f.write(f"TOPIC: {msg['topic']}\n")
                f.write(f"{'=' * 60}\n\n")
                f.write(msg['message'])

            # USPS letter
            letter = self.engine.generator.generate_usps_letter(r)
            usps_path = output_dir / 'usps' / f'{i+1:03d}_{safe_name}.txt'
            with open(usps_path, 'w') as f:
                f.write(f"ENVELOPE ADDRESS:\n{letter['envelope_address']}\n\n")
                f.write(f"{'=' * 60}\n\n")
                f.write(letter['letter_body'])

            # CWC XML (House only)
            if r.chamber == Chamber.HOUSE:
                xml = self.engine.generator.generate_cwc_xml(r)
                xml_path = output_dir / 'cwc_xml' / f'{safe_name}.xml'
                with open(xml_path, 'w') as f:
                    f.write(xml)

            manifest.append({
                'priority': i + 1,
                'name': r.name,
                'chamber': r.chamber.value,
                'state_district': r.district or r.state,
                'party': r.party,
                'stance': r.stance.value,
                'contact_form': r.contact_form,
                'dc_phone': r.dc_phone,
                'web_form_file': str(web_path.name),
                'usps_file': str(usps_path.name),
                'subject': msg['subject'],
                'topic': msg['topic'],
            })

        # Save manifest
        manifest_path = output_dir / 'SUBMISSION_MANIFEST.json'
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Save CSV for spreadsheet use
        csv_path = output_dir / 'SUBMISSION_MANIFEST.csv'
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=manifest[0].keys())
            writer.writeheader()
            writer.writerows(manifest)

        return manifest


# ═══════════════════════════════════════════════════════════════════════
#  4. STATUS TRACKER
# ═══════════════════════════════════════════════════════════════════════

class StatusTracker:
    """
    Tracks submission status for all 535 members.
    Persists to JSON file for session continuity.
    """

    def __init__(self, db_path=None):
        self.db_path = db_path or TRACKER_DB_PATH
        self.records = self._load()

    def _load(self):
        if self.db_path.exists():
            with open(self.db_path) as f:
                data = json.load(f)
                return [SubmissionRecord(**r) for r in data]
        return []

    def _save(self):
        with open(self.db_path, 'w') as f:
            json.dump([asdict(r) for r in self.records], f, indent=2)

    def record(self, submission_record):
        self.records.append(submission_record)
        self._save()

    def update_status(self, recipient_name, new_status, **kwargs):
        for r in reversed(self.records):
            if r.recipient_name == recipient_name:
                r.status = new_status
                for k, v in kwargs.items():
                    if hasattr(r, k):
                        setattr(r, k, v)
                self._save()
                return True
        return False

    def get_status(self, recipient_name):
        for r in reversed(self.records):
            if r.recipient_name == recipient_name:
                return r
        return None

    def summary(self):
        """Generate submission progress summary."""
        by_status = {}
        by_stance = {}
        by_chamber = {}

        for r in self.records:
            by_status[r.status] = by_status.get(r.status, 0) + 1
            by_stance[r.stance] = by_stance.get(r.stance, 0) + 1
            by_chamber[r.chamber] = by_chamber.get(r.chamber, 0) + 1

        return {
            'total_records': len(self.records),
            'by_status': by_status,
            'by_stance': by_stance,
            'by_chamber': by_chamber,
            'unique_recipients': len(set(r.recipient_name for r in self.records)),
        }

    def pending_follow_ups(self):
        """List submissions due for follow-up."""
        today = datetime.now().date().isoformat()
        return [r for r in self.records
                if r.follow_up_date and r.follow_up_date <= today
                and r.status in ('submitted', 'confirmed')]

    def export_report(self, path=None):
        """Export full submission report as CSV."""
        path = path or (self.db_path.parent / 'submission_report.csv')
        if not self.records:
            return None
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=asdict(self.records[0]).keys())
            writer.writeheader()
            for r in self.records:
                writer.writerow(asdict(r))
        return path


# ═══════════════════════════════════════════════════════════════════════
#  5. MANUAL SUBMISSION GUIDE
# ═══════════════════════════════════════════════════════════════════════

class ManualSubmissionGuide:
    """
    Step-by-step workflow for human-executed web form submissions.
    This is the most reliable method for non-constituent outreach.

    Realistic throughput: 20-30 submissions per hour
    Total time for 535 members: ~18-27 hours of manual work
    Recommended: Spread over 5-7 days, 3-4 hours per session
    """

    WORKFLOW = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║         MANUAL WEB FORM SUBMISSION WORKFLOW                     ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║                                                                  ║
    ║  PREPARATION (do once):                                          ║
    ║  1. Run: python congressional_submission_process.py generate     ║
    ║     This creates per-member message files in generated_letters/  ║
    ║  2. Fill in SENDER_CONFIG at top of this file                    ║
    ║  3. Open SUBMISSION_MANIFEST.csv in a spreadsheet               ║
    ║  4. Set up a browser with auto-fill for your address fields      ║
    ║                                                                  ║
    ║  PER-MEMBER SUBMISSION (2-3 minutes each):                       ║
    ║  1. Open the member's contact_form URL from the manifest         ║
    ║  2. Fill in your personal info (use browser auto-fill)           ║
    ║  3. Select the TOPIC from the manifest (Social Security, etc.)   ║
    ║  4. Paste SUBJECT from the member's .txt file                    ║
    ║  5. Paste MESSAGE from the member's .txt file                    ║
    ║  6. Complete CAPTCHA if present                                  ║
    ║  7. Submit the form                                              ║
    ║  8. Mark as SUBMITTED in your spreadsheet                        ║
    ║  9. Note any confirmation number or auto-reply                   ║
    ║                                                                  ║
    ║  DAILY SCHEDULE (recommended):                                   ║
    ║  Day 1: Champions (14 members) — manual, with care              ║
    ║  Day 2: Bridge/Skeptical (50 members) — 3-hour session           ║
    ║  Day 3: Gatekeepers (8 members) — manual + USPS letters          ║
    ║  Day 4: Receptive batch 1 (100 members) — 4-hour session         ║
    ║  Day 5: Receptive batch 2 (112 members) — 4-hour session         ║
    ║  Day 6: Hostile batch 1 (125 members) — 4-hour session           ║
    ║  Day 7: Hostile batch 2 (126 members) — 4-hour session           ║
    ║                                                                  ║
    ║  FOLLOW-UP SCHEDULE:                                             ║
    ║  Week 2: Phone calls to Champions who haven't responded          ║
    ║  Week 3: Phone calls to Skeptical members                        ║
    ║  Week 4: Second web form submission to non-responsive Champions  ║
    ║  Month 2: USPS letters to all Gatekeepers + Champions            ║
    ║  Month 3: Follow-up with any member who responded                ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """

    TIPS = """
    SUBMISSION TIPS:

    1. NON-CONSTITUENT FILTERING:
       - Most forms ask for your address to verify you're a constituent
       - Non-constituent messages may be filtered or deprioritized
       - USPS letters bypass this — they're all read
       - For national policy proposals, mention in your message that
         this affects ALL Americans, not just one district

    2. CAPTCHA HANDLING:
       - Most Senate forms use reCAPTCHA v2 (checkbox)
       - Some House forms have no CAPTCHA (handled by CWC)
       - A few use hCaptcha or custom challenges
       - Budget 10-15 seconds per CAPTCHA

    3. FORM FIELD VARIATIONS:
       - Some forms have TOPIC dropdowns — use "Social Security" or
         "Budget/Spending" or "Other" with a note
       - Some require SUBJECT lines (100-200 char limit)
       - Message body limits: 2,000-10,000 characters typical
       - Our messages are ~1,500-2,000 chars — within all limits

    4. BROWSER SETUP:
       - Use Chrome with address auto-fill configured
       - Keep SUBMISSION_MANIFEST.csv open in another tab
       - Keep the member's .txt file open for copy-paste
       - Consider a clipboard manager for quick paste

    5. TRACKING:
       - Add a "submitted" column to your CSV
       - Note the date and any confirmation message
       - Flag any forms that reject non-constituent addresses
       - These flagged members get USPS letters instead
    """


# ═══════════════════════════════════════════════════════════════════════
#  6. USPS BULK MAIL PREPARATION
# ═══════════════════════════════════════════════════════════════════════

class USPSBulkPrep:
    """
    Prepare bulk USPS mail to all congressional offices.

    ADVANTAGES OF USPS:
    - No constituent filtering — every letter is opened and read
    - Physical presence carries more weight than electronic messages
    - Can include enclosures (executive brief, policy brief)
    - No CAPTCHA, no form variations, no technical issues
    - Standardized format for all 535 members

    COST ESTIMATE (First-Class Mail):
    - 535 letters × $0.73 = $390.55 (single page, no enclosures)
    - 535 letters × $1.00 = $535.00 (with 2-page enclosure)
    - 535 letters × $1.50 = $802.50 (with full brief enclosure)
    - Envelopes + paper + printing: ~$100-150
    - Total budget: $500-950 for all 535 members

    TIMELINE:
    - Mail processing: 1-2 days
    - Security screening: 7-14 days (irradiation facility)
    - Delivery to office: 14-21 days total
    - Response window: 4-8 weeks after delivery

    ALTERNATIVE: Use a congressional mail service like Lob.com
    for automated printing, addressing, and mailing.
    """

    def generate_print_batch(self, recipients):
        """Generate all USPS letters in print-ready format."""
        output_dir = LETTERS_OUTPUT_DIR / 'usps'
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate merge file for mail merge software
        merge_data = []
        for r in recipients:
            title = 'Senator' if r.chamber == Chamber.SENATE else 'Representative'
            chamber_name = 'United States Senate' if r.chamber == Chamber.SENATE else 'United States House of Representatives'
            merge_data.append({
                'title': title,
                'full_name': r.name,
                'chamber': chamber_name,
                'address': r.dc_office,
                'stance': r.stance.value,
            })

        merge_path = output_dir / 'mail_merge_data.csv'
        with open(merge_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=merge_data[0].keys())
            writer.writeheader()
            writer.writerows(merge_data)

        return merge_path


# ═══════════════════════════════════════════════════════════════════════
#  COMMAND-LINE INTERFACE
# ═══════════════════════════════════════════════════════════════════════

def main():
    import sys

    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUSAGE:")
        print("  python congressional_submission_process.py generate    # Generate all messages")
        print("  python congressional_submission_process.py status      # Show submission status")
        print("  python congressional_submission_process.py workflow    # Show manual workflow")
        print("  python congressional_submission_process.py champions   # Generate champion messages only")
        print("  python congressional_submission_process.py preview N   # Preview message for recipient #N")
        return

    command = sys.argv[1]

    if command == 'generate':
        print("=" * 70)
        print("  GENERATING MESSAGES FOR ALL 535 MEMBERS OF CONGRESS")
        print("=" * 70)

        orchestrator = BatchOrchestrator()
        recipients = orchestrator.prioritize(orchestrator.build_recipient_list())

        print(f"\n  Total recipients: {len(recipients)}")
        print(f"  RECEPTIVE: {sum(1 for r in recipients if r.stance == Stance.RECEPTIVE)}")
        print(f"  SKEPTICAL: {sum(1 for r in recipients if r.stance == Stance.SKEPTICAL)}")
        print(f"  HOSTILE:   {sum(1 for r in recipients if r.stance == Stance.HOSTILE)}")
        print(f"  Senate:    {sum(1 for r in recipients if r.chamber == Chamber.SENATE)}")
        print(f"  House:     {sum(1 for r in recipients if r.chamber == Chamber.HOUSE)}")

        print(f"\n  Generating messages...")
        manifest = orchestrator.generate_all_messages(recipients)

        print(f"\n  Generated {len(manifest)} message packages")
        print(f"  Output directory: {LETTERS_OUTPUT_DIR}")
        print(f"  Manifest: {LETTERS_OUTPUT_DIR / 'SUBMISSION_MANIFEST.csv'}")
        print(f"\n  Files created:")
        print(f"    web_form/  — {len(manifest)} clipboard-paste text files")
        print(f"    usps/      — {len(manifest)} printable letter files")
        house_count = sum(1 for m in manifest if m['chamber'] == 'house')
        print(f"    cwc_xml/   — {house_count} CWC XML files (House members)")

        print(f"\n  FIRST 15 RECIPIENTS (by priority):")
        for m in manifest[:15]:
            print(f"    {m['priority']:>3}. {m['name']:<30} [{m['stance']:>10}] {m['chamber']:>6} {m['state_district']}")

    elif command == 'status':
        tracker = StatusTracker()
        summary = tracker.summary()
        print("=" * 50)
        print("  SUBMISSION STATUS")
        print("=" * 50)
        if summary['total_records'] == 0:
            print("\n  No submissions recorded yet.")
            print("  Run 'generate' first, then submit messages.")
        else:
            print(f"\n  Total records: {summary['total_records']}")
            print(f"  Unique recipients: {summary['unique_recipients']}")
            print(f"\n  By Status:")
            for status, count in sorted(summary['by_status'].items()):
                print(f"    {status:<15} {count:>5}")
            print(f"\n  By Stance:")
            for stance, count in sorted(summary['by_stance'].items()):
                print(f"    {stance:<15} {count:>5}")

        follow_ups = tracker.pending_follow_ups()
        if follow_ups:
            print(f"\n  PENDING FOLLOW-UPS ({len(follow_ups)}):")
            for f in follow_ups[:10]:
                print(f"    {f.recipient_name:<30} due: {f.follow_up_date}")

    elif command == 'workflow':
        print(ManualSubmissionGuide.WORKFLOW)
        print(ManualSubmissionGuide.TIPS)

    elif command == 'champions':
        print("  Generating messages for Champions only...")
        orchestrator = BatchOrchestrator()
        recipients = orchestrator.prioritize(orchestrator.build_recipient_list())
        champions = recipients[:14]  # Top priority
        manifest = orchestrator.generate_all_messages(champions)
        print(f"  Generated {len(manifest)} champion messages")

    elif command == 'preview':
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        orchestrator = BatchOrchestrator()
        recipients = orchestrator.prioritize(orchestrator.build_recipient_list())
        if n <= len(recipients):
            r = recipients[n - 1]
            gen = MessageGenerator()
            msg = gen.generate_web_form_message(r)
            print(f"\n  PREVIEW — Recipient #{n}: {r.name} ({r.party}-{r.district or r.state})")
            print(f"  Stance: {r.stance.value}")
            print(f"  Contact: {r.contact_form}")
            print(f"  Subject: {msg['subject']}")
            print(f"  Topic: {msg['topic']}")
            print(f"  {'=' * 60}")
            print(msg['message'])

    else:
        print(f"  Unknown command: {command}")
        print("  Use: generate, status, workflow, champions, preview")


if __name__ == '__main__':
    main()
