# Social Security Extension Act — Economic Model & Congressional Outreach System

A comprehensive economic modeling system and congressional submission framework for funding expanded Social Security benefits through market-based revenue restructuring and optional billionaire wealth taxation — without adding to the federal deficit.

---

## What This Is

A fully modeled, revenue-constrained proposal to:

1. **Extend Social Security** to 138 million eligible adults (67M current SS beneficiaries + 71M working-age adults below the $2,200/month living wage)
2. **Fund it** through FICA restructuring + optional mark-to-market taxation on billionaire economic income (935 individuals holding $8.2 trillion)
3. **Guarantee solvency** by mathematical construction: `benefits = available_revenue / eligible_population` — spending can never exceed revenue
4. **Deliver it** to all 535 members of the 119th Congress via personalized, stance-specific messages across four submission channels

The system includes economic models, Monte Carlo stress tests, five behavioral response regimes, a complete proposal library (200 words to 50+ pages), political letters tailored to three ideological stances, a full congressional contact directory, and a multi-channel submission engine with 535 pre-generated message packages.

---

## Key Model Results

### Means-Tested Variant (138M eligible adults)

| Metric | FICA Only | With Wealth Tax (40%) |
|--------|-----------|----------------------|
| Year 1 benefit | $198/mo | $249/mo |
| Year 10 benefit | $280/mo | $545/mo |
| Year 30 benefit | $827/mo | $1,731/mo |
| Income Gini coefficient | 0.39 → 0.35 | 0.39 → 0.32 (18% reduction) |
| GDP impact (Year 30) | +3.1% | +5.3% |
| Deficit impact | $0 | $0 |

The 18% Gini reduction moves the US from above-Brazil inequality to approximately Canada's level.

Billionaire wealth still grows from $8.8B average to $110B over 40 years (vs $157B without the tax). No billionaire is made non-billionaire.

### Population Segmentation

| Group | Population | Eligibility |
|-------|-----------|-------------|
| Current SS beneficiaries | 67M | Always eligible |
| Working-age below $2,200/mo | 71M | Eligible |
| Working-age above $2,200/mo | 120M | Not eligible (don't need it) |
| **Total eligible** | **138M (53%)** | Benefit multiplier: 1.87x vs universal |

---

## Proposal Library

The proposal system generates the same core analysis in multiple formats, each tailored to a specific audience and political framing. All proposals are mapped in the [Proposal Matrix](proposals/PROPOSAL_MATRIX.py) across three axes: length/complexity, technical depth, and political stance.

### Short Format (Public / Media)

| Document | Length | Audience | Link |
|----------|--------|----------|------|
| Evening News Bullets | 200 words, 5-7 bullets | General public, TV/radio, social media | [`short_format/evening_news_bullets.py`](proposals/short_format/evening_news_bullets.py) |
| Op-Ed | ~800 words | Newspaper readers, opinion pages | [`short_format/op_ed.py`](proposals/short_format/op_ed.py) |
| Executive Brief | ~1,500 words (2 pages) | Congress members, senior staffers, governors | [`short_format/executive_brief.py`](proposals/short_format/executive_brief.py) |

### Medium Format (Policy / Technical)

| Document | Length | Audience | Link |
|----------|--------|----------|------|
| Policy Brief | ~5,000 words (8 pages) | Policy analysts, think tanks, committee staff | [`medium_format/policy_brief.py`](proposals/medium_format/policy_brief.py) |
| White Paper | ~12,000 words (20 pages) | Congressional committees, CBO, Treasury, OMB | [`medium_format/white_paper.py`](proposals/medium_format/white_paper.py) |

### Long Format (Academic / Research)

| Document | Length | Audience | Link |
|----------|--------|----------|------|
| Working Paper | ~25,000 words (35 pages) | Economists, NBER, CBO analysts | [`long_format/working_paper.py`](proposals/long_format/working_paper.py) |
| Journal Submission | 50+ pages (w/ online appendix) | Peer reviewers (JPE, AER, Brookings Papers) | [`long_format/journal_submission.py`](proposals/long_format/journal_submission.py) |

### Political Letters (Stance-Specific)

Each letter reframes the identical underlying proposal for different ideological audiences:

| Letter | Target Audience | Framing | Lead With | Link |
|--------|----------------|---------|-----------|------|
| Receptive | Progressive Caucus, CBC, labor allies | "Expand Social Security for the 21st Century" | Benefits, moral case, 138M eligible | [`political_letters/letter_receptive.py`](proposals/political_letters/letter_receptive.py) |
| Skeptical | Problem Solvers Caucus, moderate D/R | "Strengthen & Modernize Social Security" | Solvency, fiscal discipline, no deficit | [`political_letters/letter_skeptical.py`](proposals/political_letters/letter_skeptical.py) |
| Hostile | RSC, Freedom Caucus, anti-tax members | "Protect Social Security Through Market Returns" | Constituent protection, Alaska PFD model | [`political_letters/letter_hostile.py`](proposals/political_letters/letter_hostile.py) |

---

## Congressional Outreach System

### How It Works

The outreach system connects three data layers:

1. **Recipient classification** — Every member of the 119th Congress classified by political stance, committee positions, caucus memberships, and strategic importance
2. **Contact directory** — Full contact details for all 535 members: DC offices, district/state offices, phone numbers, websites, and web contact form URLs
3. **Submission engine** — Generates and delivers personalized messages through four channels, prioritized by strategic importance

### Stance Classifications (119th Congress)

| Stance | Senate | House | Total | Strategy |
|--------|--------|-------|-------|----------|
| **RECEPTIVE** | 35 | 179 | **214** | Expansion framing — request co-sponsorship |
| **SKEPTICAL** | 15 | 36 | **51** | Solvency/fiscal discipline — request staff briefing |
| **HOSTILE** | 50 | 220 | **270** | Constituent protection — provide brief for review |

Classification data: [`recipients/senate_recipients.py`](proposals/recipients/senate_recipients.py) (100 senators) | [`recipients/house_recipients.py`](proposals/recipients/house_recipients.py) (435 representatives)

Contact data: [`recipients/senate_contact_directory.py`](proposals/recipients/senate_contact_directory.py) | [`recipients/house_contact_directory.py`](proposals/recipients/house_contact_directory.py)

### Message Personalization

The [submission engine](proposals/submission/congressional_submission_process.py) generates a unique message for each member based on their stance:

| Stance | Subject Line | Topic Category | Core Pitch |
|--------|-------------|----------------|------------|
| RECEPTIVE | "Expanding Social Security: Revenue-Constrained Benefit Extension" | Social Security | 138M eligible adults, $249/mo Year 1, Gini reduction, co-sponsor request |
| SKEPTICAL | "Strengthening Social Security Solvency — Bipartisan Framework" | Budget/Spending | 2034 trust fund depletion, revenue-constrained = zero deficit, stress-tested |
| HOSTILE | "Protecting Social Security for 67 Million Retirees — Market-Based Approach" | Social Security | 23% benefit cut at depletion, Alaska PFD model, no new spending |

Messages are ~1,500-2,000 characters (within all congressional web form limits).

### Submission Channels

The system supports four delivery channels, ranked by effectiveness:

**House of Representatives (435 members):**

| Channel | Method | Prerequisites | Link |
|---------|--------|---------------|------|
| CWC API | Bulk XML delivery to constituent service systems | Vendor registration via CWCVendors@mail.house.gov | [house.gov/doing-business-with-the-house](https://www.house.gov/doing-business-with-the-house/communicating-with-congress-cwc) |
| Web forms | Browser-based submission to member contact pages | None (manual CAPTCHA solving) | Each member's contact_form URL |
| USPS mail | Physical letters to DC offices | Postage ($500-950 for all 535) | Auto-generated in `generated_letters/usps/` |

**Senate (100 members):**

| Channel | Method | Prerequisites | Link |
|---------|--------|---------------|------|
| SCWC / SOAPBox API | Standardized vendor delivery to Senate CSS | Registration at soapbox.senate.gov | [senate.gov/senators/scwc.htm](https://www.senate.gov/senators/scwc.htm) |
| Web forms | Browser-based submission (reCAPTCHA on most) | None (manual CAPTCHA solving) | Each member's contact_form URL |
| USPS mail | Physical letters to DC offices | Postage | Auto-generated in `generated_letters/usps/` |

**Related open-source tools:**
- [democracy.io](https://democracy.io) — Single interface for contacting your 3 representatives
- [EFF/congress_forms](https://github.com/EFForg/congress_forms) — Ruby gem, headless Chrome for Senate, CWC for House
- [unitedstates/contact-congress](https://github.com/unitedstates/contact-congress) — YAML form definitions

### Submission Priority

The batch orchestrator processes recipients in six priority tiers:

| Tier | Who | Count | Why First |
|------|-----|-------|-----------|
| 1. **Champions** | Wyden, Sanders, Warren, Larson, Jayapal, AOC, Jeffries, Booker, Whitehouse, Boyle, Beyer, Doggett, DeLauro, Clark | 14 | Most likely co-sponsors; set legislative momentum |
| 2. **Bridge** | King, Cassidy, Collins, Murkowski, Warner, Bennet, Fitzpatrick, Neal, Golden | 9 | Cross-aisle credibility; bipartisan narrative |
| 3. **Gatekeepers** | Thune (Maj. Leader), Crapo (Finance Chair), Graham (Budget), Johnson (Speaker), Smith (W&M Chair), Arrington (Budget Chair), Hill (FinSvc Chair), Cole (Approps Chair) | 8 | Control legislative calendar and committee referrals |
| 4. Remaining RECEPTIVE | Progressive Caucus, CBC, CHC, New Dem Coalition | ~200 | Build co-sponsor count |
| 5. Remaining SKEPTICAL | Problem Solvers, Blue Dog, moderate members | ~42 | Expand bipartisan support |
| 6. Remaining HOSTILE | RSC, Freedom Caucus, remaining R members | ~262 | Constituent awareness, record of contact |

### Caucus Targeting Strategy

| Caucus | Est. Members | Stance | Approach |
|--------|-------------|--------|----------|
| Congressional Progressive Caucus | ~100 | RECEPTIVE | Natural allies — expansion framing, equity emphasis |
| Congressional Black Caucus | ~60 | RECEPTIVE | Racial wealth gap closure, disproportionate benefit |
| Congressional Hispanic Caucus | ~40 | RECEPTIVE | Living wage access for Latino working families |
| New Democrat Coalition | ~95 | RECEPTIVE | Evidence-based, market mechanisms, growth emphasis |
| Blue Dog Coalition | ~10 | SKEPTICAL | Fiscal discipline, revenue constraint, no deficit |
| Problem Solvers Caucus | ~50 | SKEPTICAL | Bipartisan framework, solvency guarantee |
| Republican Study Committee | ~175 | HOSTILE | Market-based returns, Alaska PFD precedent |
| Freedom Caucus | ~45 | HOSTILE | Constituent protection, no unfunded mandates |

### 7-Day Manual Submission Workflow

For human-executed web form submissions (~20-30 forms/hour, 2-3 minutes each):

| Day | Target | Count | Estimated Time |
|-----|--------|-------|----------------|
| Day 1 | Champions | 14 | 1 hour (careful, personalized) |
| Day 2 | Bridge + Skeptical | 50 | 3 hours |
| Day 3 | Gatekeepers | 8 | 1 hour (+ USPS letters) |
| Day 4 | Receptive batch 1 | 100 | 4 hours |
| Day 5 | Receptive batch 2 | 112 | 4 hours |
| Day 6 | Hostile batch 1 | 125 | 4 hours |
| Day 7 | Hostile batch 2 | 126 | 4 hours |

**Follow-up schedule:**
- Week 2-3: Phone calls to Champions who haven't responded
- Week 4: Second web form submission to non-responsive Champions
- Month 2: USPS letters to all Gatekeepers + Champions
- Month 3: Follow-up with any member who responded

### Generated Output

Running `generate` creates 535 message packages across three formats:

```
generated_letters/
├── web_form/               # 535 clipboard-paste text files
│   ├── 001_Alexandria_Ocasio-Cortez.txt
│   ├── 002_Bernie_Sanders.txt
│   ├── ...
│   └── 535_Zach_Nunn.txt
├── usps/                   # 535 printable USPS letters with envelope addressing
│   ├── 001_Alexandria_Ocasio-Cortez.txt
│   └── ...
├── cwc_xml/                # 435 CWC 2.0 XML files (House members only)
│   ├── Alexandria_Ocasio-Cortez.xml
│   └── ...
├── SUBMISSION_MANIFEST.csv  # Full spreadsheet: priority, name, stance, contact URL, phone
└── SUBMISSION_MANIFEST.json # Machine-readable manifest
```

Each web form file includes a header block for quick reference:
```
RECIPIENT: Alexandria Ocasio-Cortez
CHAMBER: HOUSE
STATE/DISTRICT: NY-14
PARTY: D
STANCE: RECEPTIVE
CONTACT FORM: https://ocasio-cortez.house.gov/contact
DC PHONE: (202) 225-3965
============================================================
SUBJECT: Expanding Social Security: Revenue-Constrained Benefit Extension
TOPIC: Social Security
============================================================

Dear Representative Alexandria Ocasio-Cortez,
...
```

---

## Economic Models

### Core Model: SS Extension V2.0

[`models/ss_extension_model.py`](models/ss_extension_model.py) — The foundation. Frames expanded benefits as a **Title II-B extension** of Social Security (not standalone UBI), making it politically and legally a modification to an existing program rather than a new entitlement. Revenue-constrained: benefits = only what the system collects. No borrowing, no deficit, no unfunded mandates.

### Means-Tested Variant

[`models/ss_extension_means_tested.py`](models/ss_extension_means_tested.py) — Restricts eligibility to those who need it: 67M SS beneficiaries (always eligible) + 71M working-age adults earning below $2,200/month. Same revenue pool, 53% of adults eligible = 1.87x higher per-person benefits. Tracks when living wage milestone is reached.

### Wealth Tax Optimizer

[`models/wealth_tax_optimizer.py`](models/wealth_tax_optimizer.py) — Models a 40% mark-to-market tax on unrealized gains of 935 US billionaires ($8.2T in wealth). Generates $210B in Year 1, growing to $578B by Year 10. Includes five behavioral response regimes (see below) modeling capital flight, avoidance, and emigration.

### Living Wage Model

[`models/living_wage_model.py`](models/living_wage_model.py) — Full cost analysis for the $2,200/month living wage target (MIT Living Wage Calculator national average). Models 10 revenue sources and projects when Tier 2 benefits reach living-wage levels under different scenarios.

### General Equilibrium

[`models/general_equilibrium.py`](models/general_equilibrium.py) — Analyzes how a $10T+ sovereign fund affects asset prices (P/E expansion, equity risk premium compression), market liquidity, corporate governance, labor markets, and fiscal sustainability. References Gabaix & Koijen (2022) on inelastic market demand, Greenwood & Vayanos (2010), Kyle (1985).

### Social Security Integration

[`models/social_security_integration.py`](models/social_security_integration.py) — Models interaction with the existing $1.4T/year Social Security system. Addresses benefit stacking, partial solvency rescue of the trust fund, labor supply effects, and political feasibility of integration. References SSA (2024), CBO (2024), Hoynes & Rothstein (2019).

### Revenue Stack

[`models/revenue_stack.py`](models/revenue_stack.py) — Composite extraction from multiple sources: equity risk premium, financial transaction tax, volatility selling, securities lending, dividend capture, and buyback yield.

### Withdrawal Policy

[`models/withdrawal_policy.py`](models/withdrawal_policy.py) — Dynamic withdrawal smoothing engine that prevents benefit volatility across market cycles. Implements Dybvig (1995) ratchet mechanism — benefits never decrease year-over-year.

### Redistribution Analyzer

[`tools/redistribution_analyzer.py`](tools/redistribution_analyzer.py) — Synthesizes all model variants to compute cumulative redistribution flows, Gini coefficient trajectories, billionaire wealth paths, and GDP effects. References Saez & Zucman (2019), Piketty/Saez/Stantcheva (2014), Chetty et al. (2014).

---

## Five Behavioral Response Regimes

The wealth tax model is stress-tested under five capital-flight scenarios, ranging from best-case to system-failure:

| Regime | Revenue Haircut | Capital Flight | Avoidance | Emigration | Net Revenue (Y1) |
|--------|----------------|----------------|-----------|------------|-------------------|
| Realistic Central | 30% | Moderate | Moderate | Minimal | ~$147B |
| Original | 45% | Conservative | High | Low | ~$116B |
| Pessimistic | 50% | Maximum | Maximum | Moderate | ~$105B |
| Severely Reduced | 15% | Near-worst | Extreme | Significant | ~$31B |
| Near-Zero | 5% | Catastrophic | Near-total | Mass exodus | ~$11B |

Even under the most pessimistic regime, the program remains solvent because `benefits = available_revenue / eligible_population` — benefits automatically adjust downward. No deficit is possible by construction.

---

## Data Sources

| Data | Source | File |
|------|--------|------|
| Economic parameters | Damodaran (2024), Dimson-Marsh-Staunton (2023), SEC MIDAS, CBOE, BEA, BLS, Federal Reserve | [`data/parameters.py`](data/parameters.py) |
| Income distribution | Census Bureau CPS ASEC 2023, BLS CES, SSA Wage Statistics | [`data/income_distribution.py`](data/income_distribution.py) |
| Congressional roster | house.gov, senate.gov, committee pages, caucus directories | [`proposals/recipients/`](proposals/recipients/) |
| Senate offices & phones | Senate Sergeant at Arms / CIO Suite & Telephone List (July 2025) | [`recipients/senate_contact_directory.py`](proposals/recipients/senate_contact_directory.py) |
| House offices & phones | house.gov/representatives official directory | [`recipients/house_contact_directory.py`](proposals/recipients/house_contact_directory.py) |

---

## Governance & Research Foundations

[`governance/institutional_design.py`](governance/institutional_design.py) — Designs safeguards against political capture of a $10T+ sovereign fund. Analyzes lessons from Norway's GPFG (gold standard), Alaska's PFD (vulnerable to politics), Singapore's GIC, Malaysia's 1MDB (failure mode), and Chile's pension system. Implements Santiago Principles (2008) for sovereign wealth fund governance.

[`research/theoretical_foundations.py`](research/theoretical_foundations.py) — Academic underpinnings: equity risk premium persistence, optimal taxation theory, redistribution welfare effects, sovereign fund market impact. Maps theoretical results to model parameters and implementation choices.

---

## Architecture

```
ubiextractor/
├── models/                    # Economic models
│   ├── ss_extension_model.py           # Core SS Extension V2.0 (universal)
│   ├── ss_extension_means_tested.py    # Means-tested variant (138M eligible)
│   ├── wealth_tax_optimizer.py         # M2M wealth tax + 5 behavioral regimes
│   ├── living_wage_model.py            # Living wage thresholds & milestone analysis
│   ├── general_equilibrium.py          # GE impact (prices, liquidity, labor, fiscal)
│   ├── revenue_stack.py                # Composite extraction (ERP, FTT, vol, lending)
│   ├── withdrawal_policy.py            # Dynamic withdrawal smoothing (Dybvig ratchet)
│   └── social_security_integration.py  # SS trust fund integration & benefit stacking
│
├── data/                      # Calibrated parameters & distributions
│   ├── parameters.py                   # Central parameter repository (50+ calibrated values)
│   └── income_distribution.py          # US income CDF with time dynamics
│
├── simulations/               # Monte Carlo & stress testing
│   └── monte_carlo_fund.py             # Probabilistic fund trajectory engine
│
├── governance/                # Institutional design
│   └── institutional_design.py         # Anti-capture safeguards, sovereign fund governance
│
├── research/                  # Theoretical foundations
│   └── theoretical_foundations.py       # Literature review, parameter calibration sources
│
├── tools/                     # Analysis utilities
│   ├── redistribution_analyzer.py      # Inequality impact synthesis (Gini, wealth paths)
│   ├── composite_analyzer.py           # Full system analysis dashboard
│   └── visualize.py                    # Chart generation
│
├── output/                    # Generated visualizations
│   ├── fund_trajectory.png             # Fund growth over 40 years
│   ├── scenario_comparison.png         # Multi-scenario benefit comparison
│   ├── revenue_waterfall.png           # Revenue source breakdown
│   ├── ftt_laffer_curve.png            # Financial transaction tax optimization
│   └── ubi_distribution.png            # Benefit distribution analysis
│
├── proposals/                 # Complete proposal & outreach system
│   ├── PROPOSAL_MATRIX.py              # Master index: 7 formats x 3 depths x 3 stances
│   │
│   ├── short_format/                   # 200-1,500 words
│   │   ├── evening_news_bullets.py     # 200 words — TV/radio/social
│   │   ├── op_ed.py                    # 800 words — newspaper opinion
│   │   └── executive_brief.py         # 1,500 words — legislative brief
│   │
│   ├── medium_format/                  # 5,000-12,000 words
│   │   ├── policy_brief.py            # 8 pages — think tanks, committee staff
│   │   └── white_paper.py             # 20 pages — CBO, Treasury, OMB
│   │
│   ├── long_format/                    # 25,000-50,000+ words
│   │   ├── working_paper.py           # 35 pages — NBER-style, JEL codes
│   │   └── journal_submission.py      # 50+ pages — AER/JPE/Brookings target
│   │
│   ├── political_letters/              # Stance-specific congressional letters
│   │   ├── letter_receptive.py        # "Expand SS" — progressives, labor
│   │   ├── letter_skeptical.py        # "Strengthen SS" — moderates, bipartisan
│   │   └── letter_hostile.py          # "Protect SS" — conservatives, market-based
│   │
│   ├── recipients/                     # 535-member congressional directory
│   │   ├── senate_recipients.py       # 100 senators: stance, committees, strategy
│   │   ├── house_recipients.py        # 435 reps: stance, committees, caucuses
│   │   ├── senate_contact_directory.py # DC suites, phones, websites, state offices
│   │   └── house_contact_directory.py # DC offices, phones, websites, district offices
│   │
│   └── submission/                     # Multi-channel delivery system
│       ├── congressional_submission_process.py  # Engine: generator, orchestrator, tracker
│       └── generated_letters/          # 535 ready-to-send message packages
│           ├── web_form/  (535 files)  # Clipboard-paste for contact forms
│           ├── usps/      (535 files)  # Printable letters with envelope addressing
│           ├── cwc_xml/   (435 files)  # House CWC 2.0 API XML
│           ├── SUBMISSION_MANIFEST.csv # Spreadsheet: priority, contact, stance
│           └── SUBMISSION_MANIFEST.json
```

---

## Quick Start

### Run the economic models

```bash
python models/ss_extension_model.py              # Core model — universal benefits
python models/ss_extension_means_tested.py        # Means-tested variant (138M eligible)
python models/wealth_tax_optimizer.py             # Wealth tax + 5 behavioral regimes
python models/living_wage_model.py                # Living wage milestone analysis
python models/general_equilibrium.py              # GE impact modeling
python models/social_security_integration.py      # SS trust fund integration
python simulations/monte_carlo_fund.py            # Fund trajectory simulation
python tools/redistribution_analyzer.py           # Inequality impact synthesis
python tools/composite_analyzer.py                # Full system dashboard
```

### Generate congressional submission packages

```bash
# 1. Edit SENDER_CONFIG at top of congressional_submission_process.py
#    Fill in: name, email, phone, address (required for congressional forms)

# 2. Generate all 535 message packages
python proposals/submission/congressional_submission_process.py generate

# 3. View the manual submission workflow
python proposals/submission/congressional_submission_process.py workflow

# 4. Preview any recipient's message (by priority number)
python proposals/submission/congressional_submission_process.py preview 1   # AOC
python proposals/submission/congressional_submission_process.py preview 27  # John Thune
python proposals/submission/congressional_submission_process.py preview 535 # Zach Nunn

# 5. Generate only champion messages (top 14)
python proposals/submission/congressional_submission_process.py champions

# 6. Check submission tracking
python proposals/submission/congressional_submission_process.py status
```

### Use the submission manifest

Open `generated_letters/SUBMISSION_MANIFEST.csv` in any spreadsheet. Columns:

| Column | Description |
|--------|-------------|
| priority | 1-535 submission order |
| name | Member name |
| chamber | senate / house |
| state_district | State or district code |
| party | D / R / I |
| stance | RECEPTIVE / SKEPTICAL / HOSTILE |
| contact_form | URL to member's web contact form |
| dc_phone | DC office phone number |
| web_form_file | Filename of clipboard-paste message |
| usps_file | Filename of printable USPS letter |
| subject | Pre-written subject line |
| topic | Form dropdown category |

---

## Requirements

- Python 3.10+
- numpy, scipy, matplotlib, pandas (for models and simulations)
- No additional dependencies for proposal generation or submission workflow

---

## License

This work is released for public policy research and advocacy purposes.
