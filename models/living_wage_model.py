"""
Living Wage UBI Model — Full Cost Analysis

Target: A living wage for every US adult (18+), funded by a composite
strategy that includes sovereign fund extraction, SS reform, wealth taxes,
and safety net consolidation.

Living Wage Definition:
- MIT Living Wage Calculator (2024): $21.33/hr for single adult, no children
  = ~$3,700/month before tax in high-cost areas
  = ~$2,200/month national average (weighted by population density)
- Federal poverty line (2024): $1,255/month for single person
- "Living wage" here means: sufficient for basic needs without employment
  = housing + food + transportation + healthcare + utilities + personal
  = ~$2,000-2,500/month depending on geography

We model $2,200/month as the national average target.
This is the ambitious goal. We show what it takes.

Key insight: $2,200/month for all adults 18+ costs ~$7.1T/year.
This is 25% of GDP — MASSIVE. No single source can fund this.
The question is: what combination of sources gets there?

Revenue Sources Modeled:
1. Sovereign wealth fund extraction (existing model)
2. SS payroll tax reform (remove income cap + restructure)
3. State wealth taxes (California, others)
4. Federal wealth tax
5. Financial transaction tax
6. Carbon tax
7. Safety net consolidation
8. Corporate equity contributions
9. Federal asset monetization
10. Induced economic effects (multiplier, tax revenue from UBI spending)

References:
- MIT Living Wage Calculator (2024)
- Saez & Zucman (2019) "The Triumph of Injustice" (wealth tax analysis)
- Summers & Sarin (2019) "A Wealth Tax is a Poor Idea" (counterargument)
- Piketty (2014) "Capital in the Twenty-First Century" (wealth concentration)
- Widerquist (2018) cost estimates for various UBI proposals
"""

import numpy as np
from dataclasses import dataclass
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.parameters import *


# === LIVING WAGE PARAMETERS ===

US_ADULTS_18_PLUS = 258_000_000  # ~258M adults 18+
US_CHILDREN = US_POPULATION - US_ADULTS_18_PLUS  # ~72M under 18

# Living wage targets (monthly, per adult)
LIVING_WAGE_LOW = 1_500   # Bare minimum (near poverty line)
LIVING_WAGE_MID = 2_200   # MIT living wage (national avg, single adult)
LIVING_WAGE_HIGH = 3_000  # Comfortable in most metros

# Annual cost at each level (adults only)
COST_LOW = LIVING_WAGE_LOW * 12 * US_ADULTS_18_PLUS    # ~$4.6T
COST_MID = LIVING_WAGE_MID * 12 * US_ADULTS_18_PLUS    # ~$6.8T
COST_HIGH = LIVING_WAGE_HIGH * 12 * US_ADULTS_18_PLUS   # ~$9.3T


@dataclass
class SSReformScenario:
    """Social Security reform parameters."""
    # Current SS payroll tax: 12.4% on first $168,600
    # Reform options:
    remove_income_cap: bool = True          # Tax ALL earnings
    additional_high_income_rate: float = 0.02  # Extra 2% on income > $400K
    increase_base_rate: float = 0.0         # Increase the 12.4% rate (0 = no change)
    raise_retirement_age: bool = False      # Raise FRA to 69
    means_test_benefits: bool = False       # Reduce benefits for high-income retirees

    @property
    def new_revenue_from_cap_removal(self) -> float:
        """
        Revenue from removing the $168,600 payroll tax cap.

        Currently ~6% of earnings are above the cap.
        Total US wages: ~$11.5T
        Earnings above cap: ~$2.5T
        New revenue: $2.5T * 12.4% = ~$310B/year

        Sources: SSA Office of the Chief Actuary, CBO (2024)
        """
        total_us_wages = 11.5e12
        earnings_above_cap = 2.5e12
        if self.remove_income_cap:
            return earnings_above_cap * SS_PAYROLL_TAX_RATE
        return 0

    @property
    def new_revenue_from_high_income_surtax(self) -> float:
        """
        Revenue from additional surtax on income > $400K.

        ~7M tax filers have AGI > $400K, total income ~$4.5T.
        Income above $400K: ~$3T
        """
        high_income_above_threshold = 3e12
        return high_income_above_threshold * self.additional_high_income_rate

    @property
    def total_new_ss_revenue(self) -> float:
        return (self.new_revenue_from_cap_removal +
                self.new_revenue_from_high_income_surtax +
                SS_TOTAL_ANNUAL_REVENUE * self.increase_base_rate / SS_PAYROLL_TAX_RATE)


@dataclass
class WealthTaxScenario:
    """Wealth tax parameters — federal and state."""

    # US household wealth: ~$150T (Federal Reserve Z.1)
    total_household_wealth: float = 150e12

    # Wealth distribution (Survey of Consumer Finances 2022)
    # Top 1%: ~32% of wealth = ~$48T
    # Top 0.1%: ~15% of wealth = ~$22.5T
    # Top 0.01%: ~7% of wealth = ~$10.5T
    top_1pct_wealth: float = 48e12
    top_01pct_wealth: float = 22.5e12
    top_001pct_wealth: float = 10.5e12

    # Federal wealth tax (Saez-Zucman / Warren proposal style)
    federal_wealth_tax_enabled: bool = True
    federal_rate_above_50m: float = 0.02   # 2% on wealth > $50M
    federal_rate_above_1b: float = 0.03    # 3% on wealth > $1B

    # Wealth above thresholds
    wealth_above_50m: float = 25e12        # ~$25T held by those with > $50M
    wealth_above_1b: float = 5.5e12        # ~$5.5T held by billionaires

    # State wealth taxes
    # California ACA 3 (proposed): 1.5% on wealth > $1B (residents)
    # Other states considering: NY, WA, CT, IL, MN, HI
    california_wealth_tax_enabled: bool = True
    california_rate: float = 0.015          # 1.5% on wealth > $1B
    california_billionaire_wealth: float = 600e9  # CA billionaire wealth

    other_state_taxes_enabled: bool = True
    other_state_combined_revenue: float = 15e9  # Estimated from NY, WA, etc.

    # Behavioral response / avoidance
    avoidance_rate: float = 0.25  # 25% of theoretical revenue lost to avoidance
    # Based on Saez-Zucman estimate of 15-35% evasion for wealth taxes

    @property
    def federal_wealth_tax_revenue(self) -> float:
        """Federal wealth tax revenue after avoidance."""
        if not self.federal_wealth_tax_enabled:
            return 0
        gross = (self.wealth_above_50m * self.federal_rate_above_50m +
                 self.wealth_above_1b * (self.federal_rate_above_1b - self.federal_rate_above_50m))
        return gross * (1 - self.avoidance_rate)

    @property
    def california_wealth_tax_revenue(self) -> float:
        if not self.california_wealth_tax_enabled:
            return 0
        return self.california_billionaire_wealth * self.california_rate * (1 - self.avoidance_rate)

    @property
    def total_state_wealth_tax_revenue(self) -> float:
        ca = self.california_wealth_tax_revenue
        other = self.other_state_combined_revenue if self.other_state_taxes_enabled else 0
        return ca + other

    @property
    def total_wealth_tax_revenue(self) -> float:
        return self.federal_wealth_tax_revenue + self.total_state_wealth_tax_revenue


@dataclass
class CarbonTaxScenario:
    """Carbon tax parameters."""
    # US CO2 emissions: ~5B metric tons/year (declining ~1%/year)
    annual_emissions_mt: float = 5e9
    tax_per_ton: float = 50  # $50/ton (Citizens Climate Lobby proposal)
    annual_decline_rate: float = 0.02  # Emissions decline 2%/year from tax

    @property
    def annual_revenue(self) -> float:
        return self.annual_emissions_mt * self.tax_per_ton * (1 - self.annual_decline_rate * 5)
        # Adjusted for ~5 year average behavioral response


class LivingWageModel:
    """
    Comprehensive model for funding a living-wage UBI.

    Computes the total revenue stack needed to fund $2,200/month
    for all 258M US adults, and shows the gap analysis.
    """

    def __init__(self,
                 target_monthly: float = LIVING_WAGE_MID,
                 ss_reform: SSReformScenario = None,
                 wealth_tax: WealthTaxScenario = None,
                 carbon_tax: CarbonTaxScenario = None,
                 sovereign_fund_size: float = 10e12,
                 sovereign_withdrawal_rate: float = 0.035):

        self.target_monthly = target_monthly
        self.target_annual = target_monthly * 12
        self.total_cost = self.target_annual * US_ADULTS_18_PLUS

        self.ss_reform = ss_reform or SSReformScenario()
        self.wealth_tax = wealth_tax or WealthTaxScenario()
        self.carbon_tax = carbon_tax or CarbonTaxScenario()
        self.fund_size = sovereign_fund_size
        self.withdrawal_rate = sovereign_withdrawal_rate

    def compute_revenue_stack(self) -> dict:
        """
        Compute all revenue sources and the gap to full living wage.
        """
        sources = {}

        # 1. Sovereign Wealth Fund (equity premium extraction)
        # GE-adjusted: reduce expected return for fund's own price impact
        erp_compression = ERP_COMPRESSION_PER_TRILLION * (self.fund_size / 1e12)
        effective_return = max(EQUITY_RISK_PREMIUM_MEAN - erp_compression, 0.02) + RISK_FREE_RATE_REAL
        fund_revenue = self.fund_size * self.withdrawal_rate
        sources['Sovereign Fund Withdrawals'] = {
            'revenue': fund_revenue,
            'notes': f'${self.fund_size/1e12:.0f}T fund at {self.withdrawal_rate:.1%} withdrawal',
            'feasibility': 0.6,
            'timeline_years': 20,
        }

        # 2. SS Payroll Tax Reform
        ss_new = self.ss_reform.total_new_ss_revenue
        # Of this, part goes to shore up SS, part is "freed up" for UBI
        # If SS is solvent, the new revenue exceeds SS deficit -> surplus to UBI
        ss_surplus_for_ubi = max(ss_new - SS_ANNUAL_DEFICIT, 0)
        sources['SS Payroll Tax Reform (cap removal + surtax)'] = {
            'revenue': ss_new,
            'revenue_available_for_ubi': ss_surplus_for_ubi,
            'ss_deficit_covered': min(ss_new, SS_ANNUAL_DEFICIT),
            'notes': (f'Remove ${SS_PAYROLL_TAX_RATE:.1%} cap: +${self.ss_reform.new_revenue_from_cap_removal/1e9:.0f}B, '
                      f'2% surtax >$400K: +${self.ss_reform.new_revenue_from_high_income_surtax/1e9:.0f}B'),
            'feasibility': 0.5,
            'timeline_years': 3,
        }

        # 3. Federal Wealth Tax
        sources['Federal Wealth Tax'] = {
            'revenue': self.wealth_tax.federal_wealth_tax_revenue,
            'notes': (f'{self.wealth_tax.federal_rate_above_50m:.0%} on >$50M, '
                      f'{self.wealth_tax.federal_rate_above_1b:.0%} on >$1B '
                      f'(after {self.wealth_tax.avoidance_rate:.0%} avoidance)'),
            'feasibility': 0.3,
            'timeline_years': 5,
        }

        # 4. State Wealth Taxes (CA + others)
        sources['State Wealth Taxes (CA + others)'] = {
            'revenue': self.wealth_tax.total_state_wealth_tax_revenue,
            'notes': f'CA 1.5% on billionaires + NY, WA, etc.',
            'feasibility': 0.4,
            'timeline_years': 3,
        }

        # 5. Financial Transaction Tax
        # Use 5bps as realistic rate
        ftt_baseline_cost = EFFECTIVE_SPREAD_BPS / 10000
        ftt_rate = 0.0005  # 5 bps
        ftt_cost_increase = ftt_rate / ftt_baseline_cost
        ftt_vol_change = VOLUME_ELASTICITY_MID * ftt_cost_increase
        ftt_new_vol = ANNUAL_EQUITY_VOLUME * max(1 + ftt_vol_change, 0.1)
        ftt_revenue = ftt_rate * ftt_new_vol * 2
        sources['Financial Transaction Tax (5bps)'] = {
            'revenue': ftt_revenue,
            'notes': f'5bps on equity trades, volume elasticity {VOLUME_ELASTICITY_MID}',
            'feasibility': 0.4,
            'timeline_years': 3,
        }

        # 6. Carbon Tax
        sources['Carbon Tax ($50/ton)'] = {
            'revenue': self.carbon_tax.annual_revenue,
            'notes': f'${self.carbon_tax.tax_per_ton}/ton CO2, declining emissions',
            'feasibility': 0.35,
            'timeline_years': 3,
        }

        # 7. Safety Net Consolidation
        # SNAP, SSI (partial), EITC (partial), TANF, Housing (partial)
        snap = 110e9
        ssi_partial = 30e9
        eitc_partial = 18e9
        tanf = 16e9
        housing_partial = 11e9
        admin_savings = (snap + ssi_partial + eitc_partial + tanf + housing_partial) * 0.05
        consolidation = snap + ssi_partial + eitc_partial + tanf + housing_partial + admin_savings
        sources['Safety Net Consolidation'] = {
            'revenue': consolidation,
            'notes': 'SNAP + SSI(partial) + EITC(partial) + TANF + Housing(partial) + admin savings',
            'feasibility': 0.5,
            'timeline_years': 5,
        }

        # 8. Corporate Equity Contributions (Meidner-style)
        corp_profits = 2e12
        corp_rate = 0.03  # 3% of profits as equity to sovereign fund
        # This produces fund growth, not immediate revenue; annualize as dividend
        corp_equity_annual = corp_profits * corp_rate
        sources['Corporate Equity Contributions (3%)'] = {
            'revenue': corp_equity_annual,
            'notes': '3% of corporate profits contributed as equity (Meidner-style)',
            'feasibility': 0.2,
            'timeline_years': 10,
        }

        # 9. Federal Asset Monetization
        federal_assets = 29.5e9
        sources['Federal Asset Monetization'] = {
            'revenue': federal_assets,
            'notes': 'Spectrum auctions, mineral rights, land leases, data licensing',
            'feasibility': 0.6,
            'timeline_years': 3,
        }

        # 10. Existing income tax on high earners receiving UBI
        # ~15% of UBI flows to people in tax brackets that effectively return it
        tax_clawback = self.total_cost * 0.15
        sources['Tax Clawback (high earners)'] = {
            'revenue': tax_clawback,
            'notes': '~15% of UBI paid to high-income adults returned via income tax',
            'feasibility': 0.9,
            'timeline_years': 1,
        }

        # 11. Economic multiplier effects
        # UBI spending creates economic activity -> tax revenue
        mpc = 0.65
        consumption_boost = self.total_cost * mpc
        induced_tax = consumption_boost * 0.15
        sources['Induced Tax Revenue (economic multiplier)'] = {
            'revenue': induced_tax,
            'notes': f'MPC={mpc:.0%}, 15% effective tax on induced consumption',
            'feasibility': 0.8,
            'timeline_years': 2,
        }

        # === TOTALS ===
        total_revenue = sum(s['revenue'] for s in sources.values())
        gap = self.total_cost - total_revenue

        # Split by timeline
        year1_sources = {k: v for k, v in sources.items() if v['timeline_years'] <= 3}
        year1_revenue = sum(s['revenue'] for s in year1_sources.values())

        return {
            'target_monthly': self.target_monthly,
            'target_annual_per_person': self.target_annual,
            'total_annual_cost': self.total_cost,
            'total_cost_pct_gdp': self.total_cost / GDP_US,
            'adults_covered': US_ADULTS_18_PLUS,
            'sources': sources,
            'total_revenue': total_revenue,
            'gap': gap,
            'gap_pct': gap / self.total_cost if self.total_cost > 0 else 0,
            'funded_pct': total_revenue / self.total_cost if self.total_cost > 0 else 0,
            'year1_revenue': year1_revenue,
            'year1_gap': self.total_cost - year1_revenue,
            'year1_funded_pct': year1_revenue / self.total_cost,
        }

    def scenario_year1(self) -> dict:
        """
        What can be funded at Year 1 (no sovereign fund yet)?

        Only includes revenue sources achievable in 1-3 years:
        - SS payroll tax reform (legislation)
        - Wealth taxes (federal + state)
        - FTT
        - Carbon tax
        - Safety net consolidation
        - Tax clawback
        - Induced economic effects
        """
        stack = self.compute_revenue_stack()
        year1_sources = {k: v for k, v in stack['sources'].items()
                        if v['timeline_years'] <= 3}

        year1_total = sum(s['revenue'] for s in year1_sources.values())

        # What monthly UBI can Year 1 revenue support?
        affordable_annual = year1_total / US_ADULTS_18_PLUS
        affordable_monthly = affordable_annual / 12

        return {
            'available_revenue': year1_total,
            'affordable_monthly_ubi': affordable_monthly,
            'target_monthly': self.target_monthly,
            'funding_gap_monthly': self.target_monthly - affordable_monthly,
            'funding_pct': affordable_monthly / self.target_monthly,
            'sources': year1_sources,
        }

    def scenario_ss_collapse(self, collapse_year_offset: int = 10) -> dict:
        """
        What happens at SS trust fund depletion (~2033-2035)?

        At depletion:
        - SS benefits cut to ~77% (payable from ongoing revenue)
        - ~67M beneficiaries lose ~$440/month average
        - Political crisis creates window for reform

        This model shows how the sovereign fund + reforms can:
        1. Prevent the SS benefit cut
        2. Provide UBI on top
        """
        # SS shortfall at depletion: ~23% of outlays
        ss_outlays_at_collapse = SS_TOTAL_ANNUAL_OUTLAYS * (1.03 ** collapse_year_offset)
        ss_shortfall = ss_outlays_at_collapse * (1 - SS_POST_DEPLETION_BENEFIT_PCT)

        # By year 10, sovereign fund has been accumulating
        # Assume $250B/year contributions + 6.5% returns for 10 years
        annual_contribution = 250e9
        fund_at_collapse = 0
        for yr in range(collapse_year_offset):
            fund_at_collapse = (fund_at_collapse + annual_contribution) * (1 + EQUITY_REAL_RETURN_MEAN)

        fund_withdrawal_for_ss = min(fund_at_collapse * self.withdrawal_rate, ss_shortfall)

        # SS reform revenue by then
        ss_reform_revenue = self.ss_reform.total_new_ss_revenue * (1.02 ** collapse_year_offset)

        # Can we cover the shortfall?
        total_ss_rescue = fund_withdrawal_for_ss + ss_reform_revenue
        ss_fully_covered = total_ss_rescue >= ss_shortfall

        # Remaining fund withdrawal available for UBI
        remaining_for_ubi = max(fund_at_collapse * self.withdrawal_rate - fund_withdrawal_for_ss, 0)

        # Other revenue sources by year 10
        wealth_tax = self.wealth_tax.total_wealth_tax_revenue * (1.03 ** collapse_year_offset)
        ftt = 15e9 * (1.02 ** collapse_year_offset)
        carbon = self.carbon_tax.annual_revenue * (0.98 ** collapse_year_offset)  # Declining emissions
        consolidation = 194e9 * (1.02 ** collapse_year_offset)

        total_for_ubi = remaining_for_ubi + wealth_tax + ftt + carbon + consolidation
        affordable_monthly = (total_for_ubi / US_ADULTS_18_PLUS) / 12

        return {
            'collapse_year_offset': collapse_year_offset,
            'calendar_year': 2024 + collapse_year_offset,
            'ss_outlays_at_collapse': ss_outlays_at_collapse,
            'ss_shortfall': ss_shortfall,
            'sovereign_fund_at_collapse': fund_at_collapse,
            'fund_withdrawal_for_ss': fund_withdrawal_for_ss,
            'ss_reform_revenue': ss_reform_revenue,
            'ss_fully_covered': ss_fully_covered,
            'total_for_ubi': total_for_ubi,
            'affordable_monthly_ubi': affordable_monthly,
            'combined_retiree_benefit': SS_AVG_RETIRED_BENEFIT_MONTHLY + affordable_monthly,
        }


def run_living_wage_analysis():
    """Full living wage feasibility analysis."""
    print("=" * 80)
    print("LIVING WAGE UBI — FULL FEASIBILITY ANALYSIS")
    print("=" * 80)

    print(f"\n  Target: ${LIVING_WAGE_MID:,}/month for all {US_ADULTS_18_PLUS/1e6:.0f}M US adults (18+)")
    print(f"  Annual cost: ${COST_MID/1e12:.2f}T ({COST_MID/GDP_US:.1%} of GDP)")
    print(f"  For context: Total current federal spending: ${FEDERAL_BUDGET/1e12:.1f}T")
    print(f"               Total current safety net:       ${TOTAL_SAFETY_NET/1e12:.1f}T")

    # === Full Revenue Stack ===
    print(f"\n\n{'='*80}")
    print("FULL REVENUE STACK — ALL SOURCES")
    print(f"{'='*80}")

    model = LivingWageModel(target_monthly=LIVING_WAGE_MID)
    stack = model.compute_revenue_stack()

    print(f"\n  {'Source':<45} {'Revenue':>12} {'Timeline':>10} {'Feas.':>7}")
    print("  " + "-" * 78)

    for name, src in stack['sources'].items():
        print(f"  {name:<45} ${src['revenue']/1e9:>10.1f}B "
              f"{'Y'+str(src['timeline_years']):>9} {src['feasibility']:>6.0%}")

    print("  " + "=" * 78)
    print(f"  {'TOTAL REVENUE':<45} ${stack['total_revenue']/1e9:>10.1f}B")
    print(f"  {'TOTAL COST':<45} ${stack['total_annual_cost']/1e9:>10.1f}B")
    print(f"  {'GAP':<45} ${stack['gap']/1e9:>10.1f}B")
    print(f"  {'FUNDED':<45} {stack['funded_pct']:>10.1%}")

    # Affordable UBI from available revenue
    affordable = (stack['total_revenue'] / US_ADULTS_18_PLUS) / 12
    print(f"\n  With ALL sources (including 20yr sovereign fund):")
    print(f"    Affordable UBI: ${affordable:,.0f}/month per adult")
    print(f"    Gap to living wage: ${LIVING_WAGE_MID - affordable:,.0f}/month")

    # === Year 1 Scenario ===
    print(f"\n\n{'='*80}")
    print("YEAR 1 SCENARIO — What's possible immediately?")
    print(f"{'='*80}")

    yr1 = model.scenario_year1()
    print(f"\n  Revenue available in Year 1-3: ${yr1['available_revenue']/1e9:,.0f}B")
    print(f"  Affordable UBI (Year 1):       ${yr1['affordable_monthly_ubi']:,.0f}/month per adult")
    print(f"  Funding gap to ${LIVING_WAGE_MID}:       ${yr1['funding_gap_monthly']:,.0f}/month")
    print(f"  Funded:                         {yr1['funding_pct']:.1%}")

    print(f"\n  Year 1 Sources:")
    for name, src in yr1['sources'].items():
        print(f"    {name:<45} ${src['revenue']/1e9:>10.1f}B")

    # === SS Collapse Scenario ===
    print(f"\n\n{'='*80}")
    print("SS COLLAPSE SCENARIO — Trust fund depletion (~2034)")
    print(f"{'='*80}")

    for offset in [8, 10, 12]:
        ss = model.scenario_ss_collapse(collapse_year_offset=offset)
        print(f"\n  --- Collapse at Year {offset} ({ss['calendar_year']}) ---")
        print(f"  Sovereign fund accumulated:   ${ss['sovereign_fund_at_collapse']/1e12:.2f}T")
        print(f"  SS shortfall at collapse:     ${ss['ss_shortfall']/1e9:.0f}B/yr")
        print(f"  Fund withdrawal for SS:       ${ss['fund_withdrawal_for_ss']/1e9:.0f}B/yr")
        print(f"  SS reform revenue:            ${ss['ss_reform_revenue']/1e9:.0f}B/yr")
        print(f"  SS fully covered:              {'YES' if ss['ss_fully_covered'] else 'NO'}")
        print(f"  Remaining for UBI:            ${ss['total_for_ubi']/1e9:.0f}B/yr")
        print(f"  Affordable UBI:               ${ss['affordable_monthly_ubi']:.0f}/month")
        print(f"  Retiree total (SS + UBI):     ${ss['combined_retiree_benefit']:.0f}/month")

    # === What It Actually Takes ===
    print(f"\n\n{'='*80}")
    print("REALITY CHECK — WHAT $2,200/MONTH ACTUALLY REQUIRES")
    print(f"{'='*80}")
    print(f"""
  Total cost: ${COST_MID/1e12:.1f}T/year = {COST_MID/GDP_US:.0%} of GDP

  For comparison:
    Current federal spending:     ${FEDERAL_BUDGET/1e12:.1f}T  (23% of GDP)
    Current total safety net:     ${TOTAL_SAFETY_NET/1e12:.1f}T  (12% of GDP)
    Total US tax revenue (all):   ~$7.6T  (27% of GDP)
    Total US corporate profits:   ~$2.0T

  The honest math:
    All revenue sources combined:     ${stack['total_revenue']/1e12:.1f}T
    Gap:                              ${stack['gap']/1e12:.1f}T
    This gap = {abs(stack['gap'])/GDP_US:.0%} of GDP

  Three paths to close the gap:

  PATH A: Higher taxes across the board
    - Increase ALL federal income tax rates by ~8 percentage points
    - Revenue: ~$1.5T additional
    - Political feasibility: Very low

  PATH B: Much larger sovereign fund (30+ year horizon)
    - $30T fund at 3.5% = $1.05T/year
    - Requires 30-40 years of accumulation
    - Combined with other sources: closes gap at maturity

  PATH C: Phased approach (RECOMMENDED)
    - Year 1-5:   ${yr1['affordable_monthly_ubi']:.0f}/month (from tax reforms)
    - Year 10-15: $400-600/month (fund growing + all tax revenue)
    - Year 20-30: $800-1,200/month (mature fund)
    - Year 30-40: $1,500-2,200/month (compound growth)

  The $2,200/month living wage is achievable but requires a
  GENERATIONAL commitment — 30+ years of compound growth.
  The Year 1 number is ${yr1['affordable_monthly_ubi']:.0f}/month.
  That's not nothing — it's real money for real people.
""")

    # === Sensitivity: How much does uncapping SS help? ===
    print(f"\n{'='*80}")
    print("SENSITIVITY: SS PAYROLL TAX CAP REMOVAL")
    print(f"{'='*80}")

    for extra_rate in [0.0, 0.02, 0.04, 0.06]:
        reform = SSReformScenario(
            remove_income_cap=True,
            additional_high_income_rate=extra_rate,
        )
        print(f"\n  Cap removed + {extra_rate:.0%} surtax on >$400K:")
        print(f"    New SS revenue:         ${reform.total_new_ss_revenue/1e9:.0f}B/yr")
        print(f"    SS deficit covered:     ${min(reform.total_new_ss_revenue, SS_ANNUAL_DEFICIT)/1e9:.0f}B")
        surplus = max(reform.total_new_ss_revenue - SS_ANNUAL_DEFICIT, 0)
        print(f"    Surplus available:      ${surplus/1e9:.0f}B/yr")
        if surplus > 0:
            ubi_from_surplus = (surplus / US_ADULTS_18_PLUS) / 12
            print(f"    UBI from surplus alone: ${ubi_from_surplus:.0f}/month")


if __name__ == '__main__':
    run_living_wage_analysis()
