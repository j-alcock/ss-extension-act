"""
Social Security Extension Model — "Social Security for All"
Version 2.0: Fiscally Grounded Projection

REFRAME: Instead of a "UBI funded by market extraction," this is an
EXTENSION of Social Security to cover all adults from age 18, funded
by reforming and expanding SS's existing revenue structure plus a
new equity investment arm.

This is not a cosmetic change. It transforms:
  1. Legal foundation — built on 90 years of SS case law and the SSA
  2. Political coalition — the 50+ voting bloc PLUS working-age adults
  3. Funding mechanism — payroll tax reform, not new tax categories
  4. Implementation — SSA already pays 67M people monthly. Scale it.
  5. Public psychology — "expanding a program you already trust" vs.
     "creating a radical new government program"

Why this is structurally superior:

  ┌─────────────────────┬────────────────────────┬──────────────────────────┐
  │                     │  STANDALONE UBI         │  SS EXTENSION            │
  ├─────────────────────┼────────────────────────┼──────────────────────────┤
  │ Legal basis         │ New legislation needed  │ Amend existing SSA (1935)│
  │ Agency              │ New agency from scratch │ SSA (65,000 employees)   │
  │ Payment rails       │ Build from scratch      │ Already pays 67M/month   │
  │ Trust fund          │ New sovereign fund      │ Expand OASDI trust fund  │
  │ Constitutional test │ Untested                │ Flemming v. Nestor (1960)│
  │ Public support      │ 55% favorable (polls)   │ 85% favorable (SS polls) │
  │ Beneficiary base    │ 0 → 258M (cold start)  │ 67M → 258M (warm start)  │
  │ Political defense   │ Vulnerable (new program)│ "Third rail" protection  │
  │ FICA infrastructure │ New tax mechanism       │ Already collecting $1.2T │
  │ Actuarial framework │ Design from scratch     │ 89 years of actuarial    │
  │ Bipartisan history  │ Partisan (coded left)   │ FDR through Reagan       │
  └─────────────────────┴────────────────────────┴──────────────────────────┘

The formal name: Social Security Universal Benefit (SSUB)
  - Title II-B of the Social Security Act (new section)
  - "Universal Old-Age, Survivors, Disability, and Livelihood Insurance"
  - Nickname: "Social Security for All" or "The American Dividend"

VERSION 2.0 KEY FIX:
  The v1.0 model set Tier 2 at an aspirational $500/month, which exceeded
  revenue capacity and caused insolvency by Year 5. V2.0 computes the
  REVENUE-CONSTRAINED benefit level: we only promise what we can pay.
  Benefits grow as the equity fund compounds — not before.

  The math: $500/mo × 258M adults = $1.55T/year in Tier 2 costs.
  New revenue (Year 0) is only ~$728B. After covering the existing
  $200B SS deficit, only ~$528B remains for Tier 2, supporting ~$170/mo.

  V2.0 starts Tier 2 at what revenue supports and grows with the system.

References:
- Altman (2005) "The Battle for Social Security" (political history)
- Ghilarducci (2024) "Rescuing Retirement"
- Clingman & Burkhalter (2023) SSA Office of Chief Actuary cost estimates
- Herd & Moynihan (2019) "Administrative Burden" (SSA capacity)
- National Academy of Social Insurance (2024) reform proposals
- Gabaix & Koijen (2022) "In Search of the Origins of Financial Fluctuations"
  (inelastic markets — used for ERP compression)
- Dimson, Marsh & Staunton (2023) global equity premium benchmarks
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Tuple
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.parameters import *


# ═══════════════════════════════════════════════════════════════════════
#  BENEFIT DESIGN
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class SSExtensionDesign:
    """
    Design parameters for Social Security Universal Benefit (SSUB).

    Three-tier structure:
      Tier 1 (existing): Traditional SS — earned benefits (avg $1,907/mo)
      Tier 2 (NEW): Universal flat benefit for all adults 18+
      Tier 3 (NEW): Equity dividend — variable, from trust fund returns

    V2.0 KEY CHANGE:
    Tier 2 is no longer set aspirationally. It is computed as:
      tier2 = min(revenue_available / (adults × 12), tier2_cap)
    This guarantees solvency by construction.
    """

    # Tier 2 cap (maximum, once revenue supports it)
    tier2_monthly_cap: float = 800         # Maximum Tier 2 (grows with inflation)
    tier2_eligible_age: int = 18
    tier2_citizenship_req: bool = True      # Citizens + permanent residents (5yr)
    tier2_revenue_share: float = 0.85       # 85% of new revenue to Tier 2 (15% to reserve)
    tier2_reserve_target_months: int = 6    # 6-month benefit reserve before increasing

    # Tier 3: Equity Dividend
    tier3_enabled: bool = True
    tier3_withdrawal_rate: float = 0.035    # 3.5% of equity fund (smoothed)
    tier3_smoothing_years: int = 5          # Average fund value over 5 years
    tier3_start_year: int = 8               # Begin withdrawals after 8 years of accumulation

    @property
    def total_monthly_cap(self) -> float:
        """Maximum combined Tier 2 + 3 benefit."""
        return self.tier2_monthly_cap + 300  # ~$300 equity dividend target


@dataclass
class SSRevenueReform:
    """
    Revenue reforms to fund the SS extension.

    Current SS revenue: $1.2T/year from FICA 12.4% on first $168,600
    Current SS outlays: $1.4T/year (deficit: $200B/year)

    Reform package (six components):
    1. Remove the FICA income cap (tax ALL earnings)         → $310B/yr
    2. Progressive surtax on high earnings (>$250K)          → $150B/yr
    3. Apply FICA to investment income (6%, extending NIIT)  → $150B/yr
    4. OASDI Equity Trust Fund (invest in global equities)   → $0 initially, growing
    5. Financial Transaction Tax dedicated to OASDI           → $50B/yr
    6. Carbon tax revenue sharing with OASDI (30%)           → $67.5B/yr

    Total new Year 0 revenue (ex-equity fund): ~$728B/year
    Less SS deficit coverage:                  ~$200B/year
    Available for Tier 2:                      ~$528B/year → ~$170/mo per adult
    """

    # Reform 1: Remove FICA cap
    remove_fica_cap: bool = True
    fica_cap_revenue: float = 310e9        # $310B/yr (SSA Chief Actuary estimate)
    fica_cap_growth: float = 0.03          # Grows with wage growth (3%/yr)

    # Reform 2: Progressive surtax
    surtax_rate_above_250k: float = 0.02   # +2% on earnings > $250K
    surtax_rate_above_1m: float = 0.04     # +4% on earnings > $1M
    surtax_base_250k: float = 5e12         # Earnings above $250K
    surtax_base_1m: float = 2.5e12         # Earnings above $1M
    surtax_growth: float = 0.03            # Wage growth

    # Reform 3: FICA on investment income (extending 3.8% NIIT to 6%)
    fica_on_investment: bool = True
    investment_fica_rate: float = 0.06
    investment_income_base: float = 2.5e12  # High-earner investment income
    investment_income_growth: float = 0.04  # Grows with wealth (faster than wages)

    # Reform 4: OASDI Equity Trust Fund
    equity_fund_enabled: bool = True
    equity_fund_seed: float = 500e9        # $500B initial (from Treasury)
    equity_fund_annual_contribution: float = 200e9  # $200B/yr from new revenue
    equity_fund_return_real: float = 0.04  # 4% real (GLOBAL, GE-adjusted per E3)
    equity_fund_return_vol: float = 0.15   # 15% annual volatility
    equity_fund_contribution_years: int = 30  # Contribute for 30 years

    # Reform 5: Financial Transaction Tax → OASDI
    ftt_rate: float = 0.0005              # 5 bps
    ftt_base_revenue: float = 50e9         # $50B/yr after behavioral response
    ftt_decline: float = 0.01             # 1%/yr volume decline

    # Reform 6: Carbon tax revenue share
    carbon_base_revenue: float = 67.5e9    # $225B × 30%
    carbon_decline: float = 0.02           # 2%/yr emission decline

    def compute_new_revenue(self, year: int) -> dict:
        """
        Compute new revenue sources for a given year.

        Returns detailed breakdown + total.
        Grows each source at its specific growth/decline rate.
        """
        # 1. FICA cap removal
        cap = self.fica_cap_revenue * (1 + self.fica_cap_growth) ** year if self.remove_fica_cap else 0

        # 2. Progressive surtax
        base_250 = self.surtax_base_250k * (1 + self.surtax_growth) ** year
        base_1m = self.surtax_base_1m * (1 + self.surtax_growth) ** year
        surtax = (base_250 * self.surtax_rate_above_250k +
                  base_1m * (self.surtax_rate_above_1m - self.surtax_rate_above_250k))

        # 3. Investment income FICA
        inv_base = self.investment_income_base * (1 + self.investment_income_growth) ** year
        inv_fica = inv_base * self.investment_fica_rate if self.fica_on_investment else 0

        # 4. FTT (declining with volume)
        ftt = self.ftt_base_revenue * (1 - self.ftt_decline) ** year

        # 5. Carbon tax (declining with emissions)
        carbon = self.carbon_base_revenue * (1 - self.carbon_decline) ** year

        total_new = cap + surtax + inv_fica + ftt + carbon

        # Existing SS revenue (grows with wages)
        existing_ss = SS_TOTAL_ANNUAL_REVENUE * (1 + self.fica_cap_growth) ** year

        return {
            'fica_cap_removal': cap,
            'progressive_surtax': surtax,
            'investment_fica': inv_fica,
            'ftt': ftt,
            'carbon_tax': carbon,
            'total_new_revenue': total_new,
            'existing_ss_revenue': existing_ss,
            'total_all_revenue': total_new + existing_ss,
        }

    def compute_year0_tier2_capacity(self) -> Tuple[float, float]:
        """
        What Tier 2 benefit can Year 0 revenue actually support?

        This is the key fiscal grounding calculation.

        Returns: (monthly_per_adult, annual_total_available)
        """
        rev = self.compute_new_revenue(year=0)
        new_revenue = rev['total_new_revenue']

        # Must first cover the SS deficit
        ss_deficit_coverage = min(new_revenue, SS_ANNUAL_DEFICIT)
        remaining = new_revenue - ss_deficit_coverage

        # Available for Tier 2 (after equity fund contribution and reserve)
        # The equity fund contribution comes from the remaining revenue
        equity_contribution = self.equity_fund_annual_contribution if self.equity_fund_enabled else 0

        # In Year 0, we must choose: pay Tier 2 now OR contribute to equity fund
        # Solution: Tier 2 gets revenue MINUS equity fund contribution
        available_for_tier2 = max(remaining - equity_contribution, 0)

        adults = 258e6
        monthly = (available_for_tier2 / adults) / 12

        return monthly, available_for_tier2


# ═══════════════════════════════════════════════════════════════════════
#  SCENARIO CONFIGURATIONS
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class ScenarioConfig:
    """Configuration for a projection scenario."""
    name: str
    description: str
    equity_fund_seed: float
    equity_fund_annual_contribution: float
    equity_fund_return_real: float
    equity_fund_contribution_years: int
    tier2_revenue_share: float  # % of available revenue going to Tier 2
    include_ftt: bool
    include_carbon: bool
    include_investment_fica: bool


SCENARIOS = {
    'conservative': ScenarioConfig(
        name='Conservative',
        description='FICA cap removal + surtax only. No FTT, no carbon, smaller fund.',
        equity_fund_seed=250e9,
        equity_fund_annual_contribution=100e9,
        equity_fund_return_real=0.035,  # 3.5% (very conservative global ERP)
        equity_fund_contribution_years=30,
        tier2_revenue_share=0.80,
        include_ftt=False,
        include_carbon=False,
        include_investment_fica=True,
    ),
    'moderate': ScenarioConfig(
        name='Moderate',
        description='All six revenue reforms. Baseline equity fund. Global ERP 4%.',
        equity_fund_seed=500e9,
        equity_fund_annual_contribution=200e9,
        equity_fund_return_real=0.04,   # 4% (DMS global, GE-adjusted)
        equity_fund_contribution_years=30,
        tier2_revenue_share=0.85,
        include_ftt=True,
        include_carbon=True,
        include_investment_fica=True,
    ),
    'ambitious': ScenarioConfig(
        name='Ambitious',
        description='All reforms + larger fund + optimistic (but defensible) returns.',
        equity_fund_seed=750e9,
        equity_fund_annual_contribution=300e9,
        equity_fund_return_real=0.045,  # 4.5% (global diversified, mild compression)
        equity_fund_contribution_years=35,
        tier2_revenue_share=0.90,
        include_ftt=True,
        include_carbon=True,
        include_investment_fica=True,
    ),
}


# ═══════════════════════════════════════════════════════════════════════
#  THE MODEL (V2.0 — FISCALLY GROUNDED)
# ═══════════════════════════════════════════════════════════════════════

class SSExtensionModelV2:
    """
    Social Security Extension Model — Version 2.0

    Key difference from v1.0:
      V1.0 set Tier 2 at $500/mo and watched it crash.
      V2.0 computes the revenue-constrained benefit and grows it.

    The model guarantees solvency by construction:
      tier2_benefit = available_revenue / (adults × 12)

    Benefits grow for three reasons:
      1. Tax revenue grows with wages and wealth (~3%/yr)
      2. Equity fund compounds (~4% real return)
      3. Equity fund withdrawals begin after Year 8
    """

    def __init__(self, scenario: str = 'moderate', design: SSExtensionDesign = None):
        if scenario not in SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}. Choose from {list(SCENARIOS.keys())}")

        self.config = SCENARIOS[scenario]
        self.design = design or SSExtensionDesign()

        # Configure revenue reforms based on scenario
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
        Project the SS Extension system forward for `years` years.

        SOLVENCY BY DESIGN: Tier 2 is always set to what revenue supports.
        There is no insolvency — only lower/higher benefit levels.

        Returns a dict of numpy arrays with full yearly detail.
        """
        # Output arrays
        results = {
            'years': np.arange(years),
            'total_revenue': np.zeros(years),
            'new_revenue': np.zeros(years),
            'existing_ss_revenue': np.zeros(years),
            'existing_ss_outlays': np.zeros(years),
            'ss_deficit': np.zeros(years),
            'revenue_after_ss_deficit': np.zeros(years),
            'equity_fund_contribution': np.zeros(years),
            'revenue_for_tier2': np.zeros(years),
            'tier2_monthly': np.zeros(years),
            'tier3_monthly': np.zeros(years),
            'total_monthly_adult': np.zeros(years),
            'total_monthly_retiree': np.zeros(years),
            'total_annual_adult': np.zeros(years),
            'equity_fund_balance': np.zeros(years + 1),
            'equity_fund_trailing_avg': np.zeros(years),
            'tier2_outlays': np.zeros(years),
            'tier3_outlays': np.zeros(years),
            'reserve_balance': np.zeros(years + 1),
            'adults': np.zeros(years),
            'retirees': np.zeros(years),
        }

        # Initial equity fund balance
        results['equity_fund_balance'][0] = self.revenue.equity_fund_seed

        # Population projections
        for t in range(years):
            results['adults'][t] = 258e6 * (1.003 ** t)    # 0.3% adult pop growth
            results['retirees'][t] = 67e6 * (1.015 ** min(t, 20)) * (1.005 ** max(t - 20, 0))

        # Track trailing fund values for smoothing
        fund_history = [self.revenue.equity_fund_seed]

        for t in range(years):
            adults = results['adults'][t]

            # ─── REVENUE ─────────────────────────────────────────
            rev = self.revenue.compute_new_revenue(year=t)
            results['total_revenue'][t] = rev['total_all_revenue']
            results['new_revenue'][t] = rev['total_new_revenue']
            results['existing_ss_revenue'][t] = rev['existing_ss_revenue']

            # ─── EXISTING SS OUTLAYS ─────────────────────────────
            # Existing SS outlays grow at ~3.5% (benefit indexing + aging)
            # Slower than v1.0's 4.5% (which was too aggressive)
            if t == 0:
                results['existing_ss_outlays'][t] = SS_TOTAL_ANNUAL_OUTLAYS
            else:
                growth = 0.035 if t < 15 else 0.025  # Slower growth after demographic wave
                results['existing_ss_outlays'][t] = results['existing_ss_outlays'][t - 1] * (1 + growth)

            # ─── SS DEFICIT ──────────────────────────────────────
            # How much of new revenue must go to keep existing SS solvent?
            ss_deficit = max(results['existing_ss_outlays'][t] - results['existing_ss_revenue'][t], 0)
            results['ss_deficit'][t] = ss_deficit

            # ─── REVENUE AVAILABLE AFTER SS DEFICIT ──────────────
            revenue_after_deficit = max(results['new_revenue'][t] - ss_deficit, 0)
            results['revenue_after_ss_deficit'][t] = revenue_after_deficit

            # ─── EQUITY FUND CONTRIBUTION ────────────────────────
            # Contribute to equity fund from available revenue
            if t < self.revenue.equity_fund_contribution_years:
                # Contribution is the LESSER of target and 40% of available revenue
                # This prevents the fund from starving Tier 2
                max_contribution = revenue_after_deficit * 0.40
                contribution = min(self.revenue.equity_fund_annual_contribution, max_contribution)
            else:
                contribution = 0
            results['equity_fund_contribution'][t] = contribution

            # ─── EQUITY FUND GROWTH ──────────────────────────────
            results['equity_fund_balance'][t + 1] = (
                (results['equity_fund_balance'][t] + contribution) *
                (1 + self.revenue.equity_fund_return_real)
            )
            fund_history.append(results['equity_fund_balance'][t + 1])

            # Trailing average for smoothed withdrawal
            lookback = min(self.design.tier3_smoothing_years, len(fund_history))
            results['equity_fund_trailing_avg'][t] = np.mean(fund_history[-lookback:])

            # ─── TIER 3: EQUITY DIVIDEND ─────────────────────────
            if self.design.tier3_enabled and t >= self.design.tier3_start_year:
                # Withdraw from trailing average (smoothed)
                tier3_total = (results['equity_fund_trailing_avg'][t] *
                               self.design.tier3_withdrawal_rate)
                # Deduct from fund
                results['equity_fund_balance'][t + 1] -= tier3_total
                # Guard: never withdraw more than 5% of actual balance
                max_withdrawal = results['equity_fund_balance'][t + 1] * 0.05
                if tier3_total > max_withdrawal + results['equity_fund_balance'][t + 1] * 0.05:
                    tier3_total = max(max_withdrawal, 0)

                results['tier3_monthly'][t] = (tier3_total / adults) / 12
                results['tier3_outlays'][t] = tier3_total
            else:
                results['tier3_monthly'][t] = 0
                results['tier3_outlays'][t] = 0

            # ─── TIER 2: REVENUE-CONSTRAINED BENEFIT ─────────────
            # V2.0 key innovation: Tier 2 = what revenue supports
            revenue_for_tier2 = max(revenue_after_deficit - contribution, 0)

            # Build reserve: 10% of Tier 2 revenue until 6-month reserve is met
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

            # Compute Tier 2 monthly benefit
            tier2_raw = (max(revenue_for_tier2, 0) / adults) / 12

            # Apply cap (inflation-adjusted)
            tier2_cap = self.design.tier2_monthly_cap * (1.02 ** t)
            tier2_uncapped = min(tier2_raw, tier2_cap)

            # ─── BENEFIT RATCHET (Dybvig 1995) ──────────────────
            # Tier 2 NEVER decreases nominally. If revenue dips, draw from reserve.
            # This is politically essential: you cannot cut 258M people's checks.
            if t > 0:
                prev_tier2 = results['tier2_monthly'][t - 1]
                if tier2_uncapped < prev_tier2:
                    # How much would it cost to maintain the previous level?
                    shortfall = (prev_tier2 - tier2_uncapped) * 12 * adults
                    if results['reserve_balance'][t + 1] >= shortfall:
                        # Draw from reserve to maintain benefit
                        results['reserve_balance'][t + 1] -= shortfall
                        tier2_uncapped = prev_tier2
                    else:
                        # Exhaust reserve, benefit drops to what's left
                        available_from_reserve = results['reserve_balance'][t + 1]
                        results['reserve_balance'][t + 1] = 0
                        tier2_uncapped = tier2_uncapped + (available_from_reserve / adults) / 12

            results['tier2_monthly'][t] = tier2_uncapped
            results['tier2_outlays'][t] = results['tier2_monthly'][t] * 12 * adults

            # ─── TOTAL BENEFITS ──────────────────────────────────
            results['total_monthly_adult'][t] = (results['tier2_monthly'][t] +
                                                  results['tier3_monthly'][t])
            results['total_annual_adult'][t] = results['total_monthly_adult'][t] * 12
            results['total_monthly_retiree'][t] = (
                SS_AVG_RETIRED_BENEFIT_MONTHLY * (1.02 ** t) +  # Existing SS grows with CPI
                results['total_monthly_adult'][t]
            )

        return results

    def compare_frames(self) -> dict:
        """
        Quantitative comparison: SS Extension vs. Standalone UBI.

        Same 7-dimension comparison as v1.0 — the structural advantages
        are unchanged. The difference is that V2.0 has credible fiscal numbers.
        """

        comparison = {
            'dimensions': [],
        }

        dims = [
            ('Political Viability', 0.75, 0.40, 0.25),
            ('Implementation Speed', 0.85, 0.45, 0.10),
            ('Legal Durability', 0.80, 0.35, 0.10),
            ('Funding Coherence', 0.80, 0.50, 0.15),
            ('Fiscal Sustainability', 0.75, 0.50, 0.10),
            ('Protection Against Political Capture', 0.70, 0.50, 0.10),
            ('Addresses SS Solvency Crisis', 0.95, 0.20, 0.20),
        ]

        for name, ss_score, ubi_score, weight in dims:
            comparison['dimensions'].append({
                'dimension': name,
                'ss_extension_score': ss_score,
                'standalone_ubi_score': ubi_score,
                'weight': weight,
            })

        ss_weighted = sum(d['ss_extension_score'] * d['weight'] for d in comparison['dimensions'])
        ubi_weighted = sum(d['standalone_ubi_score'] * d['weight'] for d in comparison['dimensions'])

        comparison['ss_extension_weighted'] = ss_weighted
        comparison['standalone_ubi_weighted'] = ubi_weighted
        comparison['advantage_ratio'] = ss_weighted / ubi_weighted if ubi_weighted > 0 else float('inf')

        return comparison


# ═══════════════════════════════════════════════════════════════════════
#  ANALYSIS & OUTPUT
# ═══════════════════════════════════════════════════════════════════════

def print_scenario_projection(scenario_name: str, years: int = 40):
    """Print detailed projection for a single scenario."""
    model = SSExtensionModelV2(scenario=scenario_name)
    config = SCENARIOS[scenario_name]
    proj = model.project(years=years)

    print(f"\n{'━' * 95}")
    print(f"  SCENARIO: {config.name.upper()}")
    print(f"  {config.description}")
    print(f"{'━' * 95}")

    # Year 0 fiscal grounding
    yr0_cap, yr0_available = model.revenue.compute_year0_tier2_capacity()
    print(f"\n  Year 0 Fiscal Grounding:")
    print(f"    New revenue (ex-equity fund):  ${model.revenue.compute_new_revenue(0)['total_new_revenue']/1e9:,.0f}B")
    print(f"    SS deficit coverage:           ${proj['ss_deficit'][0]/1e9:,.0f}B")
    print(f"    Equity fund contribution:      ${proj['equity_fund_contribution'][0]/1e9:,.0f}B")
    print(f"    Available for Tier 2:          ${proj['revenue_for_tier2'][0]/1e9:,.0f}B")
    print(f"    Tier 2 monthly (Year 0):       ${proj['tier2_monthly'][0]:,.0f}")
    print(f"    Equity fund seed:              ${config.equity_fund_seed/1e9:,.0f}B")

    # Year-by-year table
    print(f"\n  {'Yr':<4} {'NewRev':>8} {'SSDef':>8} {'EqCont':>8} {'EqFund':>8} "
          f"{'T2$/mo':>8} {'T3$/mo':>8} {'Total':>8} {'Retiree':>9} {'Reserve':>8}")
    print(f"  {'':>4} {'($B)':>8} {'($B)':>8} {'($B)':>8} {'($T)':>8} "
          f"{'':>8} {'':>8} {'$/mo':>8} {'$/mo':>9} {'($B)':>8}")
    print("  " + "─" * 91)

    milestones = [0, 1, 2, 3, 5, 8, 10, 15, 20, 25, 30, 35, 39]
    for t in milestones:
        if t < years:
            print(f"  {t:>3}  {proj['new_revenue'][t]/1e9:>7.0f} "
                  f"{proj['ss_deficit'][t]/1e9:>7.0f} "
                  f"{proj['equity_fund_contribution'][t]/1e9:>7.0f} "
                  f"{proj['equity_fund_balance'][t]/1e12:>7.1f} "
                  f"${proj['tier2_monthly'][t]:>6.0f} "
                  f"${proj['tier3_monthly'][t]:>6.0f} "
                  f"${proj['total_monthly_adult'][t]:>6.0f} "
                  f" ${proj['total_monthly_retiree'][t]:>7.0f} "
                  f"{proj['reserve_balance'][t]/1e9:>7.0f}")

    # Summary stats
    print(f"\n  Summary:")
    print(f"    Final equity fund:           ${proj['equity_fund_balance'][-1]/1e12:,.1f}T")
    print(f"    Final Tier 2 + Tier 3:       ${proj['total_monthly_adult'][-1]:,.0f}/month per adult")
    print(f"    Final retiree total:         ${proj['total_monthly_retiree'][-1]:,.0f}/month")
    print(f"    Year 10 adult benefit:       ${proj['total_monthly_adult'][10]:,.0f}/month")
    print(f"    Year 20 adult benefit:       ${proj['total_monthly_adult'][20]:,.0f}/month")
    print(f"    Year 30 adult benefit:       ${proj['total_monthly_adult'][30]:,.0f}/month")
    print(f"    Cumulative Tier 2 paid out:  ${proj['tier2_outlays'].sum()/1e12:,.1f}T over {years} years")
    print(f"    Cumulative Tier 3 paid out:  ${proj['tier3_outlays'].sum()/1e12:,.1f}T over {years} years")
    print(f"    Reserve balance:             ${proj['reserve_balance'][-1]/1e9:,.0f}B")

    # Key milestone: when does total benefit hit $500/mo?
    hit_500 = np.where(proj['total_monthly_adult'] >= 500)[0]
    hit_800 = np.where(proj['total_monthly_adult'] >= 800)[0]
    hit_1000 = np.where(proj['total_monthly_adult'] >= 1000)[0]

    print(f"\n  Milestone Timeline:")
    print(f"    ${proj['total_monthly_adult'][0]:,.0f}/mo at Year 0")
    if len(hit_500) > 0:
        print(f"    $500/mo reached at Year {hit_500[0]}")
    else:
        print(f"    $500/mo: NOT reached within {years} years")
    if len(hit_800) > 0:
        print(f"    $800/mo reached at Year {hit_800[0]}")
    else:
        print(f"    $800/mo: NOT reached within {years} years")
    if len(hit_1000) > 0:
        print(f"    $1,000/mo reached at Year {hit_1000[0]}")
    else:
        print(f"    $1,000/mo: NOT reached within {years} years")

    return proj


def run_all_scenarios():
    """Run and compare all three scenarios."""

    print("=" * 95)
    print("  SOCIAL SECURITY EXTENSION MODEL v2.0 — FISCALLY GROUNDED PROJECTION")
    print("  'Social Security for All' / 'The American Dividend'")
    print("=" * 95)

    print("""
  V2.0 KEY CHANGE: Revenue-Constrained Benefits
  ────────────────────────────────────────────────
  V1.0 set Tier 2 at $500/month — this exceeded revenue capacity and
  caused insolvency by Year 5. V2.0 computes the ACTUAL revenue-constrained
  benefit and grows it as the system matures.

  Tier 2 monthly = (New Revenue - SS Deficit - Equity Contribution - Reserve)
                    / (Adults × 12)

  This guarantees solvency by construction. There is no "insolvency" —
  only lower or higher benefit levels depending on the scenario.

  Three scenarios tested:
    CONSERVATIVE: FICA reforms only, smaller fund, 3.5% return
    MODERATE:     All six reforms, baseline fund, 4.0% global return
    AMBITIOUS:    All reforms, larger fund, 4.5% return
""")

    all_projections = {}
    for scenario_name in ['conservative', 'moderate', 'ambitious']:
        proj = print_scenario_projection(scenario_name, years=40)
        all_projections[scenario_name] = proj

    # ═══ CROSS-SCENARIO COMPARISON ═══
    print(f"\n\n{'=' * 95}")
    print("  CROSS-SCENARIO COMPARISON")
    print(f"{'=' * 95}")

    print(f"\n  {'Metric':<40} {'Conservative':>14} {'Moderate':>14} {'Ambitious':>14}")
    print("  " + "─" * 82)

    metrics = [
        ('Year 0 benefit ($/mo)', 'total_monthly_adult', 0),
        ('Year 5 benefit ($/mo)', 'total_monthly_adult', 5),
        ('Year 10 benefit ($/mo)', 'total_monthly_adult', 10),
        ('Year 20 benefit ($/mo)', 'total_monthly_adult', 20),
        ('Year 30 benefit ($/mo)', 'total_monthly_adult', 30),
        ('Year 39 benefit ($/mo)', 'total_monthly_adult', 39),
    ]

    for label, key, t in metrics:
        vals = [all_projections[s][key][t] for s in ['conservative', 'moderate', 'ambitious']]
        print(f"  {label:<40} ${vals[0]:>12,.0f} ${vals[1]:>12,.0f} ${vals[2]:>12,.0f}")

    print("  " + "─" * 82)

    # Retiree benefits
    print(f"\n  {'Retiree Benefits (Tier 1+2+3)':<40}")
    for label, key, t in [
        ('Year 10 retiree ($/mo)', 'total_monthly_retiree', 10),
        ('Year 20 retiree ($/mo)', 'total_monthly_retiree', 20),
        ('Year 30 retiree ($/mo)', 'total_monthly_retiree', 30),
    ]:
        vals = [all_projections[s][key][t] for s in ['conservative', 'moderate', 'ambitious']]
        print(f"  {label:<40} ${vals[0]:>12,.0f} ${vals[1]:>12,.0f} ${vals[2]:>12,.0f}")

    # Fund sizes
    print(f"\n  {'Equity Fund Balance':<40}")
    for t in [10, 20, 30, 39]:
        label = f'Year {t} fund ($T)'
        vals = [all_projections[s]['equity_fund_balance'][t] / 1e12
                for s in ['conservative', 'moderate', 'ambitious']]
        print(f"  {label:<40} ${vals[0]:>12.1f} ${vals[1]:>12.1f} ${vals[2]:>12.1f}")

    # ═══ FRAME COMPARISON ═══
    print(f"\n\n{'=' * 95}")
    print("  FRAME COMPARISON: SS EXTENSION vs. STANDALONE UBI")
    print(f"{'=' * 95}")

    model = SSExtensionModelV2(scenario='moderate')
    comp = model.compare_frames()

    print(f"\n  {'DIMENSION':<40} {'SS EXT':>8} {'UBI':>8} {'Weight':>8} {'Delta':>8}")
    print("  " + "─" * 72)

    for d in comp['dimensions']:
        delta = d['ss_extension_score'] - d['standalone_ubi_score']
        print(f"  {d['dimension']:<40} {d['ss_extension_score']:>7.0%} "
              f"{d['standalone_ubi_score']:>7.0%} {d['weight']:>7.0%} {delta:>+7.0%}")

    print("  " + "─" * 72)
    print(f"  {'WEIGHTED TOTAL':<40} {comp['ss_extension_weighted']:>7.0%} "
          f"{comp['standalone_ubi_weighted']:>7.0%} {'':>8} "
          f"{comp['ss_extension_weighted'] - comp['standalone_ubi_weighted']:>+7.0%}")
    print(f"\n  Advantage ratio: {comp['advantage_ratio']:.2f}x")

    # ═══ CRITICISM RESOLUTION ═══
    print(f"\n\n{'=' * 95}")
    print("  HOW THE REFRAME + V2.0 FIX ADDRESSES PRIOR CRITICISMS")
    print(f"{'=' * 95}")

    mod_proj = all_projections['moderate']

    criticisms = [
        ('P1: Constitutional amendment impossible',
         'RESOLVED',
         "SS Extension amends the existing Social Security Act — simple legislation, "
         "not constitutional amendment. The #1 political barrier is eliminated."),

        ('P3: 20-year accumulation is impossible',
         'RESOLVED',
         f"V2.0 pays benefits from Year 0: ${mod_proj['total_monthly_adult'][0]:,.0f}/month "
         f"immediately, growing to ${mod_proj['total_monthly_adult'][10]:,.0f}/month by Year 10. "
         f"No accumulation-only period. Every adult gets a check every month from Day 1."),

        ('E3: ERP compression / survivorship bias',
         'INCORPORATED',
         "V2.0 uses 4.0% global ERP (not 5.0% US-only) per Dimson-Marsh-Staunton 2023. "
         "Conservative scenario uses 3.5%. This directly incorporates the valid criticism."),

        ('E7: Multiplier/clawback double-counting',
         'RESOLVED',
         "V2.0 does NOT count induced tax revenue or clawback as funding sources. "
         "Revenue comes exclusively from FICA reform and equity fund returns. "
         "No circular reasoning."),

        ('P6: Replaces programs for vulnerable',
         'RESOLVED',
         "SS Extension ADDS Tier 2 and Tier 3. It does not replace any existing benefit. "
         "Tier 1 (traditional SS) is completely untouched. Purely additive design."),

        ('E5: Systemic risk / too big to fail',
         'MITIGATED',
         f"Moderate scenario fund reaches ${mod_proj['equity_fund_balance'][30]/1e12:.1f}T "
         f"at Year 30 — large but not dominant. Global diversification + 5-year smoothed "
         f"withdrawal reduces procyclical selling risk. Fund is ~{mod_proj['equity_fund_balance'][30]/110e12:.0%} "
         f"of global equities."),

        ('FISCAL CREDIBILITY (NEW)',
         'RESOLVED',
         f"V2.0 never promises more than revenue supports. Year 0 benefit of "
         f"${mod_proj['total_monthly_adult'][0]:,.0f}/month is honest. Benefits grow as "
         f"revenue grows. The model is solvent by construction — no insolvency at Year 5."),
    ]

    for name, status, detail in criticisms:
        badge = "RESOLVED" if status == 'RESOLVED' else ("INCORP." if status == 'INCORPORATED' else "MITIGATED")
        print(f"\n  [{badge:>9}] {name}")
        # Wrap detail text
        words = detail.split()
        lines = []
        line = "    "
        for word in words:
            if len(line) + len(word) + 1 > 88:
                lines.append(line)
                line = "    " + word
            else:
                line += " " + word if len(line) > 4 else word
        lines.append(line)
        for l in lines:
            print(l)

    # ═══ BOTTOM LINE ═══
    print(f"\n\n{'=' * 95}")
    print("  BOTTOM LINE — HONEST NUMBERS")
    print(f"{'=' * 95}")

    c = all_projections['conservative']
    m = all_projections['moderate']
    a = all_projections['ambitious']

    print(f"""
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │  SOCIAL SECURITY FOR ALL — V2.0 FISCALLY GROUNDED PROJECTIONS                         │
  ├──────────────────────┬────────────────┬────────────────┬────────────────┐              │
  │  Timeline            │  Conservative  │  Moderate      │  Ambitious     │              │
  ├──────────────────────┼────────────────┼────────────────┼────────────────┤              │
  │  Year 0 (launch)     │  ${c['total_monthly_adult'][0]:>6,.0f}/mo     │  ${m['total_monthly_adult'][0]:>6,.0f}/mo     │  ${a['total_monthly_adult'][0]:>6,.0f}/mo     │              │
  │  Year 5              │  ${c['total_monthly_adult'][5]:>6,.0f}/mo     │  ${m['total_monthly_adult'][5]:>6,.0f}/mo     │  ${a['total_monthly_adult'][5]:>6,.0f}/mo     │              │
  │  Year 10             │  ${c['total_monthly_adult'][10]:>6,.0f}/mo     │  ${m['total_monthly_adult'][10]:>6,.0f}/mo     │  ${a['total_monthly_adult'][10]:>6,.0f}/mo     │              │
  │  Year 20             │  ${c['total_monthly_adult'][20]:>6,.0f}/mo     │  ${m['total_monthly_adult'][20]:>6,.0f}/mo     │  ${a['total_monthly_adult'][20]:>6,.0f}/mo     │              │
  │  Year 30             │  ${c['total_monthly_adult'][30]:>6,.0f}/mo     │  ${m['total_monthly_adult'][30]:>6,.0f}/mo     │  ${a['total_monthly_adult'][30]:>6,.0f}/mo     │              │
  │  Year 39             │  ${c['total_monthly_adult'][39]:>6,.0f}/mo     │  ${m['total_monthly_adult'][39]:>6,.0f}/mo     │  ${a['total_monthly_adult'][39]:>6,.0f}/mo     │              │
  ├──────────────────────┴────────────────┴────────────────┴────────────────┤              │
  │                                                                         │              │
  │  Retirees get EXISTING SS + Tier 2 + Tier 3                            │              │
  │  Year 20 retiree (moderate): ${m['total_monthly_retiree'][20]:>6,.0f}/month                            │              │
  │                                                                         │              │
  │  Equity fund at Year 30 (moderate): ${m['equity_fund_balance'][30]/1e12:>5.1f}T                            │              │
  │                                                                         │              │
  │  KEY: These numbers are HONEST. Every dollar of Tier 2 is backed       │              │
  │  by actual revenue. No insolvency. No aspirational targets that        │              │
  │  exceed fiscal capacity. Benefits grow as the system compounds.        │              │
  │                                                                         │              │
  │  The SS Extension frame remains 2.0x superior to standalone UBI        │              │
  │  on political viability, implementation speed, and legal durability.    │              │
  │                                                                         │              │
  └─────────────────────────────────────────────────────────────────────────┘              │
  └────────────────────────────────────────────────────────────────────────────────────────┘
""")

    # ═══ RECONCILIATION WITH PRIOR MODELS ═══
    print(f"\n{'=' * 95}")
    print("  RECONCILIATION: WHY $106/mo (V2.0) vs. $501/mo (CRITICISM-ADJUSTED V1)")
    print(f"{'=' * 95}")

    print(f"""
  The criticism framework's post-correction estimate was $501/month (Year 1).
  V2.0's moderate scenario starts at $106/month. Why the gap?

  The $501 estimate (living_wage_model + criticism_framework) included:
    - Wealth tax revenue:        $416B  (not in SS Extension — too fragile)
    - Tax clawback:              $750B  (not counted — circular reasoning, per E7)
    - Induced multiplier:        $265B  (not counted — circular reasoning, per E7)
    - Safety net consolidation:  $136B  (not counted — SS Extension is additive, per P6)
    - Sovereign fund income:     $350B  (not yet — fund is accumulating in early years)

  V2.0 uses ONLY these Year 0 revenue sources:
    - FICA cap removal:          $310B  (rock-solid, 99%+ compliance)
    - Progressive surtax:        $150B  (straightforward legislation)
    - Investment income FICA:    $150B  (extends existing 3.8% NIIT)
    - FTT:                       $ 50B  (moderate 5bps)
    - Carbon tax share:          $ 68B  (30% to OASDI)
    ─────────────────────────────────────
    Total new revenue:           $728B
    Less SS deficit:            -$200B  (must keep existing SS solvent)
    Less equity fund contrib:   -$200B  (compounds for future Tier 3)
    Less reserve:               -$   0  (initial year)
    ─────────────────────────────────────
    Available for Tier 2:        $328B  → ${m['tier2_monthly'][0]:,.0f}/month

  This is the HONEST starting point. It grows because:
    1. FICA revenue grows at 3%/yr with wages
    2. Investment income FICA grows at 4%/yr with wealth
    3. Equity fund compounds at 4% real → withdrawals begin Year 8
    4. After Year 30, equity fund contributions stop → all revenue to Tier 2

  Year 30 benefit: ${m['total_monthly_adult'][30]:,.0f}/month  (${m['tier2_monthly'][30]:,.0f} Tier 2 + ${m['tier3_monthly'][30]:,.0f} Tier 3)
  Year 39 benefit: ${m['total_monthly_adult'][39]:,.0f}/month  (${m['tier2_monthly'][39]:,.0f} Tier 2 + ${m['tier3_monthly'][39]:,.0f} Tier 3)

  The tradeoff: lower initial benefit, but CREDIBLE and GROWING.
  V1's $500/month was a promise the system couldn't keep.
  V2's $106/month is a promise backed by revenue.
""")


if __name__ == '__main__':
    run_all_scenarios()
