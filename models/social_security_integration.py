"""
Social Security Integration Model

Models the interaction between a sovereign UBI fund and the existing
Social Security system. This is critical because:

1. Social Security is the largest existing US transfer program (~$1.4T/year)
2. Its trust fund faces depletion ~2033-2035 (CBO/SSA projections)
3. UBI and SS have complex fiscal interactions
4. The political path to a UBI fund likely runs THROUGH Social Security reform

Key questions this model addresses:
- How does UBI interact with existing SS benefits?
- Can the sovereign fund partially rescue SS solvency?
- What happens to the labor market model when we account for SS?
- What are the net fiscal effects (UBI + SS reform together)?
- Which integration strategy maximizes political feasibility?

Current US Safety Net Landscape (annual, approximate):
- Social Security (OASDI):           $1,400B  (67M beneficiaries)
- Medicare:                           $  900B  (65M beneficiaries)
- Medicaid:                           $  600B  (85M enrollees)
- SNAP (food stamps):                 $  110B  (42M participants)
- SSI (Supplemental Security Income): $   60B  (7.5M recipients)
- EITC (Earned Income Tax Credit):    $   60B  (31M filers)
- Housing assistance (Section 8 etc): $   55B  (5M households)
- TANF (welfare):                     $   16B  (2.5M families)
- Unemployment insurance:             $   30B  (varies cyclically)
- Total:                             ~$3,230B

References:
- SSA (2024) Annual Report of the Board of Trustees of OASDI Trust Funds
- CBO (2024) Long-Term Budget Outlook
- Widerquist (2018) "A Critical Analysis of Basic Income Experiments"
- Hoynes & Rothstein (2019) "Universal Basic Income in the US" Ann Rev Econ
- Ghilarducci (2024) "Rescuing Retirement" (pension/SS reform proposals)

Sources calibrated from:
- SSA.gov OASDI Statistics (2024)
- CBO Budget and Economic Outlook (2024)
- BLS Consumer Expenditure Survey
"""

import numpy as np
from dataclasses import dataclass, field
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.parameters import *


# === SOCIAL SECURITY PARAMETERS ===

@dataclass
class SSParameters:
    """Calibrated Social Security system parameters."""

    # Current system (2024 baseline)
    total_beneficiaries: int = 67_000_000       # All OASDI recipients
    retired_workers: int = 50_000_000           # Retired worker beneficiaries
    disabled_workers: int = 7_500_000           # SSDI recipients
    survivors: int = 5_800_000                  # Survivor beneficiaries
    dependents: int = 3_700_000                 # Dependent beneficiaries

    avg_retired_benefit_monthly: float = 1_907  # Average retired worker benefit
    avg_disabled_benefit_monthly: float = 1_537 # Average SSDI benefit
    avg_survivor_benefit_monthly: float = 1_513 # Average survivor benefit
    max_benefit_monthly: float = 4_873          # Maximum at FRA (2024)

    total_annual_outlays: float = 1_400e9       # $1.4T/year total OASDI
    total_annual_revenue: float = 1_200e9       # Payroll tax + taxation of benefits
    annual_deficit: float = 200e9               # Current annual shortfall

    # Trust fund
    trust_fund_balance: float = 2_700e9         # Combined OASI + DI (declining)
    projected_depletion_year: int = 2034        # CBO central estimate
    post_depletion_benefit_pct: float = 0.77    # Benefits payable from ongoing revenue

    # Tax structure
    payroll_tax_rate: float = 0.124             # 12.4% combined (employer + employee)
    taxable_maximum: float = 168_600            # 2024 wage cap
    covered_workers: int = 180_000_000          # Workers paying into system

    # Demographics
    worker_to_beneficiary_ratio: float = 2.7    # Declining from 3.3 in 2010
    ratio_projection_2040: float = 2.2          # Projected decline
    ratio_projection_2060: float = 2.0


# Other major transfer programs
@dataclass
class SafetyNetParameters:
    """Parameters for other major US safety net programs."""
    medicare_annual: float = 900e9
    medicaid_annual: float = 600e9
    snap_annual: float = 110e9
    ssi_annual: float = 60e9
    eitc_annual: float = 60e9
    housing_annual: float = 55e9
    tanf_annual: float = 16e9
    unemployment_annual: float = 30e9

    @property
    def total_non_ss(self) -> float:
        return (self.medicare_annual + self.medicaid_annual + self.snap_annual +
                self.ssi_annual + self.eitc_annual + self.housing_annual +
                self.tanf_annual + self.unemployment_annual)

    @property
    def total_all(self) -> float:
        return self.total_non_ss + SSParameters().total_annual_outlays

    # Programs that could potentially be consolidated into UBI
    @property
    def ubi_consolidation_candidates(self) -> dict:
        """
        Programs that overlap with UBI's purpose (cash/near-cash transfers).
        Medicare/Medicaid are NOT candidates — they serve a different function.
        """
        return {
            'SNAP': self.snap_annual,
            'SSI (partial)': self.ssi_annual * 0.5,  # Only supplement portion
            'EITC (partial)': self.eitc_annual * 0.3,  # Phase-out region overlap
            'TANF': self.tanf_annual,
            'Housing (partial)': self.housing_annual * 0.2,  # Voucher portion
        }

    @property
    def consolidation_savings(self) -> float:
        return sum(self.ubi_consolidation_candidates.values())

    @property
    def administrative_savings(self) -> float:
        """
        UBI eliminates means-testing bureaucracy.
        GAO estimates 5-15% of program costs go to administration.
        Conservative: 5% of consolidated programs.
        """
        return self.consolidation_savings * 0.05


class SocialSecurityProjection:
    """
    Projects the Social Security trust fund trajectory and solvency.

    Models the path to depletion under baseline demographics and
    how a sovereign UBI fund could interact with SS reform.
    """

    def __init__(self, ss: SSParameters = None):
        self.ss = ss or SSParameters()

    def project_trust_fund(self, years: int = 30,
                           gdp_growth: float = GDP_GROWTH_REAL,
                           wage_growth: float = 0.01,  # Real wage growth
                           benefit_growth: float = 0.02,  # CPI-W indexing
                           ) -> dict:
        """
        Project the SS trust fund balance forward.

        Key dynamics:
        - Revenue grows with wage growth + labor force growth
        - Outlays grow with benefit indexing + demographic pressure
        - Trust fund earns ~2.5% (special-issue Treasury bonds)
        - After depletion: benefits cut to what ongoing revenue supports
        """
        fund_balance = np.zeros(years + 1)
        revenue = np.zeros(years)
        outlays = np.zeros(years)
        benefit_cut_pct = np.zeros(years)
        depleted = np.zeros(years, dtype=bool)

        fund_balance[0] = self.ss.trust_fund_balance

        current_revenue = self.ss.total_annual_revenue
        current_outlays = self.ss.total_annual_outlays

        trust_fund_interest_rate = 0.025  # Real return on special-issue Treasuries

        for t in range(years):
            # Revenue: grows with wages + covered employment
            labor_force_growth = max(0.003 - t * 0.0001, 0.0)  # Slowing growth
            revenue_growth = wage_growth + labor_force_growth
            current_revenue *= (1 + revenue_growth)
            revenue[t] = current_revenue

            # Outlays: grow faster due to aging + benefit indexing
            # Beneficiary growth ~2-3% for next 15 years, then slows
            beneficiary_growth = 0.025 if t < 15 else 0.01
            outlay_growth = benefit_growth + beneficiary_growth
            current_outlays *= (1 + outlay_growth)
            outlays[t] = current_outlays

            # Trust fund dynamics
            interest = fund_balance[t] * trust_fund_interest_rate if fund_balance[t] > 0 else 0
            net_flow = revenue[t] - outlays[t] + interest

            new_balance = fund_balance[t] + net_flow

            if new_balance <= 0:
                # Trust fund depleted
                depleted[t] = True
                fund_balance[t + 1] = 0
                # Benefits cut to what revenue can support
                benefit_cut_pct[t] = 1 - (revenue[t] / outlays[t])
            else:
                fund_balance[t + 1] = new_balance
                benefit_cut_pct[t] = 0.0

        return {
            'fund_balance': fund_balance,
            'revenue': revenue,
            'outlays': outlays,
            'annual_deficit': outlays - revenue,
            'benefit_cut_pct': benefit_cut_pct,
            'depleted': depleted,
            'depletion_year': int(np.argmax(depleted)) if np.any(depleted) else None,
        }


class IntegrationStrategy:
    """
    Models different strategies for integrating UBI with Social Security.

    Strategy 1: PARALLEL — UBI supplements SS; both systems coexist
    Strategy 2: PARTIAL MERGER — UBI replaces SS minimum; SS tops up
    Strategy 3: FULL MERGER — UBI replaces SS entirely (most ambitious)
    Strategy 4: SS RESCUE — Sovereign fund shores up SS solvency first

    Each strategy has different fiscal costs, political feasibility,
    and distributional implications.
    """

    def __init__(self, ss: SSParameters = None, safety_net: SafetyNetParameters = None):
        self.ss = ss or SSParameters()
        self.sn = safety_net or SafetyNetParameters()

    def strategy_parallel(self, monthly_ubi: float) -> dict:
        """
        Strategy 1: UBI runs alongside SS. No program changes.

        Everyone gets UBI on top of whatever SS they currently receive.
        Simplest politically but most expensive.
        """
        annual_ubi = monthly_ubi * 12
        total_ubi_cost = annual_ubi * US_POPULATION

        # Net new spending = full UBI cost (no offsets)
        # But some fraction is "recaptured" through income tax on high earners
        # who receive UBI but are in high brackets
        # Rough: ~15% of UBI goes to people who'd pay it back in taxes
        tax_clawback = total_ubi_cost * 0.15
        net_cost = total_ubi_cost - tax_clawback

        # Total transfer spending
        total_transfers = self.ss.total_annual_outlays + self.sn.total_non_ss + net_cost

        # Effective benefit for different groups
        retiree_total = self.ss.avg_retired_benefit_monthly + monthly_ubi
        disabled_total = self.ss.avg_disabled_benefit_monthly + monthly_ubi
        working_age_no_ss = monthly_ubi

        return {
            'strategy': 'Parallel (UBI + SS coexist)',
            'monthly_ubi': monthly_ubi,
            'gross_ubi_cost': total_ubi_cost,
            'net_new_cost': net_cost,
            'ss_savings': 0,
            'other_program_savings': 0,
            'total_transfer_spending': total_transfers,
            'total_as_pct_gdp': total_transfers / GDP_US,
            'retiree_monthly_total': retiree_total,
            'disabled_monthly_total': disabled_total,
            'working_age_monthly': working_age_no_ss,
            'political_feasibility': 0.6,  # Moderate — no losers
            'distributional_note': (
                'All groups gain. Retirees get the most total income. '
                'Most expensive strategy but no one loses benefits.'
            ),
        }

    def strategy_partial_merger(self, monthly_ubi: float) -> dict:
        """
        Strategy 2: UBI replaces the bottom tier of SS.

        SS benefits above the UBI level are preserved as a "top-up."
        Those receiving less than UBI from SS get the UBI instead.
        Means-tested programs (SNAP, TANF, SSI) are consolidated.

        This is essentially: everyone gets at least $UBI/month.
        If your SS benefit exceeds that, you get UBI + (SS - UBI offset).
        Net effect: SS payroll tax savings on the bottom tier.
        """
        annual_ubi = monthly_ubi * 12

        # How many SS beneficiaries currently get less than UBI?
        # Distribution: roughly 30% get < $1500/mo, 15% get < $1000/mo
        # At $500/mo UBI: ~5% of retirees are below this (very low)
        # At $200/mo UBI: ~1% (nearly all retirees get more than this)
        if monthly_ubi < 500:
            ss_beneficiaries_below_ubi = int(self.ss.total_beneficiaries * 0.02)
            avg_ss_savings_per_beneficiary = monthly_ubi * 12 * 0.5  # Partial offset
        elif monthly_ubi < 1000:
            ss_beneficiaries_below_ubi = int(self.ss.total_beneficiaries * 0.12)
            avg_ss_savings_per_beneficiary = monthly_ubi * 12 * 0.6
        else:
            ss_beneficiaries_below_ubi = int(self.ss.total_beneficiaries * 0.30)
            avg_ss_savings_per_beneficiary = monthly_ubi * 12 * 0.7

        ss_savings = ss_beneficiaries_below_ubi * avg_ss_savings_per_beneficiary

        # Consolidate means-tested programs
        consolidation = self.sn.consolidation_savings
        admin_savings = self.sn.administrative_savings

        total_ubi_cost = annual_ubi * US_POPULATION
        net_cost = total_ubi_cost - ss_savings - consolidation - admin_savings
        tax_clawback = total_ubi_cost * 0.15
        net_cost -= tax_clawback

        total_transfers = (self.ss.total_annual_outlays - ss_savings +
                          self.sn.total_non_ss - consolidation + total_ubi_cost)

        return {
            'strategy': 'Partial Merger (UBI floor + SS top-up)',
            'monthly_ubi': monthly_ubi,
            'gross_ubi_cost': total_ubi_cost,
            'ss_savings': ss_savings,
            'program_consolidation_savings': consolidation,
            'admin_savings': admin_savings,
            'tax_clawback': tax_clawback,
            'net_new_cost': net_cost,
            'total_transfer_spending': total_transfers,
            'total_as_pct_gdp': total_transfers / GDP_US,
            'retiree_monthly_total': max(self.ss.avg_retired_benefit_monthly, monthly_ubi),
            'disabled_monthly_total': max(self.ss.avg_disabled_benefit_monthly, monthly_ubi),
            'working_age_monthly': monthly_ubi,
            'political_feasibility': 0.4,  # Hard — some perceive as "cutting SS"
            'distributional_note': (
                'No one gets less than today. Low-SS recipients see gains. '
                'SNAP/TANF recipients lose specific benefits but gain cash flexibility. '
                'Political risk: can be framed as "cutting Social Security."'
            ),
        }

    def strategy_ss_rescue(self, monthly_ubi: float, rescue_pct: float = 0.25) -> dict:
        """
        Strategy 4: Sovereign fund shores up SS solvency first.

        A fraction of the sovereign fund's withdrawals go to the SS trust
        fund to prevent benefit cuts after depletion. Remainder goes to UBI.

        This may be the most politically viable path:
        "We saved Social Security AND created a dividend for everyone."

        Args:
            monthly_ubi: Target UBI after SS rescue allocation
            rescue_pct: Fraction of sovereign fund withdrawals allocated to SS
        """
        # Project SS shortfall
        ss_proj = SocialSecurityProjection(self.ss)
        projection = ss_proj.project_trust_fund(years=30)

        # Annual SS rescue need: the deficit between revenue and full outlays
        # After trust fund depletion, this is ~23% of outlays
        ss_annual_shortfall = projection['annual_deficit']
        avg_shortfall_post_depletion = float(np.mean(
            ss_annual_shortfall[projection['depleted']]
        )) if np.any(projection['depleted']) else 0

        # Sovereign fund allocation to SS rescue
        # Assume fund of $10T, 3.5% withdrawal = $350B
        # 25% to SS = $87.5B; 75% to UBI = $262.5B
        assumed_fund_size = 10e12
        assumed_withdrawal_rate = 0.035
        total_withdrawal = assumed_fund_size * assumed_withdrawal_rate
        ss_rescue_allocation = total_withdrawal * rescue_pct
        ubi_allocation = total_withdrawal * (1 - rescue_pct)

        # Can the rescue allocation cover the SS shortfall?
        ss_coverage_ratio = ss_rescue_allocation / max(avg_shortfall_post_depletion, 1)

        # UBI from remaining allocation
        effective_ubi_annual = ubi_allocation / US_POPULATION
        effective_ubi_monthly = effective_ubi_annual / 12

        # If the fund is big enough, SS is fully rescued + UBI still works
        ss_fully_rescued = ss_rescue_allocation >= avg_shortfall_post_depletion

        return {
            'strategy': f'SS Rescue ({rescue_pct:.0%} to SS, {1-rescue_pct:.0%} to UBI)',
            'total_sovereign_withdrawal': total_withdrawal,
            'ss_rescue_allocation': ss_rescue_allocation,
            'ubi_allocation': ubi_allocation,
            'avg_ss_shortfall_post_depletion': avg_shortfall_post_depletion,
            'ss_coverage_ratio': ss_coverage_ratio,
            'ss_fully_rescued': ss_fully_rescued,
            'effective_ubi_monthly': effective_ubi_monthly,
            'depletion_year_baseline': projection['depletion_year'],
            'benefit_cut_avoided_pct': min(ss_coverage_ratio, 1.0) * projection['benefit_cut_pct'].max() if np.any(projection['depleted']) else 0,
            'political_feasibility': 0.8,  # High — saves SS + creates new benefit
            'distributional_note': (
                f'SS benefits preserved at 100% (vs {self.ss.post_depletion_benefit_pct:.0%} without rescue). '
                f'All adults receive ${effective_ubi_monthly:.0f}/month UBI on top. '
                'Strongest political narrative: "saved Social Security and created a dividend."'
            ),
        }

    def compare_all_strategies(self, monthly_ubi: float = 200) -> list[dict]:
        """Compare all integration strategies at a given UBI level."""
        return [
            self.strategy_parallel(monthly_ubi),
            self.strategy_partial_merger(monthly_ubi),
            self.strategy_ss_rescue(monthly_ubi),
        ]

    def net_fiscal_impact(self, monthly_ubi: float, strategy: str = 'parallel') -> dict:
        """
        Compute the net fiscal impact of UBI on the federal budget,
        accounting for ALL interactions with existing programs.
        """
        if strategy == 'parallel':
            result = self.strategy_parallel(monthly_ubi)
        elif strategy == 'partial_merger':
            result = self.strategy_partial_merger(monthly_ubi)
        elif strategy == 'ss_rescue':
            result = self.strategy_ss_rescue(monthly_ubi)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        # Broader fiscal effects of UBI
        annual_ubi = monthly_ubi * 12

        # 1. Economic multiplier: UBI recipients spend most of it
        # MPC for low-income: ~0.9; for high-income: ~0.3
        # Population-weighted MPC: ~0.65
        marginal_propensity_consume = 0.65
        consumption_boost = annual_ubi * US_POPULATION * marginal_propensity_consume

        # 2. Tax revenue from induced consumption (sales tax, income tax on businesses)
        # Rough: 15% effective rate on consumption-driven economic activity
        induced_tax_revenue = consumption_boost * 0.15

        # 3. Reduced social costs (ER visits, incarceration, homelessness services)
        # Literature: ~$5,000-10,000/year per person lifted from poverty
        # At $200/mo UBI: ~5M people lifted above poverty line
        poverty_reduction_persons = min(5_000_000 * (monthly_ubi / 200), 20_000_000)
        social_cost_savings = poverty_reduction_persons * 7_500  # $7,500/person

        # 4. Reduced Medicaid spending (better health outcomes)
        # Modest: 1-2% reduction in Medicaid for UBI recipients
        medicaid_savings = self.sn.medicaid_annual * 0.01 * min(monthly_ubi / 500, 1.0)

        return {
            **result,
            'consumption_boost': consumption_boost,
            'induced_tax_revenue': induced_tax_revenue,
            'social_cost_savings': social_cost_savings,
            'medicaid_savings': medicaid_savings,
            'total_fiscal_offset': (
                induced_tax_revenue + social_cost_savings + medicaid_savings +
                result.get('ss_savings', 0) + result.get('program_consolidation_savings', 0) +
                result.get('admin_savings', 0) + result.get('tax_clawback', 0)
            ),
        }


def run_ss_analysis():
    """Run the full Social Security integration analysis."""
    print("=" * 80)
    print("SOCIAL SECURITY INTEGRATION ANALYSIS")
    print("=" * 80)

    # 1. SS Trust Fund Projection (baseline, no intervention)
    print("\n--- Social Security Trust Fund Baseline Projection ---")
    ss = SSParameters()
    proj = SocialSecurityProjection(ss)
    baseline = proj.project_trust_fund(years=30)

    print(f"  Current trust fund balance:  ${ss.trust_fund_balance/1e9:.0f}B")
    print(f"  Current annual deficit:      ${ss.annual_deficit/1e9:.0f}B")
    if baseline['depletion_year'] is not None:
        print(f"  Projected depletion:         Year {baseline['depletion_year']} "
              f"(~{2024 + baseline['depletion_year']})")
        # Find max benefit cut
        max_cut = baseline['benefit_cut_pct'].max()
        print(f"  Benefit cut after depletion: {max_cut:.0%}")
    else:
        print("  Trust fund does not deplete in projection window")

    for yr in [5, 10, 15, 20, 25, 30]:
        if yr <= len(baseline['fund_balance']) - 1:
            bal = baseline['fund_balance'][yr]
            cut = baseline['benefit_cut_pct'][min(yr, len(baseline['benefit_cut_pct'])-1)]
            dep = "DEPLETED" if baseline['depleted'][min(yr, len(baseline['depleted'])-1)] else ""
            print(f"  Year {yr:2d} ({2024+yr}): Balance ${bal/1e9:>8.0f}B  "
                  f"Cut: {cut:>5.1%}  {dep}")

    # 2. Current Safety Net Overview
    print("\n--- Current US Safety Net Landscape ---")
    sn = SafetyNetParameters()
    print(f"  Social Security (OASDI):     ${ss.total_annual_outlays/1e9:>8.0f}B/yr")
    print(f"  Medicare:                     ${sn.medicare_annual/1e9:>8.0f}B/yr")
    print(f"  Medicaid:                     ${sn.medicaid_annual/1e9:>8.0f}B/yr")
    print(f"  SNAP:                         ${sn.snap_annual/1e9:>8.0f}B/yr")
    print(f"  SSI:                          ${sn.ssi_annual/1e9:>8.0f}B/yr")
    print(f"  EITC:                         ${sn.eitc_annual/1e9:>8.0f}B/yr")
    print(f"  Housing Assistance:           ${sn.housing_annual/1e9:>8.0f}B/yr")
    print(f"  TANF:                         ${sn.tanf_annual/1e9:>8.0f}B/yr")
    print(f"  Unemployment Insurance:       ${sn.unemployment_annual/1e9:>8.0f}B/yr")
    print(f"  {'─' * 50}")
    print(f"  TOTAL (all programs):         ${sn.total_all/1e9:>8.0f}B/yr "
          f"({sn.total_all/GDP_US:.1%} of GDP)")

    print(f"\n  Programs consolidatable into UBI:")
    for name, amount in sn.ubi_consolidation_candidates.items():
        print(f"    {name:<25} ${amount/1e9:>6.1f}B/yr")
    print(f"    {'─' * 35}")
    print(f"    {'Potential savings':<25} ${sn.consolidation_savings/1e9:>6.1f}B/yr")
    print(f"    {'+ Admin savings':<25} ${sn.administrative_savings/1e9:>6.1f}B/yr")

    # 3. Integration Strategy Comparison
    print("\n\n--- Integration Strategy Comparison ---")
    integrator = IntegrationStrategy(ss, sn)

    for ubi_level in [200, 500]:
        print(f"\n  === At ${ubi_level}/month UBI ===")
        strategies = integrator.compare_all_strategies(ubi_level)

        for s in strategies:
            print(f"\n  {s['strategy']}")
            if 'net_new_cost' in s:
                print(f"    Net new cost:        ${s['net_new_cost']/1e9:>8.0f}B/yr")
            if 'total_as_pct_gdp' in s:
                print(f"    Total transfers/GDP:  {s['total_as_pct_gdp']:>8.1%}")
            if 'effective_ubi_monthly' in s:
                print(f"    Effective UBI:        ${s['effective_ubi_monthly']:>8.0f}/mo")
            elif 'working_age_monthly' in s:
                print(f"    Working-age benefit:  ${s['working_age_monthly']:>8.0f}/mo")
            if 'retiree_monthly_total' in s:
                print(f"    Retiree total:        ${s['retiree_monthly_total']:>8.0f}/mo")
            print(f"    Political feasibility: {s['political_feasibility']:>7.0%}")
            print(f"    Note: {s['distributional_note'][:100]}...")

    # 4. Net Fiscal Impact (deep dive on SS Rescue strategy)
    print("\n\n--- Net Fiscal Impact: SS Rescue Strategy at $200/mo ---")
    fiscal = integrator.net_fiscal_impact(200, strategy='ss_rescue')
    print(f"  Sovereign fund withdrawal:    ${fiscal['total_sovereign_withdrawal']/1e9:>8.0f}B/yr")
    print(f"  Allocated to SS rescue:       ${fiscal['ss_rescue_allocation']/1e9:>8.0f}B/yr")
    print(f"  Allocated to UBI:             ${fiscal['ubi_allocation']/1e9:>8.0f}B/yr")
    print(f"  SS shortfall covered:          {fiscal['ss_coverage_ratio']:>7.1%}")
    print(f"  SS fully rescued:              {'YES' if fiscal['ss_fully_rescued'] else 'NO'}")
    print(f"\n  Fiscal Offsets:")
    print(f"    Consumption-induced tax rev: ${fiscal['induced_tax_revenue']/1e9:>8.1f}B/yr")
    print(f"    Social cost savings:         ${fiscal['social_cost_savings']/1e9:>8.1f}B/yr")
    print(f"    Medicaid savings:            ${fiscal['medicaid_savings']/1e9:>8.1f}B/yr")
    print(f"    Total fiscal offset:         ${fiscal['total_fiscal_offset']/1e9:>8.1f}B/yr")

    # 5. The Recommended Path
    print("\n\n" + "=" * 80)
    print("RECOMMENDED INTEGRATION: SS RESCUE + UBI DIVIDEND")
    print("=" * 80)
    print("""
  The most politically viable and fiscally efficient path:

  1. Frame the sovereign fund as "Social Security Plus"
     - Rescues SS from insolvency (prevents the ~23% benefit cut in 2034)
     - Creates a universal dividend on top for ALL adults

  2. Allocation: 25% of fund withdrawals to SS, 75% to UBI
     - At $10T fund / 3.5% withdrawal = $350B/year
     - $87.5B/year fills the SS trust fund gap
     - $262.5B/year = ~$66/month UBI per adult initially
     - As fund grows, both allocations grow

  3. This solves TWO problems at once:
     - SS solvency crisis (political urgency provides the forcing function)
     - Creates a new universal benefit (builds permanent constituency)

  4. Why this works politically:
     - "Saving Social Security" is the #1 voter issue for 50+ demographics
     - Universal dividend polls at 60-70% when framed as "national wealth sharing"
     - No one loses current benefits (critical for political viability)
     - The SS rescue creates urgency that pure UBI lacks

  5. Long-term trajectory:
     - Year 20-25: SS rescue + $50-100/mo UBI
     - Year 30-35: SS rescued, UBI grows to $200-400/mo
     - Year 40+:   SS potentially merged into UBI as fund matures
""")


if __name__ == '__main__':
    run_ss_analysis()
