"""
Theoretical Foundations & Literature Review

This module documents the academic underpinnings of the UBI Extractor system,
organized by the core theoretical questions it addresses.

Each section maps to a specific model component and provides:
- Key theoretical results
- Empirical calibration sources
- Open questions and limitations
- Connections to the implementation

This serves as both documentation and a computational reference
for the parameter choices in data/parameters.py.
"""


def print_literature_review():
    """Print the full theoretical foundations document."""

    print("=" * 80)
    print("THEORETICAL FOUNDATIONS — UBI EXTRACTOR")
    print("=" * 80)

    sections = [
        {
            'title': '1. THE EQUITY RISK PREMIUM — CAN IT FUND UBI?',
            'content': """
  The equity risk premium (ERP) is the foundational revenue source. If equities
  reliably earn 4-6% above risk-free rates, a sufficiently large fund can
  extract this premium to fund UBI.

  KEY THEORETICAL RESULTS:

  a) The ERP exists and is persistent (Mehra & Prescott 1985, "Equity Premium Puzzle")
     - Historical US ERP: ~5.5% geometric real (1926-2024)
     - Global ERP: ~3.5-4.5% geometric real (Dimson-Marsh-Staunton 2023)
     - The "puzzle" is that it's TOO HIGH given standard utility models
     - This works in our favor: there's a genuine surplus to harvest

  b) The ERP varies over time (Campbell & Shiller 1988, Cochrane 2011)
     - High CAPE -> lower future returns (R-squared ~30% at 10yr horizon)
     - Current CAPE ~33 implies below-average forward returns (~3-4% real)
     - Our model uses regime-switching to capture this variation

  c) The ERP may compress with more capital chasing it (Arnott et al 2021)
     - More passive indexing -> more capital in equities -> lower ERP
     - A $10T sovereign fund would accelerate this compression
     - Our GE model explicitly accounts for this (see general_equilibrium.py)

  CALIBRATION:
  - Mean real return: 6.5% (= 5% ERP + 1.5% risk-free)
  - Standard deviation: 17% (historical US, slightly conservative)
  - GE-adjusted ERP: 3.5-4.5% (after fund's own price impact)

  OPEN QUESTIONS:
  - Will the ERP persist in a world of ubiquitous passive investing?
  - How much does a $10T buyer compress the premium?
  - Should the fund diversify globally (lower ERP but lower vol)?
""",
        },
        {
            'title': '2. MARKET MICROSTRUCTURE — THE INELASTIC MARKETS HYPOTHESIS',
            'content': """
  Gabaix & Koijen (2022) demonstrated that equity markets are far more
  inelastic than previously assumed. This has profound implications for
  a sovereign fund's price impact.

  KEY RESULT: $1 of inflow raises market cap by ~$5 (multiplier of 5)

  WHY THIS MATTERS:
  - A $250B/year buying program raises market cap by ~$1.25T/year
  - Over 20 years: cumulative inflow of $5T -> market cap increase of $10-15T
  - The fund partly "creates" its own returns via price appreciation
  - But this is not free money — it compresses future returns

  THE FEEDBACK LOOP:
  1. Fund buys equities -> prices rise -> fund value increases
  2. Higher valuations -> lower dividend yields -> lower expected returns
  3. Lower expected returns -> less ERP to harvest -> lower UBI
  4. BUT: price level stays elevated as long as fund holds (permanent demand)

  CALIBRATION:
  - Multiplier: 5x (Gabaix-Koijen central estimate)
  - Adaptive decay: multiplier diminishes as market adjusts (~0.8^(t/10))
  - Net effect over 20 years: PE expansion of 15-25%, ERP compression of 1-2%

  IMPLICATION:
  Naive partial-equilibrium estimates overstate feasible UBI by 20-30%.
  The GE-adjusted estimate is the correct planning number.
""",
        },
        {
            'title': '3. OPTIMAL WITHDRAWAL THEORY — HOW TO SPEND DOWN',
            'content': """
  The withdrawal policy determines how volatile UBI payments are. This
  connects to deep results in consumption-portfolio theory.

  KEY THEORETICAL RESULTS:

  a) Merton (1969, 1971): Optimal consumption-portfolio problem
     - CRRA utility -> consume a fixed fraction of wealth
     - This IS the "constant percentage" rule
     - Optimal fraction depends on risk aversion, ERP, and volatility
     - For gamma=2, optimal rate ≈ ERP/(gamma * sigma^2) ≈ 3.5%

  b) Dybvig (1995): Ratchet consumption
     - If consumers have ratchet preferences (can't tolerate cuts),
       the optimal strategy spends less initially but never decreases
     - This is ultra-conservative but maximizes stability
     - Our "ratcheted" withdrawal rule implements this

  c) Waring & Siegel (2015): Spending rule comparison
     - Constant % is volatile (UBI swings with markets)
     - Constant dollar risks ruin (spending doesn't adjust to losses)
     - Hybrid rules (Yale model) offer the best tradeoff
     - Our "smoothed percentage" is the practical winner

  d) Endowment spending literature (Brown et al 2014)
     - Yale spends 5.25% of trailing 12-quarter average
     - Stanford uses similar smoothing
     - Norway uses 3% of current value (simpler, more conservative)

  OUR RECOMMENDATION:
  Smoothed percentage at 3.5% with alpha=0.3 (fast adaptation):
  - withdrawal_t = 0.3 * (fund_t * 0.035) + 0.7 * withdrawal_{t-1} * 1.02
  - This provides stability (70% based on last year) with adaptation (30% market)
  - Backtests show this survives 1930s, 1970s, 2000s, 2008, and 2020
""",
        },
        {
            'title': '4. FINANCIAL TRANSACTION TAX — THEORY AND EVIDENCE',
            'content': """
  The FTT is the most contentious revenue source. The theoretical debate
  pits Tobin/Stiglitz against Cochrane/market microstructure economists.

  ARGUMENTS FOR (Tobin 1978, Stiglitz 1989, Summers & Summers 1989):
  - Markets have excess speculation / noise trading
  - Small tax discourages short-term trading without harming long-term investors
  - Revenue is substantial given high trading volumes
  - Reduces destabilizing high-frequency trading

  ARGUMENTS AGAINST (Cochrane 2013, Amihud & Mendelson 2003):
  - Tax is regressive on retirement savers (via fund transaction costs)
  - Volume migrates to untaxed jurisdictions (Sweden 1984-91)
  - Spreads widen, harming ALL investors including retail
  - Revenue estimates are always overstated (Laffer curve)
  - Reduces price discovery efficiency

  EMPIRICAL EVIDENCE:
  - Sweden (1984-91): 50% of trading moved to London; tax repealed
  - UK Stamp Duty (0.5%): Survives because UK is a dominant venue
  - France FTT (2012): Revenue below projections; some volume migration
  - Italy FTT (2013): Revenue ~30% below estimates

  OUR CALIBRATION:
  - Volume elasticity: -0.8 (central; range -0.4 to -1.6)
  - Optimal rate: 3-8 bps depending on elasticity assumption
  - Revenue at 5 bps: $50-80B/year (after behavioral response)
  - This is useful as SEED CAPITAL, not as primary revenue source
""",
        },
        {
            'title': '5. UBI AND LABOR SUPPLY — THE EVIDENCE',
            'content': """
  The most common objection to UBI: "people will stop working."
  The evidence does not support this at moderate UBI levels.

  KEY EMPIRICAL STUDIES:

  a) Finland Basic Income Experiment (2017-2018)
     - 2,000 unemployed received 560 EUR/month unconditionally
     - Employment: +6% vs control (recipients MORE likely to work)
     - Wellbeing: significantly improved
     - Caveat: sample was already unemployed

  b) Stockton SEED (2019-2021)
     - 125 residents received $500/month for 2 years
     - Full-time employment: 28% -> 40% (vs 32% control)
     - Financial stability, mental health improved
     - Small sample, not randomized by income

  c) GiveDirectly Kenya (2016-ongoing)
     - $22/month for 12 years (large for local economy)
     - Labor supply: slight increase (recipients invest in businesses)
     - Local multiplier effects: ~2.5x (Egger et al 2022)

  d) Alaska PFD (1982-present)
     - ~$1,000-2,000/year to all residents
     - Jones & Marinescu (2022): no reduction in employment
     - Part-time work increased slightly (voluntary flexibility)

  e) Negative Income Tax Experiments (US, 1968-1982)
     - SIME/DIME, Gary, New Jersey experiments
     - Primary earners: 0-5% hours reduction
     - Secondary earners: 5-15% reduction (often for childcare)
     - Most reduction in lowest-income groups

  OUR CALIBRATION:
  - At $500/month: 1-2% employment reduction, offset by +5% entrepreneurship
  - At $1000/month: 3-5% employment reduction, larger entrepreneurship boost
  - Net GDP impact: -0.5% to +0.5% (roughly neutral)
  - Health and education improvements provide long-run productivity gains
""",
        },
        {
            'title': '6. SOVEREIGN FUND GOVERNANCE — LESSONS FROM PRACTICE',
            'content': """
  Governance is the binding constraint. A $10T fund with poor governance
  would be catastrophic. The evidence from existing funds:

  SUCCESSES:
  - Norway GPFG: $1.6T, managed by Norges Bank Investment Management
    - Strict spending rule (3%), massive transparency, no political influence
    - Annual return 5.9% since 1998; survived 2008 (-23%) without policy change
    - Key: Parliament sets rule, cannot override without formal process

  - Singapore GIC: ~$770B (estimated), more opaque but well-governed
    - Professional management, long-term horizon
    - Key: Insulated from electoral politics (authoritarian advantage)

  FAILURES:
  - Malaysia 1MDB: $4.5B stolen through complex financial fraud
    - Key failure: No independent audit, opaque structure, political control
  - Libya Investment Authority: $67B frozen, much mismanaged
    - Key failure: Authoritarian control without checks
  - Venezuela oil fund: Depleted by populist spending
    - Key failure: No constitutional protection, no spending rule

  MIXED:
  - Alaska PFD: Works financially but politically fragile
    - 2016: Governor vetoed half the dividend for budget gap
    - Public outcry restored it, but demonstrated vulnerability
  - Chile AFP pension system: Technically sound but politically unpopular
    - 2019: Pressure to allow withdrawals (which defeats the purpose)
    - 3 rounds of COVID withdrawals depleted ~20% of pension assets

  OUR DESIGN PRINCIPLES (from Clark & Monk 2017):
  1. CONSTITUTIONAL protection (not just statutory)
  2. RULE-BASED operations (minimize discretion)
  3. RADICAL TRANSPARENCY (real-time data, public audits)
  4. MULTI-STAKEHOLDER governance (prevents capture by any faction)
  5. INTERNATIONAL DIVERSIFICATION (reduces domestic political leverage)
  6. CITIZEN REPRESENTATION (creates political constituency for fund)
""",
        },
        {
            'title': '7. POLITICAL ECONOMY — THE HARDEST PART',
            'content': """
  Financing is the easy part. The political path is the hard part.

  CHALLENGES:
  a) Time inconsistency: 20+ years with no payouts requires extraordinary
     political commitment across multiple administrations
  b) Contribution funding: $200-500B/year in new revenue is a massive
     political lift (roughly 5-12% of federal revenue)
  c) Constituency building: Who fights for a fund that won't pay out
     for two decades?
  d) Ideological opposition: Left (want immediate spending), Right (oppose
     government ownership of equities)

  POSSIBLE POLITICAL PATHS:
  a) "Alaska for America": Frame as everyone's birthright to national wealth
     - Alaska PFD is wildly popular (80%+ approval)
     - Extend the concept nationally
  b) "Baby Bonds + Growth": Start with baby bonds ($1000/child at birth,
     invested until 18), expand to full UBI over time
     - Cory Booker's proposal as proof of concept
  c) "Digital Dividend": Frame as citizen's share of tech/data economy
     - Tech companies pay equity into national fund
     - Silicon Valley extraction narrative
  d) "Climate Dividend": Carbon tax revenue seeds the fund
     - Build on carbon dividend proposals (Citizens' Climate Lobby)
     - $50/ton CO2 -> ~$250B/year in revenue

  MOST REALISTIC PATH:
  Start small, prove the concept, expand:
  1. Year 0: Carbon tax + FTT -> $100B/year into new fund
  2. Year 5: Fund reaches $750B, public sees the tracker growing
  3. Year 10: Fund reaches $2T, begin small dividends ($50/month)
  4. Year 15: Dividends become politically untouchable (like Social Security)
  5. Year 20: Ramp to $200-400/month, expand contributions
  6. Year 30+: Mature system at $400-700/month
""",
        },
    ]

    for section in sections:
        print(f"\n{'─' * 80}")
        print(f"  {section['title']}")
        print(f"{'─' * 80}")
        print(section['content'])


def print_bibliography():
    """Print key references organized by topic."""
    print("\n" + "=" * 80)
    print("KEY REFERENCES")
    print("=" * 80)

    refs = {
        'Equity Risk Premium': [
            'Mehra & Prescott (1985) "The Equity Premium: A Puzzle" J Monetary Econ',
            'Dimson, Marsh & Staunton (2023) "Credit Suisse Global Investment Returns Yearbook"',
            'Damodaran (2024) "Equity Risk Premiums" NYU Stern',
            'Campbell & Shiller (1988) "Stock Prices, Earnings, and Expected Dividends" J Finance',
            'Cochrane (2011) "Presidential Address: Discount Rates" J Finance',
        ],
        'Market Microstructure': [
            'Gabaix & Koijen (2022) "In Search of the Origins of Financial Fluctuations" NBER',
            'Kyle (1985) "Continuous Auctions and Insider Trading" Econometrica',
            'Koijen & Yogo (2019) "A Demand System Approach to Asset Pricing" J Political Econ',
        ],
        'Optimal Withdrawal': [
            'Merton (1969) "Lifetime Portfolio Selection" Rev Econ Stat',
            'Merton (1971) "Optimum Consumption and Portfolio Rules" J Econ Theory',
            'Dybvig (1995) "Dusenberrys Ratcheting of Consumption" J Econ Theory',
            'Waring & Siegel (2015) "The Only Spending Rule Article Youll Ever Need" FAJ',
            'Brown, Dimmock, Kang, Weisbenner (2014) "How University Endowments Respond to Shocks" Rev Fin Stud',
        ],
        'Financial Transaction Tax': [
            'Tobin (1978) "A Proposal for International Monetary Reform" Eastern Econ J',
            'Stiglitz (1989) "Using Tax Policy to Curb Speculative Trading" J Fin Services Res',
            'Summers & Summers (1989) "When Financial Markets Work Too Well" J Fin Services Res',
            'Baltagi, Li & Li (2006) "Transaction Tax and Stock Market Behavior" Empirical Econ',
            'Cochrane (2013) "Finance: Function Matters, Not Size" J Econ Perspectives',
        ],
        'UBI Empirical Evidence': [
            'Marinescu (2018) "No Strings Attached: The Behavioral Effects of US UBI" NBER',
            'Jones & Marinescu (2022) "The Labor Market Impacts of Universal and Permanent Cash Transfers" AEJ',
            'Cesarini, Lindqvist, Notowidigdo, Ostling (2017) "Effect of Wealth on Labor Supply" AER',
            'Egger, Haushofer, Miguel, Niehaus, Walker (2022) "General Equilibrium Effects of Cash Transfers" Econometrica',
            'Hoynes & Rothstein (2019) "Universal Basic Income in the US and Advanced Countries" Ann Rev Econ',
        ],
        'Sovereign Fund Governance': [
            'Clark & Monk (2017) "Institutional Investors in Global Markets" Oxford UP',
            'Chambers, Dimson & Ilmanen (2012) "The Norway Model" J Portfolio Mgmt',
            'Al-Hassan, Papaioannou, Skancke, Sung (2013) "Sovereign Wealth Funds" IMF Working Paper',
            'Ang (2014) "Asset Management: A Systematic Approach" Oxford UP',
            'International Working Group (2008) "Santiago Principles" IFSWF',
        ],
    }

    for topic, papers in refs.items():
        print(f"\n  {topic}:")
        for paper in papers:
            print(f"    - {paper}")


if __name__ == '__main__':
    print_literature_review()
    print_bibliography()
