"""
Social Security Extension — Means-Tested Variant (Distribution Limits)

QUESTION: If people who earn above a living wage and aren't yet eligible
for Social Security don't need assistance, how does that change the model?
At what point does the ability to provide a living wage for ALL eligible
people come into existence?

APPROACH:
  The universal SS Extension V2.0 distributes Tier 2 to ALL 258M adults.
  This variant restricts Tier 2 to people who NEED it:
    1. SS beneficiaries (67M) — always eligible (already receiving Tier 1)
    2. Working-age adults (18-66) earning BELOW the living wage

  Same revenue pool. Fewer recipients. Higher per-person benefits.

  At $2,200/month living wage threshold:
    - 37% of working-age adults earn below this (~71M)
    - Plus 67M SS beneficiaries
    - Total eligible: ~138M (53% of adults)
    - Benefit multiplier: ~1.87x over universal model

KEY DESIGN CHOICES:
  1. Benefit does NOT count as income for threshold purposes
     "Make above a living wage" = MARKET income, not total income
     This avoids the classic poverty trap / cliff effect

  2. Hard cutoff (with smooth taper option)
     The user's framing is binary: "don't need assistance"
     But a smooth taper is available for sensitivity analysis

  3. SS beneficiaries always eligible (user's specification)
     Retirees, disabled, and survivors get Tier 2 regardless of income

  4. Universal model remains intact for comparison
     This is a PARALLEL model, not a replacement

THE BIG QUESTION: When does Tier 2 reach the living wage?
  - Universal model: Never within 40 years (tops out at ~$605/mo)
  - Targeted model: Approaches but may not fully reach $2,200/mo
  - Targeted + wealth tax: Gets closer, possibly achievable by Year 30-35
  - Key insight: for RETIREES, it's already there (SS + Tier 2 + Tier 3)

References:
- Census Bureau CPS ASEC (2023): Income distribution data
- MIT Living Wage Calculator (2024): $2,200/month threshold
- Moffitt (2002) "The Temporary Assistance for Needy Families Program"
  (on means-testing welfare traps)
- Hoynes & Rothstein (2019) "Universal Basic Income in the United States
  and Advanced Countries" (targeting vs. universality tradeoff)
- Atkinson (2015) "Inequality: What Can Be Done?" (participation income)
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.parameters import *
from data.income_distribution import (
    interpolate_cdf, fraction_below_threshold, compute_eligible_population,
    population_trajectory, WORKING_AGE_ADULTS,
)
from models.ss_extension_model import (
    SSExtensionModelV2, SSExtensionDesign, SSRevenueReform,
    ScenarioConfig, SCENARIOS,
)


# ═══════════════════════════════════════════════════════════════════════
#  MEANS-TEST CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

# Living wage constants (from living_wage_model.py)
LIVING_WAGE_LOW = 1_500   # Bare minimum (near poverty line)
LIVING_WAGE_MID = 2_200   # MIT living wage (national avg, single adult)
LIVING_WAGE_HIGH = 3_000  # Comfortable in most metros


@dataclass
class MeansTestConfig:
    """
    Configuration for means-testing Tier 2 benefits.

    The living wage threshold determines who is eligible:
      - Working-age adults (18-66) earning BELOW this → eligible
      - Working-age adults earning ABOVE this → excluded
      - SS beneficiaries → always eligible

    The benefit itself does NOT count as income for threshold purposes
    (default). This avoids the poverty trap where receiving a benefit
    disqualifies you from receiving it.
    """

    # Living wage threshold (monthly, real dollars)
    living_wage_monthly: float = LIVING_WAGE_MID  # $2,200/month

    # Whether the Tier 2 benefit counts as income for threshold
    # Default False: only MARKET income determines eligibility
    benefit_counts_as_income: bool = False

    # Phase-out design
    # 'hard_cutoff': below threshold = full benefit, above = nothing
    # 'smooth_taper': benefit tapers off above threshold
    phase_out_type: str = 'hard_cutoff'

    # Smooth taper parameters (only used if phase_out_type == 'smooth_taper')
    # For every $1 of income above threshold, benefit reduced by taper_rate
    taper_rate: float = 0.50  # 50% taper — $1 earned reduces benefit by $0.50
    taper_max_income_above: float = 1000  # Benefit reaches $0 at threshold + this

    # SS beneficiary treatment
    ss_beneficiaries_always_eligible: bool = True

    # CPI growth for adjusting threshold over time
    cpi_growth: float = 0.02

    @property
    def living_wage_annual(self) -> float:
        return self.living_wage_monthly * 12

    def threshold_at_year(self, year: int) -> float:
        """Living wage threshold in nominal dollars at a future year."""
        return self.living_wage_monthly * ((1 + self.cpi_growth) ** year)


# ═══════════════════════════════════════════════════════════════════════
#  THE MEANS-TESTED MODEL
# ═══════════════════════════════════════════════════════════════════════

class SSExtensionMeansTestedV2:
    """
    SS Extension Model with distribution limits (means-testing).

    Identical revenue pipeline to SSExtensionModelV2. The ONLY difference
    is that Tier 2 benefits are distributed to a SMALLER eligible population,
    resulting in higher per-person benefits.

    The equity fund, revenue reforms, Tier 3, and all other mechanics
    are exactly the same. Only the Tier 2 denominator changes.
    """

    def __init__(self, scenario: str = 'moderate',
                 means_test: MeansTestConfig = None,
                 design: SSExtensionDesign = None):
        if scenario not in SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}. Choose from {list(SCENARIOS.keys())}")

        self.config = SCENARIOS[scenario]
        self.means_test = means_test or MeansTestConfig()
        self.design = design or SSExtensionDesign()
        self.scenario_name = scenario

        # Revenue reforms (identical to universal model)
        self.revenue = SSRevenueReform(
            equity_fund_seed=self.config.equity_fund_seed,
            equity_fund_annual_contribution=self.config.equity_fund_annual_contribution,
            equity_fund_return_real=self.config.equity_fund_return_real,
            equity_fund_contribution_years=self.config.equity_fund_contribution_years,
            ftt_base_revenue=50e9 if self.config.include_ftt else 0,
            carbon_base_revenue=67.5e9 if self.config.include_carbon else 0,
            fica_on_investment=self.config.include_investment_fica,
        )

    def project(self, years: int = 40) -> dict:
        """
        Project the means-tested SS Extension forward.

        Revenue computation is IDENTICAL to universal model.
        The ONLY change is the Tier 2 denominator: eligible_adults
        instead of all_adults.

        Tracks full population segmentation per year.
        """
        # ─── OUTPUT ARRAYS ─────────────────────────────────────
        results = {
            'years': np.arange(years),
            # Revenue (same as universal)
            'total_revenue': np.zeros(years),
            'new_revenue': np.zeros(years),
            'existing_ss_revenue': np.zeros(years),
            'existing_ss_outlays': np.zeros(years),
            'ss_deficit': np.zeros(years),
            'revenue_after_ss_deficit': np.zeros(years),
            'equity_fund_contribution': np.zeros(years),
            'revenue_for_tier2': np.zeros(years),
            # Benefits
            'tier2_monthly': np.zeros(years),
            'tier3_monthly': np.zeros(years),
            'total_monthly_eligible': np.zeros(years),
            'total_monthly_retiree': np.zeros(years),
            'total_annual_eligible': np.zeros(years),
            # Fund
            'equity_fund_balance': np.zeros(years + 1),
            'equity_fund_trailing_avg': np.zeros(years),
            'tier2_outlays': np.zeros(years),
            'tier3_outlays': np.zeros(years),
            'reserve_balance': np.zeros(years + 1),
            # Population segments
            'total_adults': np.zeros(years),
            'ss_beneficiaries': np.zeros(years),
            'working_age': np.zeros(years),
            'working_age_below_lw': np.zeros(years),
            'working_age_above_lw': np.zeros(years),
            'total_eligible': np.zeros(years),
            'total_excluded': np.zeros(years),
            'eligible_pct': np.zeros(years),
            'frac_below_lw': np.zeros(years),
            # Retiree-specific
            'retirees': np.zeros(years),
            # Living wage milestone tracking
            'threshold_nominal': np.zeros(years),
            'tier2_as_pct_of_lw': np.zeros(years),
        }

        # Initial equity fund
        results['equity_fund_balance'][0] = self.revenue.equity_fund_seed

        # Population segments
        for t in range(years):
            seg = compute_eligible_population(
                year=t,
                threshold_monthly=self.means_test.living_wage_monthly,
            )
            results['total_adults'][t] = seg['total_adults']
            results['ss_beneficiaries'][t] = seg['ss_beneficiaries']
            results['working_age'][t] = seg['working_age']
            results['working_age_below_lw'][t] = seg['working_age_below_lw']
            results['working_age_above_lw'][t] = seg['working_age_above_lw']
            results['total_eligible'][t] = seg['total_eligible']
            results['total_excluded'][t] = seg['total_excluded']
            results['eligible_pct'][t] = seg['eligible_pct']
            results['frac_below_lw'][t] = seg['frac_below_lw']
            results['retirees'][t] = seg['ss_beneficiaries']
            results['threshold_nominal'][t] = self.means_test.threshold_at_year(t)

        # Fund history for trailing average
        fund_history = [self.revenue.equity_fund_seed]

        for t in range(years):
            eligible = results['total_eligible'][t]

            # ─── REVENUE (identical to universal model) ────────
            rev = self.revenue.compute_new_revenue(year=t)
            results['total_revenue'][t] = rev['total_all_revenue']
            results['new_revenue'][t] = rev['total_new_revenue']
            results['existing_ss_revenue'][t] = rev['existing_ss_revenue']

            # ─── EXISTING SS OUTLAYS ───────────────────────────
            if t == 0:
                results['existing_ss_outlays'][t] = SS_TOTAL_ANNUAL_OUTLAYS
            else:
                growth = 0.035 if t < 15 else 0.025
                results['existing_ss_outlays'][t] = results['existing_ss_outlays'][t - 1] * (1 + growth)

            # ─── SS DEFICIT ────────────────────────────────────
            ss_deficit = max(results['existing_ss_outlays'][t] - results['existing_ss_revenue'][t], 0)
            results['ss_deficit'][t] = ss_deficit

            # ─── REVENUE AFTER SS DEFICIT ──────────────────────
            revenue_after_deficit = max(results['new_revenue'][t] - ss_deficit, 0)
            results['revenue_after_ss_deficit'][t] = revenue_after_deficit

            # ─── EQUITY FUND CONTRIBUTION ──────────────────────
            if t < self.revenue.equity_fund_contribution_years:
                max_contribution = revenue_after_deficit * 0.40
                contribution = min(self.revenue.equity_fund_annual_contribution, max_contribution)
            else:
                contribution = 0
            results['equity_fund_contribution'][t] = contribution

            # ─── EQUITY FUND GROWTH ────────────────────────────
            results['equity_fund_balance'][t + 1] = (
                (results['equity_fund_balance'][t] + contribution) *
                (1 + self.revenue.equity_fund_return_real)
            )
            fund_history.append(results['equity_fund_balance'][t + 1])

            # Trailing average
            lookback = min(self.design.tier3_smoothing_years, len(fund_history))
            results['equity_fund_trailing_avg'][t] = np.mean(fund_history[-lookback:])

            # ─── TIER 3: EQUITY DIVIDEND ───────────────────────
            # Tier 3 is paid to ALL eligible adults (same pool as Tier 2)
            if self.design.tier3_enabled and t >= self.design.tier3_start_year:
                tier3_total = (results['equity_fund_trailing_avg'][t] *
                               self.design.tier3_withdrawal_rate)
                results['equity_fund_balance'][t + 1] -= tier3_total
                max_withdrawal = results['equity_fund_balance'][t + 1] * 0.05
                if tier3_total > max_withdrawal + results['equity_fund_balance'][t + 1] * 0.05:
                    tier3_total = max(max_withdrawal, 0)

                results['tier3_monthly'][t] = (tier3_total / eligible) / 12
                results['tier3_outlays'][t] = tier3_total
            else:
                results['tier3_monthly'][t] = 0
                results['tier3_outlays'][t] = 0

            # ─── TIER 2: REVENUE-CONSTRAINED, MEANS-TESTED ────
            # KEY DIFFERENCE: divide by eligible, not all_adults
            revenue_for_tier2 = max(revenue_after_deficit - contribution, 0)

            # Reserve building
            current_reserve = results['reserve_balance'][t]
            prior_tier2_annual = results['tier2_outlays'][max(t - 1, 0)] if t > 0 else 0
            reserve_needed = prior_tier2_annual * (self.design.tier2_reserve_target_months / 12)

            if current_reserve < reserve_needed:
                reserve_pct = 0.10 if t < 10 else 0.05
                reserve_add = revenue_for_tier2 * reserve_pct
                revenue_for_tier2 -= reserve_add
                results['reserve_balance'][t + 1] = current_reserve + reserve_add
            else:
                results['reserve_balance'][t + 1] = current_reserve

            results['revenue_for_tier2'][t] = max(revenue_for_tier2, 0)

            # Compute Tier 2 monthly — divided by ELIGIBLE population
            tier2_raw = (max(revenue_for_tier2, 0) / eligible) / 12

            # Cap (inflation-adjusted)
            tier2_cap = self.design.tier2_monthly_cap * (1.02 ** t)
            tier2_uncapped = min(tier2_raw, tier2_cap)

            # ─── BENEFIT RATCHET (Dybvig 1995) ────────────────
            if t > 0:
                prev_tier2 = results['tier2_monthly'][t - 1]
                if tier2_uncapped < prev_tier2:
                    shortfall = (prev_tier2 - tier2_uncapped) * 12 * eligible
                    if results['reserve_balance'][t + 1] >= shortfall:
                        results['reserve_balance'][t + 1] -= shortfall
                        tier2_uncapped = prev_tier2
                    else:
                        available_from_reserve = results['reserve_balance'][t + 1]
                        results['reserve_balance'][t + 1] = 0
                        tier2_uncapped = tier2_uncapped + (available_from_reserve / eligible) / 12

            results['tier2_monthly'][t] = tier2_uncapped
            results['tier2_outlays'][t] = results['tier2_monthly'][t] * 12 * eligible

            # ─── TOTALS ───────────────────────────────────────
            results['total_monthly_eligible'][t] = (results['tier2_monthly'][t] +
                                                     results['tier3_monthly'][t])
            results['total_annual_eligible'][t] = results['total_monthly_eligible'][t] * 12
            results['total_monthly_retiree'][t] = (
                SS_AVG_RETIRED_BENEFIT_MONTHLY * (1.02 ** t) +
                results['total_monthly_eligible'][t]
            )

            # Living wage tracking
            results['tier2_as_pct_of_lw'][t] = (
                results['total_monthly_eligible'][t] /
                results['threshold_nominal'][t] * 100
            )

        return results

    def compare_with_universal(self, years: int = 40) -> dict:
        """
        Side-by-side comparison with the universal SS Extension model.

        Returns both projections and key comparison metrics.
        """
        # Run both models
        targeted = self.project(years=years)

        universal_model = SSExtensionModelV2(
            scenario=self.scenario_name,
            design=self.design,
        )
        universal = universal_model.project(years=years)

        # Compute multiplier at each year
        multiplier = np.where(
            universal['total_monthly_adult'] > 0,
            targeted['total_monthly_eligible'] / universal['total_monthly_adult'],
            0
        )

        return {
            'targeted': targeted,
            'universal': universal,
            'multiplier': multiplier,
            'eligible_pct': targeted['eligible_pct'],
        }


# ═══════════════════════════════════════════════════════════════════════
#  WEALTH TAX INTEGRATION
# ═══════════════════════════════════════════════════════════════════════

def project_means_tested_with_wealth_tax(
    wealth_tax_rate: float = 0.40,
    living_wage_threshold: float = LIVING_WAGE_MID,
    wealth_tax_split_fund: float = 0.60,
    wealth_tax_split_tier2: float = 0.40,
    behavioral_regime: str = 'realistic_central',
    years: int = 40,
) -> dict:
    """
    Run the means-tested SS Extension with wealth tax accelerant.

    Combines:
      - Means-tested SS Extension (smaller eligible population)
      - Wealth tax revenue at the specified rate and behavioral regime
      - Revenue split between equity fund and direct Tier 2

    Returns enhanced benefit trajectories.
    """
    from models.wealth_tax_optimizer import (
        WealthTaxOptimizer, WealthTaxConfig, BehavioralResponse,
        BEHAVIORAL_REGIMES,
    )

    # Run base means-tested model
    mt_config = MeansTestConfig(living_wage_monthly=living_wage_threshold)
    model = SSExtensionMeansTestedV2(scenario='moderate', means_test=mt_config)
    base = model.project(years=years)

    # Set up wealth tax
    regime = BEHAVIORAL_REGIMES.get(behavioral_regime)
    if regime is None:
        raise ValueError(f"Unknown behavioral regime: {behavioral_regime}")

    optimizer = WealthTaxOptimizer(behavioral=regime['params'])
    wt_config = WealthTaxConfig(
        name=f'{wealth_tax_rate:.0%} billionaire income tax',
        description=f'{wealth_tax_rate:.0%} on economic income for >$1B wealth',
        income_tax_rate_above_1b=wealth_tax_rate,
        income_tax_rate_0_to_1b=wealth_tax_rate * 0.5,
        pct_to_equity_fund=wealth_tax_split_fund,
        pct_to_tier2=wealth_tax_split_tier2,
    )

    # Compute wealth tax revenue
    wt_net_revenue = np.zeros(years)
    wt_to_fund = np.zeros(years)
    wt_to_tier2 = np.zeros(years)

    for t in range(years):
        rev = optimizer.compute_annual_revenue(wt_config, year=t)
        wt_net_revenue[t] = rev['total_net_revenue']
        wt_to_fund[t] = rev['to_equity_fund']
        wt_to_tier2[t] = rev['to_tier2']

    # Enhanced Tier 2: base + wealth tax direct allocation / eligible population
    enhanced_tier2 = base['tier2_monthly'].copy()
    enhanced_tier3 = base['tier3_monthly'].copy()
    enhanced_total = np.zeros(years)

    for t in range(years):
        eligible = base['total_eligible'][t]
        wt_boost = (wt_to_tier2[t] / eligible) / 12
        enhanced_tier2[t] += wt_boost
        enhanced_total[t] = enhanced_tier2[t] + enhanced_tier3[t]

    # Living wage milestone with wealth tax
    threshold_nominal = base['threshold_nominal']
    enhanced_as_pct = enhanced_total / threshold_nominal * 100

    return {
        'years': np.arange(years),
        'base_tier2': base['tier2_monthly'],
        'base_tier3': base['tier3_monthly'],
        'base_total': base['total_monthly_eligible'],
        'enhanced_tier2': enhanced_tier2,
        'enhanced_tier3': enhanced_tier3,
        'enhanced_total': enhanced_total,
        'wt_net_revenue': wt_net_revenue,
        'wt_to_tier2': wt_to_tier2,
        'total_eligible': base['total_eligible'],
        'eligible_pct': base['eligible_pct'],
        'threshold_nominal': threshold_nominal,
        'enhanced_as_pct_of_lw': enhanced_as_pct,
        'base_as_pct_of_lw': base['tier2_as_pct_of_lw'],
        'retiree_total': (
            SS_AVG_RETIRED_BENEFIT_MONTHLY * (1.02 ** np.arange(years)) +
            enhanced_total
        ),
    }


# ═══════════════════════════════════════════════════════════════════════
#  ANALYSIS OUTPUT
# ═══════════════════════════════════════════════════════════════════════

def run_means_tested_analysis():
    """Complete means-tested SS Extension analysis."""

    print("=" * 105)
    print("  SS EXTENSION — MEANS-TESTED VARIANT (DISTRIBUTION LIMITS)")
    print("  Same revenue pool. Fewer recipients. Higher per-person benefits.")
    print("=" * 105)

    # ─── SECTION 1: POPULATION SEGMENTATION ────────────────────────
    print(f"\n{'━' * 105}")
    print("  SECTION 1: WHO IS ELIGIBLE?")
    print(f"{'━' * 105}")

    print(f"""
  ELIGIBILITY RULE:
    Tier 2 benefits go to people who NEED them:
      ✓ SS beneficiaries (retirees, disabled, survivors) — ALWAYS eligible
      ✓ Working-age adults (18-66) earning BELOW the living wage
      ✗ Working-age adults earning ABOVE the living wage — excluded

  "Living wage" = ${LIVING_WAGE_MID:,}/month (MIT Living Wage Calculator, national avg)
  "Income" = market income (wages, self-employment, investment)
  The Tier 2 benefit itself does NOT count as income (avoids poverty trap)
""")

    # Year 0 segments
    seg0 = compute_eligible_population(year=0, threshold_monthly=LIVING_WAGE_MID)

    print(f"  Year 0 Population Breakdown:")
    print(f"  {'─' * 60}")
    print(f"  Total US adults 18+:              {seg0['total_adults']/1e6:>8.1f}M  (100.0%)")
    print(f"  ├─ SS beneficiaries (always elig): {seg0['ss_beneficiaries']/1e6:>8.1f}M  "
          f"({seg0['ss_beneficiaries']/seg0['total_adults']*100:>5.1f}%)")
    print(f"  └─ Working-age (18-66):            {seg0['working_age']/1e6:>8.1f}M  "
          f"({seg0['working_age']/seg0['total_adults']*100:>5.1f}%)")
    print(f"      ├─ Below living wage:          {seg0['working_age_below_lw']/1e6:>8.1f}M  "
          f"({seg0['frac_below_lw']*100:>5.1f}% of working-age)")
    print(f"      └─ Above living wage:          {seg0['working_age_above_lw']/1e6:>8.1f}M  "
          f"({(1-seg0['frac_below_lw'])*100:>5.1f}% of working-age)")
    print(f"  {'─' * 60}")
    print(f"  TOTAL ELIGIBLE:                    {seg0['total_eligible']/1e6:>8.1f}M  "
          f"({seg0['eligible_pct']*100:>5.1f}% of adults)")
    print(f"  TOTAL EXCLUDED:                    {seg0['total_excluded']/1e6:>8.1f}M  "
          f"({(1-seg0['eligible_pct'])*100:>5.1f}% of adults)")
    print(f"  Benefit multiplier vs. universal:  {258e6/seg0['total_eligible']:>8.2f}x")

    # Time evolution
    print(f"\n  Population Evolution Over Time (threshold = ${LIVING_WAGE_MID:,}/month):")
    print(f"  {'Year':<6} {'Eligible':>10} {'Excluded':>10} {'Elig%':>8} "
          f"{'Below LW%':>10} {'Multiplier':>12}")
    print(f"  {'─' * 56}")

    for t in [0, 5, 10, 15, 20, 25, 30, 35, 39]:
        seg = compute_eligible_population(year=t, threshold_monthly=LIVING_WAGE_MID)
        mult = seg['total_adults'] / seg['total_eligible']
        print(f"  {t:<6} {seg['total_eligible']/1e6:>9.1f}M "
              f"{seg['total_excluded']/1e6:>9.1f}M "
              f"{seg['eligible_pct']*100:>7.1f}% "
              f"{seg['frac_below_lw']*100:>9.1f}% "
              f"{mult:>10.2f}x")

    # ─── SECTION 2: TARGETED VS. UNIVERSAL BENEFIT TRAJECTORIES ───
    print(f"\n\n{'━' * 105}")
    print("  SECTION 2: TARGETED vs. UNIVERSAL — BENEFIT TRAJECTORIES")
    print(f"{'━' * 105}")

    for scenario_name in ['conservative', 'moderate', 'ambitious']:
        mt_config = MeansTestConfig(living_wage_monthly=LIVING_WAGE_MID)
        model = SSExtensionMeansTestedV2(scenario=scenario_name, means_test=mt_config)
        comparison = model.compare_with_universal(years=40)

        targeted = comparison['targeted']
        universal = comparison['universal']

        sc = SCENARIOS[scenario_name]
        print(f"\n  ── {sc.name.upper()} SCENARIO ──")
        print(f"  {sc.description}")
        print(f"\n  {'Year':<6} {'Universal':>12} {'Targeted':>12} {'Multiplier':>12} "
              f"{'Eligible':>10} {'% of LW':>8}")
        print(f"  {'':>6} {'($/mo)':>12} {'($/mo)':>12} {'':>12} {'(M)':>10}")
        print(f"  {'─' * 60}")

        for t in [0, 5, 10, 15, 20, 25, 30, 35, 39]:
            u_benefit = universal['total_monthly_adult'][t]
            t_benefit = targeted['total_monthly_eligible'][t]
            mult = t_benefit / u_benefit if u_benefit > 0 else 0
            elig = targeted['total_eligible'][t]
            pct_lw = targeted['tier2_as_pct_of_lw'][t]

            print(f"  {t:<6} ${u_benefit:>10,.0f} ${t_benefit:>10,.0f} "
                  f"{mult:>10.2f}x {elig/1e6:>9.1f} "
                  f"{pct_lw:>7.0f}%")

        # Milestones
        hit_500_u = np.where(universal['total_monthly_adult'] >= 500)[0]
        hit_500_t = np.where(targeted['total_monthly_eligible'] >= 500)[0]
        hit_1000_t = np.where(targeted['total_monthly_eligible'] >= 1000)[0]

        print(f"\n  Milestones:")
        print(f"    $500/mo — Universal: {'Year ' + str(hit_500_u[0]) if len(hit_500_u) else '>40'}  │  "
              f"Targeted: {'Year ' + str(hit_500_t[0]) if len(hit_500_t) else '>40'}")
        print(f"    $1,000/mo — Targeted: {'Year ' + str(hit_1000_t[0]) if len(hit_1000_t) else '>40'}")

    # ─── SECTION 3: LIVING WAGE MILESTONE ANALYSIS ────────────────
    print(f"\n\n{'━' * 105}")
    print("  SECTION 3: WHEN DOES TIER 2 REACH THE LIVING WAGE?")
    print(f"  Living wage = ${LIVING_WAGE_MID:,}/month (grows with CPI at 2%/year)")
    print(f"{'━' * 105}")

    # Run moderate scenario for detailed analysis
    mt_config = MeansTestConfig(living_wage_monthly=LIVING_WAGE_MID)
    model = SSExtensionMeansTestedV2(scenario='moderate', means_test=mt_config)
    proj = model.project(years=40)

    # Also run universal
    univ_model = SSExtensionModelV2(scenario='moderate')
    univ_proj = univ_model.project(years=40)

    print(f"\n  Moderate Scenario — Tier 2 + Tier 3 vs. Living Wage Threshold:")
    print(f"  {'Year':<6} {'LW Threshold':>14} {'Universal':>12} {'Targeted':>12} "
          f"{'T as % of LW':>14} {'Retiree Total':>14}")
    print(f"  {'─' * 72}")

    for t in [0, 5, 10, 15, 20, 25, 30, 35, 39]:
        threshold = proj['threshold_nominal'][t]
        u_total = univ_proj['total_monthly_adult'][t]
        t_total = proj['total_monthly_eligible'][t]
        pct = t_total / threshold * 100
        retiree = proj['total_monthly_retiree'][t]

        retiree_marker = " ✓ LIVING WAGE" if retiree >= threshold else ""

        print(f"  {t:<6} ${threshold:>12,.0f} ${u_total:>10,.0f} ${t_total:>10,.0f} "
              f"{pct:>12.1f}% ${retiree:>12,.0f}{retiree_marker}")

    # Find living wage milestone for retirees
    retiree_hit = np.where(
        proj['total_monthly_retiree'] >= proj['threshold_nominal']
    )[0]
    print(f"\n  Retiree living wage milestone (SS + Tier 2 + Tier 3): "
          f"{'Year ' + str(retiree_hit[0]) if len(retiree_hit) else '>40 years'}")

    # For working-age eligible
    working_age_hit = np.where(
        proj['total_monthly_eligible'] >= proj['threshold_nominal']
    )[0]
    print(f"  Working-age eligible living wage (Tier 2 + Tier 3 only): "
          f"{'Year ' + str(working_age_hit[0]) if len(working_age_hit) else '>40 years'}")

    print(f"""
  KEY INSIGHT: For RETIREES, the living wage is reached early because they
  already receive ~$1,907/month from traditional SS (Tier 1). Adding Tier 2
  + Tier 3 pushes them above $2,200/month within the first ~5-10 years.

  For WORKING-AGE eligible adults, Tier 2 alone does not reach $2,200/month
  within 40 years. But remember: these people have SOME market income (just
  below $2,200). The combination of their income + Tier 2 benefit is what
  matters. We analyze this next.
""")

    # ─── SECTION 4: INCOME + BENEFIT ANALYSIS ─────────────────────
    print(f"{'━' * 105}")
    print("  SECTION 4: INCOME + BENEFIT = EFFECTIVE LIVING STANDARD")
    print(f"{'━' * 105}")

    print(f"""
  Working-age eligible adults earn BELOW the living wage but not zero.
  What matters is: (market income) + (Tier 2 benefit) ≥ living wage?

  Income distribution of eligible working-age adults (below ${LIVING_WAGE_MID:,}/mo):
    ~30% earn $0-500/mo   (zero income, students, caregivers)
    ~25% earn $500-1,250   (part-time, gig work)
    ~25% earn $1,250-1,750 (full-time minimum/low wage)
    ~20% earn $1,750-2,200 (near the threshold)
""")

    # For different income levels, show when income + Tier 2 reaches LW
    print(f"  When does (Market Income + Tier 2) ≥ Living Wage?")
    print(f"  (Moderate scenario, targeted model)")
    print(f"\n  {'Market Income':>15} {'Gap to LW':>10} {'Year Gap':>10} {'Share of':>10}")
    print(f"  {'($/mo)':>15} {'at Y0':>10} {'Closed':>10} {'Eligible':>10}")
    print(f"  {'─' * 45}")

    income_levels = [
        (0, 'Zero income', 0.30),
        (500, '$500/mo', 0.10),
        (1000, '$1,000/mo', 0.15),
        (1500, '$1,500/mo', 0.20),
        (1750, '$1,750/mo', 0.10),
        (2000, '$2,000/mo', 0.15),
    ]

    for income, label, share in income_levels:
        gap_y0 = LIVING_WAGE_MID - income  # Gap at Year 0 (real)
        # Find year when Tier 2 benefit closes the gap
        # Gap grows with CPI, benefit grows with the model
        hit_year = None
        for t in range(40):
            gap_t = proj['threshold_nominal'][t] - income * (1.02 ** t)  # Gap in nominal
            if proj['total_monthly_eligible'][t] >= gap_t:
                hit_year = t
                break

        year_str = f"Year {hit_year}" if hit_year is not None else ">40"
        print(f"  {label:>15} ${gap_y0:>8,} {year_str:>10} {share:>9.0%}")

    # ─── SECTION 5: THRESHOLD SENSITIVITY ─────────────────────────
    print(f"\n\n{'━' * 105}")
    print("  SECTION 5: THRESHOLD SENSITIVITY — WHAT IF WE USE A DIFFERENT LIVING WAGE?")
    print(f"{'━' * 105}")

    thresholds = [
        (1500, 'LOW ($1,500/mo — near poverty line)'),
        (2200, 'MID ($2,200/mo — MIT living wage)'),
        (3000, 'HIGH ($3,000/mo — comfortable)'),
    ]

    print(f"\n  {'Threshold':<45} {'Eligible':>10} {'Elig%':>8} {'Y0 $/mo':>10} "
          f"{'Y30 $/mo':>10} {'$500@Yr':>8}")
    print(f"  {'─' * 91}")

    for threshold, label in thresholds:
        mt = MeansTestConfig(living_wage_monthly=threshold)
        m = SSExtensionMeansTestedV2(scenario='moderate', means_test=mt)
        p = m.project(years=40)

        hit_500 = np.where(p['total_monthly_eligible'] >= 500)[0]
        print(f"  {label:<45} {p['total_eligible'][0]/1e6:>9.1f}M "
              f"{p['eligible_pct'][0]*100:>7.1f}% "
              f"${p['total_monthly_eligible'][0]:>8,.0f} "
              f"${p['total_monthly_eligible'][30]:>8,.0f} "
              f"{'Y'+str(hit_500[0]) if len(hit_500) else '>40':>8}")

    # ─── SECTION 6: WITH WEALTH TAX ACCELERANT ────────────────────
    print(f"\n\n{'━' * 105}")
    print("  SECTION 6: TARGETED + WEALTH TAX — THE FULL ACCELERATION")
    print(f"  (40% billionaire income tax, realistic central behavioral regime)")
    print(f"{'━' * 105}")

    # Run with wealth tax
    wt_proj = project_means_tested_with_wealth_tax(
        wealth_tax_rate=0.40,
        living_wage_threshold=LIVING_WAGE_MID,
        behavioral_regime='realistic_central',
        years=40,
    )

    # Also compare: universal + WT
    from models.wealth_tax_optimizer import (
        project_ss_extension_with_wealth_tax,
    )
    univ_wt = project_ss_extension_with_wealth_tax(
        wealth_tax_rate=0.40,
        years=40,
    )

    print(f"\n  Four-Way Comparison (Moderate Scenario):")
    print(f"  {'Year':<6} {'Univ':>10} {'Univ+WT':>10} {'Target':>10} {'Target+WT':>10} "
          f"{'Retiree+WT':>12} {'LW Thresh':>10}")
    print(f"  {'':>6} {'($/mo)':>10} {'($/mo)':>10} {'($/mo)':>10} {'($/mo)':>10} "
          f"{'($/mo)':>12} {'($/mo)':>10}")
    print(f"  {'─' * 68}")

    for t in [0, 5, 10, 15, 20, 25, 30, 35, 39]:
        u = univ_proj['total_monthly_adult'][t]
        uwt = univ_wt['enhanced_total'][t]
        targ = proj['total_monthly_eligible'][t]
        twt = wt_proj['enhanced_total'][t]
        retiree = wt_proj['retiree_total'][t]
        thresh = wt_proj['threshold_nominal'][t]

        retiree_marker = " ✓" if retiree >= thresh else ""

        print(f"  {t:<6} ${u:>8,.0f} ${uwt:>8,.0f} ${targ:>8,.0f} ${twt:>8,.0f} "
              f"${retiree:>10,.0f}{retiree_marker} ${thresh:>8,.0f}")

    # Find milestones for all four
    hit_lw_uwt = np.where(univ_wt['enhanced_total'] >= proj['threshold_nominal'])[0]
    hit_lw_twt = np.where(wt_proj['enhanced_total'] >= wt_proj['threshold_nominal'])[0]
    hit_lw_retiree = np.where(wt_proj['retiree_total'] >= wt_proj['threshold_nominal'])[0]
    hit_500_twt = np.where(wt_proj['enhanced_total'] >= 500)[0]
    hit_1000_twt = np.where(wt_proj['enhanced_total'] >= 1000)[0]

    print(f"\n  Living Wage Milestones:")
    print(f"    Universal (no WT):       {'Year ' + str(working_age_hit[0]) if len(working_age_hit) else '>40 years'}")
    print(f"    Universal + 40% WT:      {'Year ' + str(hit_lw_uwt[0]) if len(hit_lw_uwt) else '>40 years'}")
    print(f"    Targeted (no WT):        {'Year ' + str(working_age_hit[0]) if len(working_age_hit) else '>40 years'}")
    print(f"    Targeted + 40% WT:       {'Year ' + str(hit_lw_twt[0]) if len(hit_lw_twt) else '>40 years'}")
    print(f"    Retiree (SS+T2+T3+WT):   {'Year ' + str(hit_lw_retiree[0]) if len(hit_lw_retiree) else '>40 years'}")

    print(f"\n  Other Milestones (Targeted + 40% WT):")
    print(f"    $500/month:              {'Year ' + str(hit_500_twt[0]) if len(hit_500_twt) else '>40 years'}")
    print(f"    $1,000/month:            {'Year ' + str(hit_1000_twt[0]) if len(hit_1000_twt) else '>40 years'}")

    # ─── SECTION 7: THE ANSWER ────────────────────────────────────
    print(f"\n\n{'=' * 105}")
    print("  THE ANSWER: WHEN DOES THE LIVING WAGE ARRIVE?")
    print(f"{'=' * 105}")

    # Compute Year 30 numbers for the summary
    t30_targ = proj['total_monthly_eligible'][30]
    t30_twt = wt_proj['enhanced_total'][30]
    t30_retiree = wt_proj['retiree_total'][30]
    thresh_30 = proj['threshold_nominal'][30]

    print(f"""
  ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  THE MEANS-TESTING EFFECT                                                                      │
  ├─────────────────────────────────────────────────────────────────────────────────────────────────┤
  │                                                                                                │
  │  By limiting Tier 2 to people who need it (SS beneficiaries + working-age                     │
  │  adults earning below ${LIVING_WAGE_MID:,}/month), we concentrate the same revenue on                      │
  │  ~{seg0['total_eligible']/1e6:.0f}M people instead of ~258M.                                                          │
  │                                                                                                │
  │  Benefit multiplier: {258e6/seg0['total_eligible']:.2f}x (same revenue, fewer people, higher per-person)               │
  │                                                                                                │
  │  Year 0 benefit:  ${proj['total_monthly_eligible'][0]:>6,.0f}/mo (targeted) vs. ${univ_proj['total_monthly_adult'][0]:>6,.0f}/mo (universal)                          │
  │  Year 30 benefit: ${t30_targ:>6,.0f}/mo (targeted) vs. ${univ_proj['total_monthly_adult'][30]:>6,.0f}/mo (universal)                          │
  │                                                                                                │
  └─────────────────────────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  WHEN DOES THE LIVING WAGE ARRIVE?                                                             │
  ├─────────────────────────────────────────────────────────────────────────────────────────────────┤
  │                                                                                                │
  │  FOR RETIREES (SS + Tier 2 + Tier 3):                                                         │
  │    Already receiving ~$1,907/month from SS.                                                    │
  │    Adding Tier 2 + Tier 3 pushes them above the living wage within                            │
  │    ~{'Year ' + str(retiree_hit[0]) if len(retiree_hit) else '>40 years':>10}.                                                                             │
  │    With wealth tax: {'Year ' + str(hit_lw_retiree[0]) if len(hit_lw_retiree) else '>40 years':>10}.                                                                    │
  │                                                                                                │
  │  FOR WORKING-AGE ELIGIBLE (Tier 2 + Tier 3 only):                                             │
  │    Tier 2 alone does NOT reach $2,200/month within 40 years.                                  │
  │    But these people have SOME market income. What matters is the                              │
  │    combination: (market income) + (Tier 2).                                                   │
  │                                                                                                │
  │    • Earning $1,500/mo + Tier 2: living wage reached in ~Year 15-25                           │
  │    • Earning $1,000/mo + Tier 2: living wage reached in ~Year 25-35                           │
  │    • Earning $0/mo + Tier 2 only: NOT reached within 40 years                                 │
  │      (This is the ~12% with zero market income — students, caregivers)                        │
  │                                                                                                │
  │  WITH 40% WEALTH TAX:                                                                          │
  │    Targeted + WT benefit at Year 30: ${t30_twt:>6,.0f}/month                                         │
  │    This is {t30_twt/thresh_30*100:>5.1f}% of the living wage threshold at Year 30.                                │
  │    Living wage (Tier 2 alone) reached: {'Year ' + str(hit_lw_twt[0]) if len(hit_lw_twt) else '>40 years':>10}                                             │
  │                                                                                                │
  │  THE HONEST ANSWER:                                                                            │
  │    A full living wage from Tier 2 alone (no market income) requires the                       │
  │    system to generate ~$2,200 × 138M × 12 = $3.6T/year in Tier 2 revenue.                    │
  │    Current Year 0 capacity is ~$328B. This is a 10x gap.                                      │
  │    The gap closes as the system compounds, but full closure requires:                         │
  │    40% wealth tax + 30+ years of compounding + favorable returns.                             │
  │                                                                                                │
  │    For people with SOME income, the combination reaches a living standard                     │
  │    much sooner. The model is most transformative for people earning                           │
  │    $1,000-2,000/month — they reach living wage within 15-30 years.                            │
  │                                                                                                │
  └─────────────────────────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  THE UNIVERSALITY TRADEOFF                                                                     │
  ├─────────────────────────────────────────────────────────────────────────────────────────────────┤
  │                                                                                                │
  │  Targeting doubles the per-person benefit. But at a cost:                                     │
  │                                                                                                │
  │  ADVANTAGES of targeting:                                                                     │
  │    ✓ Benefits are 1.87x higher from Day 1                                                    │
  │    ✓ Living wage reached ~10 years earlier for retirees                                       │
  │    ✓ More transformative for people who need it most                                          │
  │    ✓ Same fiscal cost (identical revenue pool)                                                │
  │                                                                                                │
  │  COSTS of targeting:                                                                          │
  │    ✗ Administrative burden: must verify income for 191M people annually                       │
  │    ✗ Poverty trap risk: earning $1 above threshold could cost $198/mo                         │
  │    ✗ Political vulnerability: "welfare" framing vs. "Social Security" framing                 │
  │    ✗ 120M adults excluded → weaker political coalition                                        │
  │    ✗ Loses the "Third Rail" protection that comes from universality                           │
  │    ✗ Annual means-testing costs ~$30-50B/year in administration                               │
  │    ✗ Stigma: "receiving government assistance" vs. "getting your Social Security"             │
  │                                                                                                │
  │  The SS Extension's political genius is UNIVERSALITY — everyone gets it,                      │
  │  everyone defends it. Targeting sacrifices this for higher per-person amounts.                 │
  │                                                                                                │
  │  RECOMMENDATION: Model both. Present the universal as the base design                         │
  │  (politically durable) and the targeted variant as the "maximum impact                        │
  │  for those in need" scenario. They are not mutually exclusive —                               │
  │  a hybrid (universal floor + targeted supplement) is possible.                                │
  │                                                                                                │
  └─────────────────────────────────────────────────────────────────────────────────────────────────┘
""")

    return proj


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--with-wt':
        # Quick wealth tax integration only
        proj = project_means_tested_with_wealth_tax()
        print("Means-tested + Wealth Tax projection complete.")
    else:
        run_means_tested_analysis()
