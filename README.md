# Social Security Extension Act — Economic Model & Congressional Outreach System

A comprehensive economic modeling system and congressional submission framework for funding expanded Social Security benefits through market-based revenue restructuring and optional billionaire wealth taxation — without adding to the federal deficit.

## What This Is

A fully modeled, revenue-constrained proposal to:
1. **Extend Social Security** to 138 million eligible adults (67M current SS beneficiaries + 71M working-age adults below the living wage)
2. **Fund it** through FICA restructuring + optional mark-to-market taxation on billionaire economic income
3. **Guarantee solvency** by mathematical construction — benefits = available_revenue / eligible_population
4. **Deliver it** to all 535 members of Congress via personalized, stance-specific messages

## Key Model Results

| Metric | FICA Only | With Wealth Tax (40%) |
|--------|-----------|----------------------|
| Year 1 benefit | $198/mo | $249/mo |
| Year 10 benefit | $280/mo | $545/mo |
| Year 30 benefit | $827/mo | $1,731/mo |
| Income Gini | 0.39 → 0.35 | 0.39 → 0.32 |
| GDP impact (Y30) | +3.1% | +5.3% |
| Deficit impact | $0 | $0 |

Billionaire wealth still grows from $8.8B average to $110B over 40 years (vs $157B without tax).

## Architecture

```
ubiextractor/
├── models/                    # Economic models
│   ├── ss_extension_model.py           # Core SS Extension V2.0 (universal)
│   ├── ss_extension_means_tested.py    # Means-tested variant (138M eligible)
│   ├── wealth_tax_optimizer.py         # M2M wealth tax with behavioral regimes
│   ├── living_wage_model.py            # Living wage thresholds & analysis
│   ├── general_equilibrium.py          # GE impact (price, crowding, behavioral)
│   ├── revenue_stack.py                # Composite revenue extraction
│   ├── withdrawal_policy.py            # Dynamic withdrawal smoothing
│   └── social_security_integration.py  # SS trust fund integration
│
├── data/                      # Parameters & distributions
│   ├── parameters.py                   # Core economic parameters
│   └── income_distribution.py          # US income CDF (Census CPS-based)
│
├── simulations/               # Monte Carlo & stress testing
├── governance/                # Institutional design
├── research/                  # Literature review & foundations
├── tools/                     # Analysis utilities & visualization
├── output/                    # Generated charts & figures
│
├── proposals/                 # Complete proposal system
│   ├── PROPOSAL_MATRIX.py              # 7 formats × 3 complexity × 3 stances
│   ├── short_format/                   # Executive brief, op-ed, fact sheet
│   ├── medium_format/                  # Policy brief, white paper
│   ├── long_format/                    # Working paper, journal submission
│   ├── political_letters/              # Stance-specific congressional letters
│   │   ├── letter_receptive.py         # Expansion framing
│   │   ├── letter_skeptical.py         # Solvency/fiscal discipline framing
│   │   └── letter_hostile.py           # Constituent protection framing
│   │
│   ├── recipients/                     # Congressional directory (119th Congress)
│   │   ├── senate_recipients.py        # 100 senators with stance classifications
│   │   ├── house_recipients.py         # 435 reps with stance classifications
│   │   ├── senate_contact_directory.py # Full contact info (DC + state offices)
│   │   └── house_contact_directory.py  # Full contact info (DC + district offices)
│   │
│   └── submission/                     # Submission workflow system
│       ├── congressional_submission_process.py  # Multi-channel delivery engine
│       └── generated_letters/          # 535 ready-to-send message packages
│           ├── web_form/               # Clipboard-paste files for web forms
│           ├── usps/                   # Printable USPS letters
│           ├── cwc_xml/                # House CWC API XML files
│           ├── SUBMISSION_MANIFEST.csv # Full spreadsheet for tracking
│           └── SUBMISSION_MANIFEST.json
```

## Quick Start

### Run the economic models
```bash
python models/ss_extension_model.py              # Core model — universal benefits
python models/ss_extension_means_tested.py        # Means-tested variant
python models/wealth_tax_optimizer.py             # Wealth tax behavioral analysis
python models/living_wage_model.py                # Living wage milestone analysis
python models/general_equilibrium.py              # GE impact modeling
python simulations/monte_carlo_fund.py            # Fund trajectory simulation
```

### Generate congressional submission packages
```bash
# Edit SENDER_CONFIG in congressional_submission_process.py first
python proposals/submission/congressional_submission_process.py generate   # All 535 messages
python proposals/submission/congressional_submission_process.py champions  # Top 14 only
python proposals/submission/congressional_submission_process.py preview 1  # Preview any message
python proposals/submission/congressional_submission_process.py workflow   # Manual submission guide
python proposals/submission/congressional_submission_process.py status     # Track submissions
```

## Congressional Outreach

### Stance Classifications (119th Congress)
| Stance | Senate | House | Total | Strategy |
|--------|--------|-------|-------|----------|
| RECEPTIVE | 35 | 179 | 214 | Expansion framing — co-sponsor request |
| SKEPTICAL | 15 | 36 | 51 | Solvency/fiscal discipline framing |
| HOSTILE | 50 | 220 | 270 | Constituent protection framing |

### Submission Channels
- **CWC API** (House) — Bulk XML delivery to constituent service systems
- **SCWC/SOAPBox** (Senate) — Standardized vendor delivery
- **Web contact forms** — Manual or automated browser submission
- **USPS mail** — Physical letters to DC offices (most reliable for non-constituents)

### Priority Order
1. **Champions** (14): Wyden, Sanders, Warren, Larson, Jayapal, AOC, Jeffries...
2. **Bridge** (9): King, Cassidy, Collins, Murkowski, Fitzpatrick, Neal...
3. **Gatekeepers** (8): Thune, Crapo, Graham, Johnson, Smith, Arrington...
4. **Remaining**: RECEPTIVE → SKEPTICAL → HOSTILE

## Five Behavioral Response Regimes

The wealth tax model is stress-tested under five capital-flight scenarios:

| Regime | Revenue Haircut | Assumption |
|--------|----------------|------------|
| Pessimistic | 50% | Maximum avoidance + capital flight |
| Original | 45% | Conservative baseline |
| Realistic Central | 30% | Best empirical estimate |
| Severely Reduced | 15% | Near-worst case |
| Near-Zero | 5% | System effectively fails |

Even under the most pessimistic regime, the program remains solvent because benefits automatically adjust to available revenue.

## Requirements

- Python 3.10+
- numpy, scipy, matplotlib, pandas (for models/simulations)
- No additional dependencies for proposal generation

## License

This work is released for public policy research and advocacy purposes.
