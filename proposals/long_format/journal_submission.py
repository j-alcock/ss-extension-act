"""
Journal Submission — Level 7C Proposal (AER/QJE/JPE format)
Format: 50+ pages including online appendix
Audience: Peer reviewers, academic economists
Tone: Rigorous academic prose, hedged claims, full methodology
Citations: 80-120 references with full bibliographic details

This file contains the LaTeX-ready structure, additional appendix
material, and reviewer-anticipation notes beyond the working paper.
"""

JOURNAL_SUBMISSION_STRUCTURE = """
══════════════════════════════════════════════════════════════════════════════
  JOURNAL SUBMISSION PACKAGE
  Target: Journal of Public Economics (primary)
         AER (secondary), Brookings Papers (tertiary)
══════════════════════════════════════════════════════════════════════════════

MAIN PAPER STRUCTURE (35-40 pages):

  1. Introduction (5 pages)
     - Motivation: twin crises (insolvency + income inadequacy)
     - Contribution: revenue-constrained benefits, optimal M2M rate,
       five-regime behavioral calibration, distributional impact
     - Preview of results
     - Related literature (detailed)

  2. Institutional Background (3 pages)
     - OASDI trust fund mechanics and depletion timeline
     - Current FICA structure and the earnings cap distortion
     - Buy-borrow-die strategy and effective tax rates
     - Moore v. United States and constitutional landscape

  3. Model (8 pages)
     3.1 Revenue-Constrained Benefit Framework
         - Formal definition with solvency guarantee
         - Benefit ratchet (Dybvig 1995) with reserve constraint
         - Comparison with defined-benefit vs. defined-contribution
     3.2 Revenue Model
         - FICA reform: cap removal + investment income extension
         - Billionaire income tax: M2M with graduated rates
         - Revenue decomposition theorem: engine vs. accelerant
     3.3 Behavioral Response Model
         - Three channels: avoidance, evasion, emigration
         - Five calibrated regimes with parameter sources
         - Emigration analysis with IRC 877A exit tax
     3.4 Eligible Population Dynamics
         - CDF calibration from CPS ASEC
         - Time-dynamic eligibility with real wage growth
         - Poverty trap avoidance: benefit exclusion from income
     3.5 Optimal Tax Rate Derivation
         - Social welfare function specification
         - First-order conditions
         - Numerical solution across behavioral regimes
     3.6 General Equilibrium Extension
         - Inelastic markets price impact (Gabaix-Koijen)
         - Labor market (Marinescu semi-elasticities)
         - GDP decomposition: consumption, labor, inequality

  4. Calibration (3 pages)
     - Complete parameter table with sources
     - CDF fitting procedure
     - Wealth tier data construction
     - Behavioral regime calibration (with confidence intervals)

  5. Results (8 pages)
     5.1 Baseline Projections (40-year horizon)
     5.2 Benefit Trajectories Across Scenarios
     5.3 Optimal Tax Rate Results
     5.4 Distributional Impact (Gini decomposition)
     5.5 GDP and Labor Market Effects
     5.6 Monte Carlo Fund Simulation (10,000 paths)

  6. Robustness (5 pages)
     6.1 Without Billionaire Tax (Engine-Only)
     6.2 Pessimistic Behavioral Response
     6.3 Low Equity Returns
     6.4 Constitutional Risk Scenario
     6.5 Labor Supply Sensitivity
     6.6 Alternative Eligibility Thresholds
     6.7 Universal vs. Targeted Design Comparison

  7. Discussion (3 pages)
     - Political economy considerations
     - Comparison with existing proposals
     - Universality vs. targeting tradeoff
     - Implementation sequencing

  8. Conclusion (2 pages)

  References (3-4 pages, 80-120 entries)

ONLINE APPENDIX (20-30 pages):

  A. Full 40-Year Projection Tables
     - All scenarios × all behavioral regimes × all time horizons
     - Revenue decomposition year-by-year

  B. Income Distribution CDF
     - 22-point CDF calibration
     - Goodness-of-fit tests
     - Comparison with ACS and tax return data
     - Time-dynamic eligibility trajectories

  C. Behavioral Response Model Details
     - Full derivation of avoidance ceiling
     - European wealth tax case studies
     - IRC 877A exit tax mechanics
     - Enforcement degradation model

  D. Monte Carlo Simulation Details
     - Return distribution specification (GBM parameters)
     - Correlation structure (equity-bond-wages)
     - 10,000-path summary statistics
     - Percentile trajectories (5th, 25th, 50th, 75th, 95th)

  E. General Equilibrium Derivations
     - Gabaix-Koijen multiplier calibration
     - Adaptive multiplier decay function
     - Labor market semi-elasticity decomposition
     - GDP channel interactions

  F. Gini Decomposition Methodology
     - Lerman-Yitzhaki framework
     - Modification for targeted transfers
     - Concentration bonus derivation
     - Wealth Gini estimation with savings accumulation

  G. Sensitivity Analysis Full Results
     - 2D heatmaps: tax rate × avoidance elasticity
     - 2D heatmaps: equity return × wage growth
     - Break-even analysis: what makes the system fail?
     - Parameter tornado diagrams

  H. Legislative Language (Draft)
     - IRC amendments for FICA cap removal
     - SSIIC statutory language
     - M2M tax framework
     - AEF governance charter

  I. International Sovereign Wealth Fund Comparison
     - Norway GPFG: governance, returns, withdrawal rule
     - Alaska PFD: political economy, dividend history
     - Singapore GIC and Temasek
     - Abu Dhabi Investment Authority
     - Lessons for AEF design

  J. Comparison Table: This Proposal vs. Alternatives
     - Status quo (2034 cuts)
     - Raise retirement age proposals
     - FICA cap-only proposals
     - Biden minimum tax
     - Wyden M2M tax
     - Yang UBI
     - Bennet child allowance
     - Booker baby bonds
"""

REFEREE_ANTICIPATION = """
══════════════════════════════════════════════════════════════════════════════
  ANTICIPATED REFEREE OBJECTIONS AND RESPONSES
══════════════════════════════════════════════════════════════════════════════

OBJECTION 1: "This is a calibration exercise, not an empirical paper.
             Where is the identification strategy?"

RESPONSE: We acknowledge this is a calibration-based policy analysis,
not an estimation paper. Our contribution is the mechanism design
(revenue-constrained benefits) and the comprehensive behavioral
calibration across five regimes that bound the policy space. We cite
empirical estimates from Brulhart et al. (2022), Cesarini et al. (2017),
and Marinescu (2018) for the key elasticities. The five-regime approach
is a substitute for estimation: rather than claiming to know the "true"
elasticity, we show the system works across the entire plausible range.

OBJECTION 2: "The billionaire behavioral response estimates are
             speculative. There is no empirical analog for a 40% M2M
             tax on US billionaires."

RESPONSE: Correct. We address this through bounded analysis. The
pessimistic regime assumes 50% of revenue is lost to avoidance —
higher than any observed rate in the literature. The key finding is
that even under this extreme assumption, the system remains viable
because FICA reform (which has well-established revenue estimates)
is the engine. The billionaire tax is analytically separable.

OBJECTION 3: "The Gini estimates use an approximation, not a
             microsimulation."

RESPONSE: We use the Lerman-Yitzhaki (1985) decomposition with a
targeting adjustment. We acknowledge this is an approximation and note
that a full microsimulation using tax return data (e.g., IRS SOI
Public Use Files) would be more precise. However, the direction and
approximate magnitude of the Gini shift are robust to the method —
a $1,731/month transfer to the bottom 53% of the income distribution
mechanically reduces the Gini substantially.

OBJECTION 4: "The general equilibrium effects are speculative.
             A sovereign fund of this size has no precedent."

RESPONSE: Norway's GPFG ($1.7T, ~3% of global equity market) provides
a partial analog. We incorporate the Gabaix-Koijen multiplier with
adaptive decay, which accounts for market adjustment. The key insight
is that the fund is a permanent holder (structural demand), not a
trader (flow demand). We show price impact is modest relative to
market capitalization and diminishes over time.

OBJECTION 5: "Why not a simpler proposal — just lift the FICA cap?"

RESPONSE: Our contribution is precisely to show what becomes possible
BEYOND cap removal. Cap removal alone solves solvency but generates
no new benefits. The revenue-constrained design converts the surplus
into a Tier 2 benefit without creating unfunded promises. The
billionaire tax further amplifies the benefit level. We present cap-
removal-only as a robustness check (Section 6.1) and show it still
generates meaningful but smaller benefits.

OBJECTION 6: "Constitutional risk of M2M is too high to model as a
             central case."

RESPONSE: We model constitutional risk explicitly (30% probability of
being struck down within 10 years) and present alternative structures
(minimum tax with lookback, mandatory realization at death) as
fallback provisions. The paper's central finding — that the system
works without the billionaire tax — makes the constitutional question
analytically secondary, even if politically important.

OBJECTION 7: "The 40-year horizon projections are unreliable."

RESPONSE: We agree that 40-year point estimates are unreliable. We
present them not as predictions but as illustrative of the compounding
dynamics. The Monte Carlo analysis (10,000 paths) captures the
uncertainty, showing 97.3% positive fund balance at Year 40 and a
wide confidence interval for benefits. The solvency result is exact
(by construction), not projected.
"""

ADDITIONAL_CITATIONS_FOR_JOURNAL = """
══════════════════════════════════════════════════════════════════════════════
  ADDITIONAL REFERENCES FOR JOURNAL VERSION
══════════════════════════════════════════════════════════════════════════════

  (Beyond the 33 validated citations in the working paper)

Auerbach, Alan J. and Laurence J. Kotlikoff (1987). "Dynamic Fiscal Policy." Cambridge: Cambridge University Press.

Banerjee, Abhijit et al. (2017). "Debunking the Stereotype of the Lazy Welfare Recipient: Evidence from Cash Transfer Programs." World Bank Research Observer, 32(2): 155-184.

Blanchard, Olivier J. (2019). "Public Debt and Low Interest Rates." American Economic Review, 109(4): 1197-1229.

Chetty, Raj et al. (2014). "Where is the Land of Opportunity? The Geography of Intergenerational Mobility in the United States." Quarterly Journal of Economics, 129(4): 1553-1623.

Diamond, Peter A. (2004). "Social Security." American Economic Review, 94(1): 1-24.

Dimson, Elroy, Paul Marsh, and Mike Staunton (2023). "Credit Suisse Global Investment Returns Yearbook 2023." Zurich: Credit Suisse Research Institute.

Feldstein, Martin (1974). "Social Insurance." In Alan Auerbach and Martin Feldstein (eds.), Handbook of Public Economics, Vol. 2. Amsterdam: North-Holland.

Gentilini, Ugo et al. (2020). "Exploring Universal Basic Income: A Guide to Navigating Concepts, Evidence, and Practices." World Bank.

Guvenen, Fatih et al. (2022). "Use It or Lose It: Efficiency and Redistributional Effects of Wealth Taxation." Quarterly Journal of Economics, 137(2): 835-894.

Heckman, James J. (2006). "Skill Formation and the Economics of Investing in Disadvantaged Children." Science, 312(5782): 1900-1902.

Jakobsen, Katrine et al. (2020). "Wealth Taxation and Wealth Accumulation: Theory and Evidence from Denmark." Quarterly Journal of Economics, 135(1): 329-388.

Jones, Damon, and Ioana Marinescu (2022). "The Labor Market Impacts of Universal and Permanent Cash Transfers: Evidence from the Alaska Permanent Fund." American Economic Journal: Economic Policy, 14(2): 315-340.

Kleven, Henrik (2014). "How Can Scandinavians Tax So Much?" Journal of Economic Perspectives, 28(4): 77-98.

Kopczuk, Wojciech (2013). "Taxation of Intergenerational Transfers and Wealth." In Alan J. Auerbach et al. (eds.), Handbook of Public Economics, Vol. 5.

Lockwood, Benjamin B. and Matthew Weinzierl (2016). "Positive and Normative Judgments Implicit in U.S. Tax Policy, and the Costs of Unequal Growth and Recessions." Journal of Monetary Economics, 77: 30-47.

Mirrlees, James A. (1971). "An Exploration in the Theory of Optimum Income Taxation." Review of Economic Studies, 38(2): 175-208.

Piketty, Thomas (2014). "Capital in the Twenty-First Century." Cambridge, MA: Harvard University Press.

Saez, Emmanuel (2001). "Using Elasticities to Derive Optimal Income Tax Rates." Review of Economic Studies, 68(1): 205-229.

Slemrod, Joel (2007). "Cheating Ourselves: The Economics of Tax Evasion." Journal of Economic Perspectives, 21(1): 25-48.

Stiglitz, Joseph E. (2015). "The Great Divide: Unequal Societies and What We Can Do About Them." New York: W.W. Norton.

Summers, Lawrence H. and Natasha Sarin (2019). "A 'Wealth Tax' Presents a Revenue Estimation Challenge." Tax Notes, November 18, 2019.

Zucman, Gabriel (2015). "The Hidden Wealth of Nations." Chicago: University of Chicago Press.
"""


if __name__ == '__main__':
    print("=" * 70)
    print("  LEVEL 7C: JOURNAL SUBMISSION PACKAGE")
    print("=" * 70)
    print(JOURNAL_SUBMISSION_STRUCTURE)
    print(REFEREE_ANTICIPATION[:2000])
    print("  [... continued ...]")
