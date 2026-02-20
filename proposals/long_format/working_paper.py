"""
Working Paper — Level 6C Proposal (NBER-style)
Format: ~25,000 words (35 pages), academic
Audience: Economists, academic researchers, CBO analysts
Tone: Academic, formal, methodologically rigorous
Citations: 50-80 references

NOTE: This file contains the structured outline and key sections of an
NBER-style working paper. The full paper would be typeset in LaTeX.
All model results reference the validated outputs from the SS Extension
model suite at /Volumes/Exine/revvy/dev/ubiextractor/.

Target venues: NBER Working Paper Series, Brookings Papers on Economic
Activity, Journal of Public Economics (working paper version)
"""

WORKING_PAPER_METADATA = {
    'title': 'Revenue-Constrained Income Security: A Mark-to-Market '
             'Approach to Social Security Extension',
    'authors': '[Authors]',
    'affiliation': '[Institutions]',
    'date': '[Date]',
    'jel_codes': ['H55', 'H24', 'H23', 'D31', 'E62', 'G28'],
    'keywords': [
        'Social Security', 'income security', 'mark-to-market taxation',
        'wealth taxation', 'sovereign wealth fund', 'income inequality',
        'revenue-constrained benefits', 'FICA reform',
    ],
}

ABSTRACT = """
We propose and model a three-component reform to the U.S. Social
Security system: (i) removal of the FICA earnings cap and extension of
payroll contributions to investment income, generating approximately
$728 billion annually in new revenue; (ii) a revenue-constrained
"Tier 2" income supplement for Social Security beneficiaries and
working-age adults below the living wage, covering approximately 138
million adults (53.4% of the adult population); and (iii) a 40%
mark-to-market income tax on billionaires, funding a sovereign equity
fund. The system is revenue-constrained by construction: benefits
equal only what the system collects, eliminating unfunded liabilities.

We calibrate behavioral responses using five regimes spanning the
empirical literature (Brulhart et al. 2022; Scheuer and Slemrod 2021)
and find that the system remains viable across all assumptions. Under
our central estimate (81% collection efficiency), the Tier 2 benefit
reaches $1,731/month within 30 years, reducing the U.S. post-tax
income Gini from 0.39 to 0.32. The billionaire income tax is shown to
be an accelerant rather than the engine: FICA reform alone sustains
the system, generating $106-198/month in Tier 2 benefits without any
wealth-related taxation.

We derive the optimal tax rate as a function of behavioral elasticities,
equity fund return assumptions, and a social welfare function that
weights the marginal utility of transfers against deadweight loss.
Monte Carlo simulation (10,000 runs) shows positive fund balances in
97.3% of 40-year scenarios under central parameters. General
equilibrium analysis incorporating the Gabaix-Koijen (2022) inelastic
markets framework shows equity risk premium compression of 0.3-0.5
percentage points at scale, with a net positive GDP effect of 1.5-5.3%.
"""

SECTIONS = {
    '1_introduction': """
1. INTRODUCTION

The Old-Age, Survivors, and Disability Insurance (OASDI) system faces
projected trust fund depletion in 2034 (SSA 2024). Simultaneously,
approximately 37% of working-age Americans earn below the living wage
as calculated by the MIT Living Wage Calculator (Glasmeier 2024), while
the effective tax rate on billionaire wealth accumulation averages 3.4%
(Eisinger, Ernsthausen, and Kiel 2021). These three facts — pending
insolvency, inadequate labor income, and undertaxed capital income —
jointly motivate the Social Security Extension (SSE).

This paper makes four contributions. First, we formalize the concept of
a revenue-constrained benefit: a transfer payment that is mechanically
tied to revenue collections, eliminating unfunded liabilities by
construction. This contrasts with the defined-benefit structure of
current Social Security, which creates promises that may outstrip
revenue. Second, we derive the optimal mark-to-market tax rate on
billionaire economic income as a function of behavioral elasticities,
fund return assumptions, and social welfare weights. Third, we
calibrate the model to U.S. data using five behavioral response
regimes spanning the empirical literature, demonstrating robustness.
Fourth, we compute the distributional impact — changes in the income
Gini, wealth Gini, and GDP — under each scenario.

The key insight is structural: the system's solvency does not depend on
the billionaire income tax. FICA reform alone (cap removal + investment
income extension) generates sufficient revenue to (a) cover the OASDI
deficit, (b) fund Tier 2 benefits at $106-198/month, and (c) seed a
sovereign equity fund. The billionaire tax is an accelerant that roughly
triples the benefit level and funds the equity fund more rapidly, but
the system is viable without it. This separation of engine (FICA) and
accelerant (billionaire tax) is both an analytical and political design
feature.

Related literature. Our work builds on several strands. The FICA reform
component draws on the large literature on Social Security reform
(Diamond and Orszag 2004; Goss 2010; CBO 2024). The mark-to-market
taxation framework follows Saez and Zucman (2019, 2021) and the Wyden
(2021) legislative proposal, with behavioral calibration from Brulhart
et al. (2022) and Scheuer and Slemrod (2021). The sovereign wealth fund
component draws on Bernstein (2017) on public wealth funds and the
empirical track records of the Norway GPFG (Norges Bank 2024) and
Alaska Permanent Fund (APFC 2024). The revenue-constrained benefit
design applies Dybvig's (1995) optimal consumption ratchet to public
transfer policy. Distributional analysis uses the Lerman-Yitzhaki
(1985) Gini decomposition. The general equilibrium framework
incorporates the Gabaix-Koijen (2022) inelastic markets hypothesis
and the IMF's (Ostry, Berg, and Tsangarides 2014) findings on the
growth effects of redistribution.
""",

    '2_model': """
2. MODEL

2.1 Revenue-Constrained Benefit Design

Let R_t denote total new revenue in year t, D_t the existing OASDI
deficit, F_t the equity fund contribution, and N_t the eligible
population. The Tier 2 benefit per person per month is:

    b_t = max(0, R_t - D_t - F_t) / (N_t * 12)                    (1)

This formula guarantees solvency: total outlays never exceed total
revenue. The system cannot accumulate unfunded liabilities.

We augment (1) with a benefit ratchet following Dybvig (1995):

    B_t = max(b_t, B_{t-1})                                        (2)

subject to a reserve fund constraint:

    B_t = B_{t-1}  if  S_t >= (B_{t-1} - b_t) * N_t * 12          (3)
    B_t = b_t + S_t / (N_t * 12)  otherwise

where S_t is the reserve fund balance. This ensures nominal benefits
never decrease while maintaining fiscal discipline.

2.2 Revenue Sources

Total new revenue R_t has two components:

    R_t = R^{FICA}_t + R^{BIT}_t                                   (4)

FICA reform revenue:

    R^{FICA}_t = (W_t - W^{cap}_t) * tau^{FICA} +
                 I_t * tau^{inv} +
                 existing adjustments                               (5)

where W_t is total wage income, W^{cap}_t is wage income below the
current cap, tau^{FICA} is the combined OASDI rate (12.4%), I_t is
investment income, and tau^{inv} is the investment income FICA rate
(half of employee share, 3.1%).

Billionaire Income Tax revenue:

    R^{BIT}_t = sum_j [Y^{econ}_{j,t} * tau^{BIT}(Y^{econ}_{j,t}) *
                (1 - alpha_j - epsilon_j)] * (1 - delta_j)^t        (6)

where Y^{econ}_{j,t} is the economic income of billionaire j (change
in net worth + consumption), tau^{BIT} is the graduated rate schedule,
alpha_j is the avoidance rate, epsilon_j is the evasion rate, and
delta_j is the annual emigration probability for tier j.

2.3 Behavioral Response

Following Brulhart et al. (2022) and Scheuer and Slemrod (2021), we
model three behavioral channels:

Avoidance: alpha(tau) = min(alpha_0 + alpha_1 * tau, alpha_max)     (7)

where alpha_0 is the base avoidance rate, alpha_1 is the avoidance
elasticity, and alpha_max is the ceiling. We calibrate five regimes:

  Pessimistic:       alpha_0 = 0.15, alpha_1 = 0.40, alpha_max = 0.50
  Original:          alpha_0 = 0.10, alpha_1 = 0.30, alpha_max = 0.45
  Realistic Central: alpha_0 = 0.07, alpha_1 = 0.22, alpha_max = 0.30
  Severely Reduced:  alpha_0 = 0.05, alpha_1 = 0.15, alpha_max = 0.15
  Near-Zero:         alpha_0 = 0.03, alpha_1 = 0.05, alpha_max = 0.05

Evasion: epsilon(tau) = epsilon_0 + epsilon_1 * tau                 (8)

Emigration: delta_j = f(tau, exit_cost_j, non_financial_cost_j)     (9)

where exit_cost_j = 0.238 * 0.56 * W_j (IRC 877A exit tax on
unrealized gains, which represent ~56% of wealth).

2.4 Eligible Population

Let F(y; t) denote the CDF of market income for working-age adults
at time t, calibrated to Census CPS ASEC (2023). The eligible
population is:

    N_t = N^{SS}_t + N^{WA}_t * F(y_bar * (1+g)^t; t)             (10)

where N^{SS}_t is Social Security beneficiaries, N^{WA}_t is working-
age adults, y_bar is the living wage threshold ($2,200/month), and g
is real wage growth (~0.4%/year), which shrinks the below-threshold
fraction over time.

2.5 Optimal Tax Rate

The social planner maximizes:

    max_{tau} W = sum_t beta^t [u(B_t) * N_t - DWL(tau)]           (11)

where u(.) is a concave social utility function for transfers, beta
is the discount factor, and DWL(tau) is the deadweight loss from
behavioral distortion. The first-order condition yields:

    tau* = (u'(B) * dB/dtau * N) / (dDWL/dtau)                    (12)

We solve this numerically for each behavioral regime and report the
sensitivity of tau* to the elasticity parameters.

2.6 General Equilibrium

We incorporate the Gabaix-Koijen (2022) inelastic markets framework
to model the price impact of sovereign fund equity purchases:

    dP/P = mu * (dF / P * Q)                                       (13)

where mu ~ 5 is the inelastic markets multiplier, dF is the fund's
annual equity inflow, and P * Q is the total market capitalization.

The labor market response follows Marinescu (2018) and Cesarini et al.
(2017):

    dL/L = eta_p * (B * 12 / w_bar) + eta_h * (B * 12 / w_bar)   (14)

where eta_p ~ -0.15 is the participation elasticity and
eta_h ~ -0.12 is the hours elasticity.

GDP impact:

    dY/Y = s_L * dL/L + MPC * k * B * 12 * N / Y + gamma * dG     (15)

where s_L is the labor share of GDP, MPC is the marginal propensity
to consume for recipients (~0.90), k is the fiscal multiplier (1.4),
and gamma * dG captures the IMF (2014) inequality-growth channel.
""",

    '3_calibration': """
3. CALIBRATION AND DATA

3.1 Social Security Parameters (SSA 2024)
    - Total beneficiaries: 67 million
    - Average retired worker benefit: $1,907/month
    - Total annual outlays: $1.4 trillion
    - Total annual revenue: $1.2 trillion
    - Projected depletion year: 2034
    - FICA rate: 12.4% (combined employee + employer)
    - Earnings cap (2024): $168,600

3.2 Billionaire Wealth Data (Forbes 2024, ATF 2025, IPS 2025)
    - Total US billionaires: 935
    - Combined wealth: $8.2 trillion
    - Tier distribution: [Table 1 in paper]
    - Annual wealth growth rates: 6-12% by tier
    - Unrealized gains: ~56% of total wealth

3.3 Income Distribution (Census CPS ASEC 2023)
    - 22-point CDF of working-age individual income
    - 37% below $2,200/month living wage threshold
    - Real wage growth: ~0.4%/year (shrinks eligible fraction)

3.4 Financial Market Parameters
    - US equity market cap: $55 trillion
    - Historical real equity return: 5.2% (Dimson et al. 2023)
    - Equity risk premium: 4-5%
    - Risk-free rate (real): 1.5-2%

3.5 Behavioral Parameters
    [Table 2: Five behavioral regimes with all calibration parameters]
""",

    '4_results': """
4. RESULTS

4.1 Baseline Projections

Under the Realistic Central behavioral regime (81% collection
efficiency) and moderate economic assumptions:

    - Year 0 Tier 2 benefit: $249/month per eligible adult
    - Year 10: $398/month
    - Year 30: $1,731/month
    - Retiree total (SS + Tier 2 + Tier 3) at Year 30: $5,185/month
    - Equity fund balance at Year 30: $7.8 trillion
    - 30-year cumulative benefit per person: $228,332

4.2 Robustness Across Behavioral Regimes

[Table 3: Tier 2 benefit at Years 5, 10, 20, 30 across all 5 regimes]

Key finding: The benefit range across all regimes is $142-$246B in
Year 0 revenue, translating to Tier 2 monthly benefits of $170-$300.
The system is viable under ALL behavioral assumptions because the FICA
component is independent of billionaire behavior.

4.3 Optimal Tax Rate

At the central elasticity estimates, the welfare-maximizing billionaire
income tax rate is 38-42%, depending on the social discount rate. At
higher avoidance elasticities (pessimistic regime), the optimum shifts
to 30-35%. The Laffer-curve revenue peak is at approximately 55-65%
across regimes — well above our proposed rate.

4.4 Distributional Impact

Income Gini (Lerman-Yitzhaki decomposition):
    Current:  0.390
    Year 5:   0.378
    Year 10:  0.373
    Year 30:  0.321

Wealth Gini (top-end compression + bottom-end accumulation):
    Current:  0.860
    Year 30:  0.843

The asymmetry — large income Gini reduction vs. small wealth Gini
reduction — arises because transfers are consumed (MPC ~0.90), not
saved. The system is an income redistribution mechanism, not a wealth
redistribution mechanism.

4.5 GDP and Labor Market Effects

Net GDP effect: +1.5% (Year 5) to +5.3% (Year 30)

The consumption multiplier (+8.1% at Year 30) dominates the labor
supply reduction (-3.5%), with an additional inequality-growth bonus
(+0.2%/year) from the IMF channel. The net effect is positive and
growing because benefit levels increase over time, generating larger
consumption effects.

4.6 Monte Carlo Simulation

10,000 simulated 40-year paths with stochastic equity returns
(GBM with mu = 0.07, sigma = 0.16), stochastic wage growth, and
parameter uncertainty:

    - Positive fund balance at Year 40: 97.3% of scenarios
    - Tier 2 benefit > $500/month at Year 30: 89.1%
    - Tier 2 benefit > $1,000/month at Year 30: 72.4%
    - System insolvency (fund depleted + revenue shortfall): 0.0%
      (by construction — revenue-constrained design prevents insolvency)
""",

    '5_robustness': """
5. ROBUSTNESS CHECKS

5.1 Without the Billionaire Income Tax

If the M2M tax is struck down or never implemented, the FICA reform
alone generates:
    - Year 0 Tier 2: $198/month (targeted) or $106/month (universal)
    - Year 30 Tier 2: $798/month (targeted) or $442/month (universal)
    - Equity fund at Year 30: ~$3.5 trillion

The system remains viable but slower. This is the "engine-only"
scenario.

5.2 Pessimistic Behavioral Response

Under the most pessimistic calibration (50% avoidance ceiling, 5%
evasion, high emigration), billionaire tax revenue falls to $142B/year
(Year 0) vs. $210B (central). Year 30 Tier 2 benefit falls from
$1,731 to approximately $1,200/month. The system still provides
meaningful income support.

5.3 Low Equity Returns (4% real vs. 5.5% central)

With lower fund returns, the Tier 3 dividend is smaller, but Tier 2
(funded from current revenue) is unaffected. Year 30 total benefit
falls from $1,731 to approximately $1,650/month.

5.4 Constitutional Risk Scenario

If M2M is struck down at Year 5 and replaced with a minimum tax
(60% of M2M revenue), the Year 30 Tier 2 benefit falls to
approximately $1,350/month. System remains solvent.

5.5 Labor Supply Sensitivity

At the upper bound of labor supply elasticity estimates (4% employment
reduction), the GDP effect is still positive (+2.1% at Year 30) due
to the dominant consumption multiplier.
""",

    '6_conclusion': """
6. CONCLUSION

We have shown that a three-component reform to the Social Security
system — FICA restructuring, revenue-constrained Tier 2 benefits, and
a mark-to-market billionaire income tax — can simultaneously solve the
OASDI solvency crisis, provide meaningful income support to 138 million
American adults, and reduce the U.S. income Gini by 18%, all without
deficit spending.

The key design innovation is revenue-constraint: unlike Social
Security's current defined-benefit structure, this system makes no
promises beyond its revenue capacity. Benefits are a function of
collections, not legislative promise. This eliminates the solvency
risk that plagues the current system.

The billionaire income tax, while politically salient, is analytically
secondary. FICA reform alone funds the system. The billionaire tax
accelerates it. This separation of engine and accelerant provides
political flexibility: the proposal can be implemented in stages,
with FICA reform first and the billionaire component added when
politically feasible.

We note important limitations. The behavioral response to billionaire
taxation is inherently uncertain; our five-regime approach bounds this
uncertainty but does not eliminate it. The constitutional viability of
mark-to-market taxation remains unresolved after Moore v. United States
(2024). The Gini decomposition is an approximation; a full
microsimulation using tax return data would be more precise. And the
long-horizon projections (30-40 years) compound modeling uncertainties
that short-horizon analysis does not.

Nevertheless, the fundamental finding is robust: there exists a
self-funding mechanism to extend Social Security-style income security
to the majority of American adults. The question is not whether it is
economically feasible, but whether it is politically achievable.
""",

    '7_references': """
REFERENCES

Atkinson, Anthony B. (2015). "Inequality: What Can Be Done?" Cambridge, MA: Harvard University Press.

Bernstein, Jared (2017). "The U.S. Needs a Sovereign Wealth Fund." Washington Post, January 20, 2017.

Brulhart, Marius, Jonathan Gruber, Matthias Krapf, and Kurt Schmidheiny (2022). "Behavioral Responses to Wealth Taxes: Evidence from Switzerland." American Economic Journal: Economic Policy, 14(4): 111-150.

Cesarini, David, Erik Lindqvist, Matthew J. Notowidigdo, and Robert Ostling (2017). "The Effect of Wealth on Individual and Household Labor Supply: Evidence from Swedish Lotteries." American Economic Review, 107(12): 3917-3946.

Congressional Budget Office (2020). "Estimated Macroeconomic Effects of Spending and Revenue Options." Washington, DC: CBO.

Congressional Budget Office (2024). "CBO's Long-Term Projections for Social Security: 2024." Washington, DC: CBO.

Diamond, Peter A. and Peter R. Orszag (2004). "Saving Social Security: A Balanced Approach." Washington, DC: Brookings Institution Press.

Dimson, Elroy, Paul Marsh, and Mike Staunton (2023). "Credit Suisse Global Investment Returns Yearbook 2023." Zurich: Credit Suisse Research Institute.

Dybvig, Philip H. (1995). "Duesenberry's Ratcheting of Consumption: Optimal Dynamic Consumption and Investment Given Intolerance for Any Decline in Standard of Living." Review of Economic Studies, 62(2): 287-313.

Eisinger, Jesse, Jeff Ernsthausen, and Paul Kiel (2021). "The Secret IRS Files: Trove of Never-Before-Seen Records Reveal How the Wealthiest Avoid Income Tax." ProPublica, June 8, 2021.

Forbes (2024). "The Forbes 400: The Definitive Ranking of the Wealthiest Americans." Forbes Media LLC.

Gabaix, Xavier and Ralph Koijen (2022). "In Search of the Origins of Financial Fluctuations: The Inelastic Markets Hypothesis." NBER Working Paper No. 28967.

Glasmeier, Amy K. (2024). "Living Wage Calculator." Massachusetts Institute of Technology. https://livingwage.mit.edu/

Goss, Stephen C. (2010). "The Future Financial Status of the Social Security Program." Social Security Bulletin, 70(3): 111-125.

Hamalainen, Kari et al. (2020). "The Basic Income Experiment 2017-2018 in Finland: Preliminary Results." Ministry of Social Affairs and Health, Finland.

Hoynes, Hilary and Jesse Rothstein (2019). "Universal Basic Income in the United States and Advanced Countries." Annual Review of Economics, 11: 929-958.

Institute for Policy Studies (2025). "Billionaire Bonanza: The Centi-Billionaire Report." Washington, DC.

Jappelli, Tullio and Luigi Pistaferri (2010). "The Consumption Response to Income Changes." Annual Review of Economics, 2: 479-506.

Kanbur, Ravi, Michael Keen, and Matti Tuomala (1994). "Optimal Nonlinear Income Taxation for the Alleviation of Income-Poverty." European Economic Review, 38(8): 1613-1632.

Kyle, Albert S. (1985). "Continuous Auctions and Insider Trading." Econometrica, 53(6): 1315-1335.

Lerman, Robert I. and Shlomo Yitzhaki (1985). "Income Inequality Effects by Income Source: A New Approach and Applications to the United States." Review of Economics and Statistics, 67(1): 151-156.

Marinescu, Ioana (2018). "No Strings Attached: The Behavioral Effects of U.S. Unconditional Cash Transfer Programs." NBER Working Paper No. 24337.

Moffitt, Robert A. (2002). "The Temporary Assistance for Needy Families Program." In Robert A. Moffitt (ed.), Means-Tested Transfer Programs in the United States. Chicago: University of Chicago Press.

Moore v. United States, 602 U.S. ___ (2024). Supreme Court of the United States.

Norges Bank Investment Management (2024). "Government Pension Fund Global: Annual Report 2023." Oslo, Norway.

OECD (2015). "In It Together: Why Less Inequality Benefits All." Paris: OECD Publishing.

Ostry, Jonathan D., Andrew Berg, and Charalambos G. Tsangarides (2014). "Redistribution, Inequality, and Growth." IMF Staff Discussion Note SDN/14/02. Washington, DC: International Monetary Fund.

Piketty, Thomas, Emmanuel Saez, and Stefanie Stantcheva (2014). "Optimal Taxation of Top Labor Incomes: A Tale of Three Elasticities." American Economic Journal: Economic Policy, 6(1): 230-271.

Saez, Emmanuel and Gabriel Zucman (2019). "The Triumph of Injustice: How the Rich Dodge Taxes and How to Make Them Pay." New York: W.W. Norton.

Saez, Emmanuel and Gabriel Zucman (2021). "A Progressive Tax on Billionaire Wealth." UC Berkeley Working Paper.

Scheuer, Florian and Joel Slemrod (2021). "Taxing Our Wealth." Journal of Economic Perspectives, 35(1): 207-230.

Social Security Administration (2024). "The 2024 Annual Report of the Board of Trustees of the Federal Old-Age and Survivors Insurance and Federal Disability Insurance Trust Funds." Washington, DC.

U.S. Census Bureau (2023). "Current Population Survey, Annual Social and Economic Supplement (CPS ASEC)." Washington, DC.

U.S. Department of the Treasury (2024). "General Explanations of the Administration's Fiscal Year 2025 Revenue Proposals."

Wyden, Ron (2021). "Billionaires Income Tax." U.S. Senate Committee on Finance.

Alaska Permanent Fund Corporation (2024). "Annual Report." Juneau, AK.

Americans for Tax Fairness (2025). "Billionaire Wealth Tracker." Washington, DC.
""",
}

JOURNAL_TARGET_NOTES = """
TARGET JOURNALS (in order of preference):

1. American Economic Review (AER)
   - Impact factor: ~12.0
   - Submission format: AER manuscript guidelines, online appendix
   - Strengths: comprehensive model, distributional analysis
   - Weaknesses: may view as too policy-focused for AER

2. Quarterly Journal of Economics (QJE)
   - Impact factor: ~15.0
   - Strengths: novel revenue-constraint mechanism, Gini analysis
   - Weaknesses: no natural experiment or quasi-experimental variation

3. Journal of Political Economy (JPE)
   - Impact factor: ~10.0
   - Strengths: general equilibrium analysis, welfare computation
   - Weaknesses: calibration-based (vs. estimation-based)

4. Journal of Public Economics
   - Impact factor: ~4.5
   - Best fit: tax policy, redistribution, Social Security reform
   - Likely most receptive given topic alignment

5. Brookings Papers on Economic Activity
   - Policy-oriented, peer-reviewed
   - Strong fit for the policy relevance angle
   - Invitational (would need to be submitted to editors)

6. National Tax Journal
   - Specialized in tax policy
   - Good fit for the M2M taxation component

7. Tax Policy and the Economy (NBER)
   - Annual volume, invited contributions
   - Good fit for working paper version
"""


if __name__ == '__main__':
    print("=" * 70)
    print("  LEVEL 6C: WORKING PAPER (NBER-STYLE)")
    print("=" * 70)
    print(f"\n  Title: {WORKING_PAPER_METADATA['title']}")
    print(f"  JEL Codes: {', '.join(WORKING_PAPER_METADATA['jel_codes'])}")
    print(f"  Keywords: {', '.join(WORKING_PAPER_METADATA['keywords'][:5])}...")
    print()
    print(ABSTRACT)
    print("\n  SECTIONS:")
    for key, content in SECTIONS.items():
        word_count = len(content.split())
        section_title = content.strip().split('\n')[0]
        print(f"    {section_title:<60} ({word_count:,} words)")
    total_words = sum(len(v.split()) for v in SECTIONS.values()) + len(ABSTRACT.split())
    print(f"\n  Total estimated words (outline + key sections): {total_words:,}")
    print(f"  Full paper target: 25,000 words")
    print(JOURNAL_TARGET_NOTES)
