"""
Institutional Design & Governance Architecture for Sovereign UBI Fund

The single biggest risk to a market-funded UBI is not financial — it's political.
A $10T+ fund would be the largest pool of capital in human history and an
irresistible target for political capture, corruption, and mismanagement.

This module designs the institutional architecture to prevent these failures.

Key Design Principles:
1. Constitutional entrenchment (not just statutory)
2. Multi-stakeholder governance with veto rights
3. Rule-based operations (minimize discretion)
4. Radical transparency
5. International diversification (reduces domestic political leverage)
6. Independent validation

Historical Lessons:
- Norway GPFG: Gold standard of governance (Norges Bank, Ministry of Finance, Parliament)
- Alaska PFD: Vulnerable to legislative raids (2016 veto controversy)
- Singapore GIC/Temasek: Effective but opaque
- Malaysia 1MDB: Catastrophic governance failure
- Chile pension system: Political pressure to withdraw during crises
- Social Security Trust Fund: Accounting fiction, no real assets

References:
- Clark & Monk (2017) "Institutional Investors in Global Markets"
- Monk (2009) "Recasting the Sovereign Wealth Fund Debate"
- Al-Hassan et al (2013) "Sovereign Wealth Funds: Aspects of Governance"
- Santiago Principles (IWG, 2008) — IFSWF Governance Standards
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class GovernanceTier(Enum):
    """Levels of governance authority."""
    CONSTITUTIONAL = "constitutional"  # Requires amendment to change
    STATUTORY = "statutory"            # Requires legislation to change
    REGULATORY = "regulatory"          # Board/agency can modify
    OPERATIONAL = "operational"        # Management discretion


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class GovernanceBody:
    """A governing institution within the fund architecture."""
    name: str
    role: str
    members: int
    appointment_method: str
    term_years: int
    removal_process: str
    veto_powers: list[str] = field(default_factory=list)
    transparency_requirements: list[str] = field(default_factory=list)


@dataclass
class GovernanceRule:
    """A specific governance rule or constraint."""
    name: str
    description: str
    tier: GovernanceTier
    enforcement_mechanism: str
    override_requirement: str


class InstitutionalArchitecture:
    """
    Complete institutional design for the sovereign UBI fund.

    Architecture modeled on best practices from Norway, Singapore,
    and central bank independence literature.

    Structure:
    ┌─────────────────────────────────────────────────┐
    │              CONSTITUTIONAL LAYER                │
    │  (Fund existence, UBI right, asset protection)   │
    ├─────────────────────────────────────────────────┤
    │              OVERSIGHT BOARD                     │
    │  (15 members, multi-stakeholder, veto rights)    │
    ├─────────────┬───────────────┬───────────────────┤
    │ INVESTMENT  │  DISTRIBUTION │  AUDIT &          │
    │ COMMITTEE   │  COMMITTEE    │  TRANSPARENCY     │
    │ (CIO +      │  (Withdrawal  │  OFFICE           │
    │  portfolio)  │   rules, UBI) │  (Independent)    │
    ├─────────────┴───────────────┴───────────────────┤
    │              OPERATIONS                          │
    │  (Execution, custody, reporting)                 │
    └─────────────────────────────────────────────────┘
    """

    def __init__(self):
        self.bodies = self._define_governing_bodies()
        self.rules = self._define_governance_rules()
        self.risk_controls = self._define_risk_controls()
        self.transparency = self._define_transparency_requirements()

    def _define_governing_bodies(self) -> list[GovernanceBody]:
        return [
            GovernanceBody(
                name="Sovereign UBI Fund Board of Governors",
                role=(
                    "Supreme governing authority. Sets investment policy, "
                    "approves withdrawal rates, oversees all operations. "
                    "Cannot modify constitutional provisions."
                ),
                members=15,
                appointment_method=(
                    "5 appointed by President (confirmed by Senate), "
                    "3 by Federal Reserve Board, "
                    "2 by Congressional Budget Office, "
                    "2 elected by UBI recipients (lottery + election), "
                    "3 independent experts (selected by existing board, "
                    "confirmed by Senate)"
                ),
                term_years=10,
                removal_process="2/3 Senate vote or judicial finding of malfeasance",
                veto_powers=[
                    "Any withdrawal exceeding constitutional rate cap",
                    "Any change to investment policy outside approved bands",
                    "Any transaction with related parties",
                    "Any use of fund assets as collateral for sovereign debt",
                ],
                transparency_requirements=[
                    "All meetings recorded and transcribed",
                    "All votes public within 24 hours",
                    "No member may hold other financial sector positions",
                    "5-year cooling-off period post-service",
                    "Full financial disclosure of all members",
                ],
            ),
            GovernanceBody(
                name="Investment Committee",
                role=(
                    "Manages portfolio allocation within Board-approved bands. "
                    "Hires/fires external managers. Executes rebalancing. "
                    "Cannot deviate from strategic asset allocation by >5%."
                ),
                members=7,
                appointment_method=(
                    "CIO + 6 members appointed by Board. "
                    "Must have >15 years institutional investment experience."
                ),
                term_years=7,
                removal_process="Board vote (majority)",
                veto_powers=[
                    "Reject any single investment >0.5% of fund",
                    "Reject any new asset class not in approved universe",
                ],
                transparency_requirements=[
                    "Quarterly portfolio disclosure (60-day delay)",
                    "Annual performance attribution report",
                    "All external manager fees disclosed",
                ],
            ),
            GovernanceBody(
                name="Distribution Committee",
                role=(
                    "Manages UBI withdrawal calculations and disbursement. "
                    "Operates within constitutional withdrawal rate bands. "
                    "Cannot modify the withdrawal formula — only apply it."
                ),
                members=5,
                appointment_method="Board appointment, Senate confirmation",
                term_years=8,
                removal_process="Board vote (supermajority)",
                veto_powers=[
                    "Reject any ad-hoc withdrawal outside formula",
                    "Reject any change to distribution infrastructure",
                ],
                transparency_requirements=[
                    "Monthly distribution reports",
                    "Real-time fund value publication",
                    "Annual actuarial review by independent auditor",
                ],
            ),
            GovernanceBody(
                name="Independent Audit & Transparency Office",
                role=(
                    "Continuous independent audit of all fund operations. "
                    "Reports directly to Congress and public. "
                    "Has full access to all fund data and systems."
                ),
                members=3,
                appointment_method=(
                    "Appointed by GAO Comptroller General. "
                    "Must be from Big 4 or equivalent with no fund conflicts."
                ),
                term_years=6,
                removal_process="Only by GAO Comptroller General",
                veto_powers=[
                    "Suspend any operation pending investigation",
                    "Require immediate public disclosure of any irregularity",
                ],
                transparency_requirements=[
                    "Real-time transaction monitoring dashboard (public)",
                    "Quarterly audit reports",
                    "Annual comprehensive governance review",
                ],
            ),
        ]

    def _define_governance_rules(self) -> list[GovernanceRule]:
        return [
            GovernanceRule(
                name="Asset Protection Clause",
                description=(
                    "Fund assets may not be used as collateral, pledged against "
                    "sovereign debt, redirected to general revenue, or raided "
                    "for any purpose other than UBI distribution."
                ),
                tier=GovernanceTier.CONSTITUTIONAL,
                enforcement_mechanism="Judicial review; standing for any citizen to sue",
                override_requirement="Constitutional amendment (2/3 Congress + 3/4 states)",
            ),
            GovernanceRule(
                name="Withdrawal Rate Band",
                description=(
                    "Annual withdrawals must be between 2.5% and 5.0% of the "
                    "trailing 5-year average fund value. The specific rate is "
                    "determined by the Distribution Committee using the "
                    "constitutionally prescribed formula."
                ),
                tier=GovernanceTier.CONSTITUTIONAL,
                enforcement_mechanism="Automatic formula; manual override requires Board supermajority",
                override_requirement="Constitutional amendment for band changes",
            ),
            GovernanceRule(
                name="Universal Distribution",
                description=(
                    "All adult citizens and permanent residents receive equal "
                    "UBI payments. No means testing, no conditions, no "
                    "geographic variation. Payments are not taxable income."
                ),
                tier=GovernanceTier.CONSTITUTIONAL,
                enforcement_mechanism="Automatic direct deposit; IRS/SSA infrastructure",
                override_requirement="Constitutional amendment",
            ),
            GovernanceRule(
                name="Investment Policy Constraints",
                description=(
                    "Fund must maintain: >60% global equities, <20% any single "
                    "country, <5% any single company, no direct real estate, "
                    "no private equity >10% of fund, no leverage >1.1x. "
                    "No investment in domestic government bonds (to prevent "
                    "the Social Security Trust Fund accounting fiction)."
                ),
                tier=GovernanceTier.STATUTORY,
                enforcement_mechanism="Board oversight; automatic compliance monitoring",
                override_requirement="Congressional legislation",
            ),
            GovernanceRule(
                name="Political Isolation",
                description=(
                    "No elected official may serve on any fund body. "
                    "No fund body may consider political factors in investment "
                    "decisions. ESG/exclusion mandates require supermajority "
                    "Board vote and 90-day public comment period."
                ),
                tier=GovernanceTier.STATUTORY,
                enforcement_mechanism="Board code of conduct; judicial review",
                override_requirement="Congressional legislation",
            ),
            GovernanceRule(
                name="Accumulation Phase Lock",
                description=(
                    "During the accumulation phase (first 15-25 years), "
                    "no withdrawals except in declared national emergencies "
                    "(requiring 2/3 Congressional vote + Presidential declaration + "
                    "Board approval). Even emergency withdrawals capped at 10% of fund."
                ),
                tier=GovernanceTier.STATUTORY,
                enforcement_mechanism="Automated system blocks; Board veto",
                override_requirement="Emergency declaration process",
            ),
            GovernanceRule(
                name="Radical Transparency",
                description=(
                    "All holdings disclosed quarterly (60-day delay). "
                    "All transactions disclosed monthly (30-day delay). "
                    "Real-time fund NAV published continuously. "
                    "All governance meetings transcribed and published. "
                    "Annual independent audit by two separate firms."
                ),
                tier=GovernanceTier.REGULATORY,
                enforcement_mechanism="Audit Office; FOIA; public dashboard",
                override_requirement="Board supermajority",
            ),
        ]

    def _define_risk_controls(self) -> list[dict]:
        return [
            {
                'risk': 'Political raid / diversion of assets',
                'severity': RiskLevel.CRITICAL,
                'mitigation': [
                    'Constitutional protection of fund assets',
                    'Judicial standing for any citizen',
                    'International custody (assets held outside US jurisdiction)',
                    'Multi-signature withdrawal requirements',
                ],
                'precedent': 'Alaska PFD survived 2016 raid attempt due to public outcry',
            },
            {
                'risk': 'Investment mismanagement / corruption',
                'severity': RiskLevel.CRITICAL,
                'mitigation': [
                    'Passive index strategy reduces discretion',
                    'Independent audit office with suspension powers',
                    'All external manager fees and performance disclosed',
                    'Criminal penalties for self-dealing',
                ],
                'precedent': '1MDB ($4.5B fraud) — prevented by transparency requirements',
            },
            {
                'risk': 'Market crash depletes fund during distribution',
                'severity': RiskLevel.HIGH,
                'mitigation': [
                    'Smoothed withdrawal formula (trailing 5-year average)',
                    'Withdrawal floor and ceiling (2.5-5.0%)',
                    'Counter-cyclical contribution buffer',
                    'Strategic reserve fund (6 months of distributions)',
                ],
                'precedent': 'Norway GPFG survived 2008 (-23%) via spending rule',
            },
            {
                'risk': 'Geopolitical risk to international holdings',
                'severity': RiskLevel.HIGH,
                'mitigation': [
                    'Maximum 20% in any single country',
                    'Diversified custody across jurisdictions',
                    'Bilateral investment treaties',
                    'Gradual rebalancing to reduce concentration',
                ],
                'precedent': 'Russia sanctions froze $300B in central bank reserves (2022)',
            },
            {
                'risk': 'Inflation erodes UBI purchasing power',
                'severity': RiskLevel.MEDIUM,
                'mitigation': [
                    'Equity returns historically beat inflation',
                    'TIPS/inflation-linked bond allocation (5-10%)',
                    'UBI payout linked to CPI floor',
                    'Commodity exposure provides natural hedge',
                ],
                'precedent': 'Equities returned 7% real over 120 years (DMS 2023)',
            },
            {
                'risk': 'Public opposition / fund abolition movement',
                'severity': RiskLevel.MEDIUM,
                'mitigation': [
                    'Constitutional entrenchment (very hard to repeal)',
                    'Universal benefit creates broad constituency',
                    'Regular public education and reporting',
                    'Citizen representatives on Board',
                ],
                'precedent': 'Social Security "third rail" — politically untouchable',
            },
        ]

    def _define_transparency_requirements(self) -> dict:
        return {
            'real_time': [
                'Fund NAV (net asset value) — updated every 15 seconds during market hours',
                'Trailing 12-month UBI payout per person',
                'Current withdrawal rate vs. constitutional band',
                'Accumulation progress tracker (% to target fund size)',
            ],
            'daily': [
                'Portfolio summary by asset class and geography',
                'Cash flow report (contributions, withdrawals, fees)',
            ],
            'monthly': [
                'Full transaction list (30-day delay)',
                'Performance attribution by strategy',
                'Risk exposure report (VaR, stress tests)',
            ],
            'quarterly': [
                'Complete holdings disclosure (60-day delay)',
                'External manager performance review',
                'Board meeting transcripts',
                'Distribution Committee formula calculations',
            ],
            'annual': [
                'Independent financial audit (two firms)',
                'Governance effectiveness review',
                'Actuarial sustainability assessment',
                'Public report card with citizen satisfaction survey',
                'Comparison to benchmark sovereign funds (Norway, Singapore)',
            ],
        }

    def print_architecture(self):
        """Print the full institutional architecture."""
        print("=" * 80)
        print("INSTITUTIONAL ARCHITECTURE — SOVEREIGN UBI FUND")
        print("=" * 80)

        print("\n--- GOVERNING BODIES ---")
        for body in self.bodies:
            print(f"\n  {body.name}")
            print(f"  {'Role:':<12} {body.role[:100]}...")
            print(f"  {'Members:':<12} {body.members}")
            print(f"  {'Terms:':<12} {body.term_years} years")
            print(f"  {'Appointed:':<12} {body.appointment_method[:80]}...")
            print(f"  {'Veto powers:':<12} {len(body.veto_powers)}")

        print("\n\n--- GOVERNANCE RULES ---")
        for rule in self.rules:
            print(f"\n  [{rule.tier.value.upper()}] {rule.name}")
            print(f"    {rule.description[:100]}...")
            print(f"    Override: {rule.override_requirement}")

        print("\n\n--- RISK CONTROLS ---")
        for rc in self.risk_controls:
            print(f"\n  [{rc['severity'].value.upper()}] {rc['risk']}")
            for m in rc['mitigation']:
                print(f"    - {m}")

        print("\n\n--- TRANSPARENCY SCHEDULE ---")
        for freq, items in self.transparency.items():
            print(f"\n  {freq.upper()}:")
            for item in items:
                print(f"    - {item}")


class ImplementationTimeline:
    """
    Phased implementation plan for the sovereign UBI fund.

    Phase 1 (Years 1-3):   Legislative foundation + seed capital
    Phase 2 (Years 3-10):  Accumulation phase I (build to $2-3T)
    Phase 3 (Years 10-20): Accumulation phase II (build to $8-12T)
    Phase 4 (Years 20-25): Transition to distribution
    Phase 5 (Years 25+):   Steady-state UBI distribution
    """

    @staticmethod
    def get_phases() -> list[dict]:
        return [
            {
                'phase': 1,
                'name': 'Legislative Foundation',
                'years': '1-3',
                'objectives': [
                    'Constitutional amendment ratified (fund protection + UBI right)',
                    'Enabling legislation passed (fund charter, governance bodies)',
                    'Initial seed capital: $500B (from redirected revenues + new FTT)',
                    'Board of Governors appointed and confirmed',
                    'Custody and operational infrastructure established',
                    'Public education campaign launched',
                ],
                'funding_sources': [
                    'Financial Transaction Tax: $50-60B/year',
                    'Federal asset monetization: $25-30B/year',
                    'Redirected existing transfer programs: $100B/year (phased)',
                    'Initial Treasury allocation: $200B (one-time)',
                ],
                'milestones': [
                    'Constitutional amendment ratified',
                    'First Board meeting held',
                    'First equity purchases executed',
                    'Public dashboard launched',
                ],
            },
            {
                'phase': 2,
                'name': 'Accumulation Phase I',
                'years': '3-10',
                'objectives': [
                    'Build fund to $2-3T through contributions + returns',
                    'Establish track record of governance and transparency',
                    'No distributions (accumulation lock in effect)',
                    'Begin securities lending program',
                    'Implement volatility premium harvesting',
                ],
                'funding_sources': [
                    'FTT: $60-80B/year (rate optimization)',
                    'Federal assets: $30B/year',
                    'Corporate equity contributions: phase in 1-2% of profits',
                    'Compound returns on existing holdings',
                ],
                'milestones': [
                    'Fund reaches $1T',
                    'Fund reaches $2T',
                    'First governance audit completed',
                    'International investment program launched',
                ],
            },
            {
                'phase': 3,
                'name': 'Accumulation Phase II',
                'years': '10-20',
                'objectives': [
                    'Build fund to $8-12T',
                    'Diversify internationally (reduce US concentration)',
                    'Build strategic reserve fund (6 months of future distributions)',
                    'Pilot UBI distributions to small test groups',
                ],
                'funding_sources': [
                    'All Phase 2 sources (growing with economy)',
                    'Compound returns (increasingly dominant)',
                    'Potential: carbon tax revenue allocation',
                ],
                'milestones': [
                    'Fund reaches $5T (largest sovereign fund globally)',
                    'Fund reaches $10T',
                    'Pilot distributions begin',
                    'Actuarial assessment confirms distribution readiness',
                ],
            },
            {
                'phase': 4,
                'name': 'Transition to Distribution',
                'years': '20-25',
                'objectives': [
                    'Begin UBI distributions (starting at lower rate, ramping up)',
                    'Year 20: $100-200/month per person',
                    'Year 25: $300-500/month per person',
                    'Optimize withdrawal rule based on 20 years of data',
                    'Continue accumulation (contributions > withdrawals initially)',
                ],
                'funding_sources': [
                    'Fund returns (now $400-600B/year at 4-5% real on $10T+)',
                    'Ongoing contributions (reduced as fund self-sustains)',
                ],
                'milestones': [
                    'First UBI payment issued',
                    'UBI reaches $200/month',
                    'Fund demonstrates sustainability through first bear market',
                    'Public approval >70%',
                ],
            },
            {
                'phase': 5,
                'name': 'Steady-State Distribution',
                'years': '25+',
                'objectives': [
                    'Mature UBI: $400-800/month per person (real dollars)',
                    'Fund self-sustaining (no new contributions needed)',
                    'Withdrawals = 3-4% of trailing 5-year average',
                    'Continuous governance improvement',
                    'Potential expansion to higher UBI as fund grows',
                ],
                'funding_sources': [
                    'Fund returns only (fully self-sustaining)',
                    'FTT revenue redirected to other public goods',
                ],
                'milestones': [
                    'UBI covers basic needs for lowest-income quintile',
                    'Fund weathers 2+ market cycles without distribution cuts',
                    'Model replicated by other nations',
                ],
            },
        ]

    @staticmethod
    def print_timeline():
        """Print the implementation timeline."""
        phases = ImplementationTimeline.get_phases()
        print("\n" + "=" * 80)
        print("IMPLEMENTATION TIMELINE")
        print("=" * 80)

        for phase in phases:
            print(f"\n{'─' * 80}")
            print(f"PHASE {phase['phase']}: {phase['name']} (Years {phase['years']})")
            print(f"{'─' * 80}")
            print("\n  Objectives:")
            for obj in phase['objectives']:
                print(f"    ▸ {obj}")
            print("\n  Funding Sources:")
            for src in phase['funding_sources']:
                print(f"    $ {src}")
            print("\n  Milestones:")
            for ms in phase['milestones']:
                print(f"    ✓ {ms}")


if __name__ == '__main__':
    arch = InstitutionalArchitecture()
    arch.print_architecture()
    ImplementationTimeline.print_timeline()
