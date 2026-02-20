"""
US Individual Income Distribution — Working-Age Adults (18-66)

This module provides the income distribution data needed to model
means-tested benefit eligibility. The core question: how many
working-age adults earn below a given monthly income threshold?

DATA SOURCE: Census Bureau Current Population Survey (CPS)
Annual Social and Economic Supplement (ASEC), 2023.
Cross-referenced with BLS Current Employment Statistics (CES).

IMPORTANT NOTES:
  1. This is INDIVIDUAL personal income, not household income.
     A person reporting $0 income may be a stay-at-home spouse
     in a wealthy household. The model acknowledges this limitation.

  2. "Income" = total personal income: wages, salaries, self-employment,
     investment income, Social Security, disability, transfers.
     For means-testing purposes, we want MARKET income (excluding
     government transfers) to avoid circular logic. However, the
     CPS ASEC data includes transfers. We adjust by noting that
     ~12% of working-age adults have near-zero market income.

  3. The distribution shifts over time because:
     - Nominal wages grow ~3%/year
     - CPI grows ~2%/year
     - Real wage growth (~1%/year) slowly pushes people above
       any fixed real threshold
     - Net effect: the fraction below a real threshold shrinks
       by ~0.3-0.5%/year

  4. Working-age = 18 to 66 (pre-SS eligibility). This is the
     population that the means test applies to. SS beneficiaries
     (67M) are always eligible regardless of income.

References:
- Census Bureau CPS ASEC (2023): Table PINC-01 — Individual Income
- BLS (2024): Occupational Employment & Wage Statistics (OEWS)
- Semega et al. (2023) "Income in the United States: 2022" Census P60-279
- SSA (2024): Wage Statistics — National Average Wage Index
- BLS CES (2024): Employment Situation Summary
"""

import numpy as np
from typing import Tuple


# ═══════════════════════════════════════════════════════════════════════
#  POPULATION CONSTANTS
# ═══════════════════════════════════════════════════════════════════════

US_ADULTS_18_PLUS = 258_000_000      # Total adults 18+
SS_BENEFICIARIES = 67_000_000        # Current OASDI beneficiaries
WORKING_AGE_ADULTS = US_ADULTS_18_PLUS - SS_BENEFICIARIES  # ~191M

# Working-age adult growth rate (net of aging into SS eligibility)
WORKING_AGE_GROWTH_RATE = 0.002      # 0.2%/year (slower than total adult pop)
SS_BENEFICIARY_GROWTH_RATE = 0.015   # 1.5%/year (aging baby boomers, first 20yr)


# ═══════════════════════════════════════════════════════════════════════
#  INCOME DISTRIBUTION — CUMULATIVE DISTRIBUTION FUNCTION (CDF)
# ═══════════════════════════════════════════════════════════════════════

"""
Cumulative distribution: fraction of WORKING-AGE adults (18-66) with
individual monthly income BELOW the given threshold.

Constructed from Census CPS ASEC Table PINC-01 (2023), BLS OEWS,
and SSA Wage Statistics. Dollar amounts are MONTHLY.

Key calibration points:
  - Median individual income (full-time, year-round): ~$57,200/yr = $4,767/mo
  - Median for ALL individuals (incl. part-time, non-working): ~$40,500/yr = $3,375/mo
  - ~12% of working-age adults have zero or near-zero reported income
    (students, stay-at-home parents, discouraged workers, unreported)
  - Federal minimum wage ($7.25/hr, 2080hrs): $15,080/yr = $1,257/mo
  - ~30% of workers earn below $15/hr (~$31,200/yr = $2,600/mo)
  - MIT living wage single adult no children: $21.33/hr = $2,200/mo (national avg)
"""

# (monthly_income_threshold, cumulative_fraction_below)
# These are calibrated to CPS ASEC 2023 data for ages 18-66
INCOME_CDF_POINTS = [
    (0,       0.000),   # By definition
    (250,     0.060),   # Near-zero income: students, dependents, unreported
    (500,     0.100),   # Minimal income: very part-time, gig
    (750,     0.135),   # Part-time at or near minimum wage
    (1000,    0.170),   # Part-time ~25hrs/week at $10/hr
    (1250,    0.200),   # Full-time at federal minimum wage ($7.25/hr)
    (1500,    0.245),   # $18K/yr — near poverty line; LIVING_WAGE_LOW
    (1750,    0.285),   # ~$21K/yr
    (2000,    0.330),   # $24K/yr — below median part-time
    (2200,    0.370),   # $26.4K/yr — MIT living wage (national avg); LIVING_WAGE_MID
    (2500,    0.405),   # $30K/yr
    (3000,    0.460),   # $36K/yr — LIVING_WAGE_HIGH
    (3500,    0.510),   # $42K/yr — approaching median all-workers
    (4000,    0.555),   # $48K/yr
    (4500,    0.600),   # $54K/yr
    (5000,    0.640),   # $60K/yr — near median full-time
    (6000,    0.720),   # $72K/yr
    (7500,    0.800),   # $90K/yr
    (10000,   0.880),   # $120K/yr
    (15000,   0.940),   # $180K/yr — top ~6%
    (25000,   0.975),   # $300K/yr — top ~2.5%
    (50000,   0.993),   # $600K/yr — top ~0.7%
    (100000,  0.999),   # $1.2M/yr — top ~0.1%
]

# Convert to numpy arrays for interpolation
_CDF_INCOMES = np.array([p[0] for p in INCOME_CDF_POINTS], dtype=float)
_CDF_FRACTIONS = np.array([p[1] for p in INCOME_CDF_POINTS], dtype=float)


def interpolate_cdf(monthly_income: float) -> float:
    """
    Interpolate the income CDF to find the fraction of working-age
    adults earning below a given monthly income threshold.

    Uses linear interpolation between calibration points.

    Args:
        monthly_income: Monthly individual income threshold ($)

    Returns:
        Fraction of working-age adults (18-66) earning below threshold (0-1)
    """
    if monthly_income <= 0:
        return 0.0
    if monthly_income >= _CDF_INCOMES[-1]:
        return _CDF_FRACTIONS[-1]

    return float(np.interp(monthly_income, _CDF_INCOMES, _CDF_FRACTIONS))


def fraction_below_threshold(threshold_monthly: float, year: int = 0,
                              nominal_wage_growth: float = 0.03,
                              cpi_growth: float = 0.02) -> float:
    """
    Compute the fraction of working-age adults earning below a given
    monthly income threshold at a future year.

    The threshold is assumed to grow with CPI (real constant).
    Wages grow faster than CPI (real wage growth ~1%/year).
    This means the fraction below threshold SHRINKS over time
    as real incomes rise.

    The shrinkage rate is calibrated to ~0.3-0.5%/year based on
    historical real wage growth and income distribution dynamics.
    We use 0.4%/year as the central estimate.

    We impose a floor of 5% — even in a very prosperous economy,
    at least 5% of working-age adults will have near-zero market
    income (students, caregivers, disabled-but-not-on-SS, etc.).

    Args:
        threshold_monthly: Living wage threshold (real, Year 0 dollars)
        year: Years into the future (0 = today)
        nominal_wage_growth: Nominal wage growth rate (default 3%)
        cpi_growth: CPI inflation rate (default 2%)

    Returns:
        Fraction of working-age adults below threshold (0-1)
    """
    # Base fraction from the CDF (Year 0)
    base_fraction = interpolate_cdf(threshold_monthly)

    # Real wage growth shrinks the below-threshold population
    real_wage_growth = nominal_wage_growth - cpi_growth  # ~1%/year
    # Shrinkage rate: ~40% of real wage growth translates to CDF shift
    # (not 100% because income distribution has a thick lower tail)
    shrinkage_rate = real_wage_growth * 0.40  # ~0.4%/year

    adjusted = base_fraction * ((1 - shrinkage_rate) ** year)

    # Floor: at least 5% always below any living-wage threshold
    return max(adjusted, 0.05)


def compute_eligible_population(
    year: int,
    threshold_monthly: float = 2200,
    total_adults_base: float = 258e6,
    adult_growth_rate: float = 0.003,
    ss_base: float = 67e6,
    ss_growth_rate: float = 0.015,
    ss_growth_slowdown_year: int = 20,
    ss_growth_rate_after: float = 0.005,
) -> dict:
    """
    Compute population segments for a given year.

    Returns a dict with:
      - total_adults: All adults 18+
      - ss_beneficiaries: Current SS recipients (always eligible)
      - working_age: Adults not on SS
      - working_age_below_lw: Working-age adults earning below living wage
      - working_age_above_lw: Working-age adults earning above living wage
      - total_eligible: SS beneficiaries + working-age below living wage
      - total_excluded: Working-age above living wage
      - eligible_pct: Fraction of all adults who are eligible

    Args:
        year: Years from now (0 = today)
        threshold_monthly: Living wage threshold (real $)
        total_adults_base: Base adult population
        adult_growth_rate: Annual adult population growth
        ss_base: Base SS beneficiary count
        ss_growth_rate: SS beneficiary growth (aging boomers)
        ss_growth_slowdown_year: Year after which SS growth slows
        ss_growth_rate_after: Slower SS growth rate
    """
    # Total adults
    total_adults = total_adults_base * ((1 + adult_growth_rate) ** year)

    # SS beneficiaries (same growth model as ss_extension_model.py)
    if year <= ss_growth_slowdown_year:
        ss = ss_base * ((1 + ss_growth_rate) ** year)
    else:
        ss = ss_base * ((1 + ss_growth_rate) ** ss_growth_slowdown_year) * \
             ((1 + ss_growth_rate_after) ** (year - ss_growth_slowdown_year))

    # Working-age adults
    working_age = max(total_adults - ss, 0)

    # Fraction below living wage (shrinks over time with real wage growth)
    frac_below = fraction_below_threshold(threshold_monthly, year)

    # Working-age segments
    working_age_below = working_age * frac_below
    working_age_above = working_age * (1 - frac_below)

    # Eligible population
    total_eligible = ss + working_age_below
    total_excluded = working_age_above

    return {
        'total_adults': total_adults,
        'ss_beneficiaries': ss,
        'working_age': working_age,
        'working_age_below_lw': working_age_below,
        'working_age_above_lw': working_age_above,
        'total_eligible': total_eligible,
        'total_excluded': total_excluded,
        'eligible_pct': total_eligible / total_adults if total_adults > 0 else 0,
        'frac_below_lw': frac_below,
    }


# ═══════════════════════════════════════════════════════════════════════
#  CONVENIENCE: POPULATION TRAJECTORY
# ═══════════════════════════════════════════════════════════════════════

def population_trajectory(years: int = 40,
                           threshold_monthly: float = 2200) -> dict:
    """
    Compute full population trajectory over time.

    Returns dict of numpy arrays for each population segment.
    """
    result = {key: np.zeros(years) for key in [
        'total_adults', 'ss_beneficiaries', 'working_age',
        'working_age_below_lw', 'working_age_above_lw',
        'total_eligible', 'total_excluded', 'eligible_pct', 'frac_below_lw',
    ]}

    for t in range(years):
        seg = compute_eligible_population(year=t, threshold_monthly=threshold_monthly)
        for key in result:
            result[key][t] = seg[key]

    return result


# ═══════════════════════════════════════════════════════════════════════
#  SELF-TEST
# ═══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 80)
    print("  US INCOME DISTRIBUTION — WORKING-AGE ADULTS (18-66)")
    print("  Source: Census CPS ASEC 2023, BLS OEWS, SSA Wage Statistics")
    print("=" * 80)

    # CDF at key thresholds
    print(f"\n  Income CDF (fraction of working-age adults earning below threshold):")
    print(f"  {'Threshold':>12} {'Monthly':>10} {'Annual':>12} {'Below':>8}")
    print("  " + "─" * 42)

    test_points = [
        ('Poverty line', 1255),
        ('LW LOW', 1500),
        ('LW MID', 2200),
        ('LW HIGH', 3000),
        ('Median (all)', 3375),
        ('Median (FT)', 4767),
        ('$90K/yr', 7500),
        ('$120K/yr', 10000),
    ]

    for label, monthly in test_points:
        frac = interpolate_cdf(monthly)
        annual = monthly * 12
        print(f"  {label:>12} ${monthly:>8,}/mo ${annual:>10,}/yr {frac:>7.1%}")

    # Population segments at Year 0
    print(f"\n\n  Population Segments at Year 0 (threshold = $2,200/month):")
    print("  " + "─" * 55)
    seg = compute_eligible_population(year=0, threshold_monthly=2200)
    for key, val in seg.items():
        if key == 'eligible_pct' or key == 'frac_below_lw':
            print(f"  {key:<30} {val:>10.1%}")
        else:
            print(f"  {key:<30} {val/1e6:>10.1f}M")

    # Time evolution
    print(f"\n\n  Population Segments Over Time ($2,200/month threshold):")
    print(f"  {'Year':<6} {'Eligible':>10} {'Excluded':>10} {'Elig%':>8} {'Below LW%':>10}")
    print("  " + "─" * 44)

    for t in [0, 5, 10, 15, 20, 25, 30, 35, 40]:
        if t < 40:
            seg = compute_eligible_population(year=t, threshold_monthly=2200)
            print(f"  {t:<6} {seg['total_eligible']/1e6:>9.1f}M "
                  f"{seg['total_excluded']/1e6:>9.1f}M "
                  f"{seg['eligible_pct']:>7.1%} "
                  f"{seg['frac_below_lw']:>9.1%}")
        else:
            seg = compute_eligible_population(year=39, threshold_monthly=2200)
            print(f"  {39:<6} {seg['total_eligible']/1e6:>9.1f}M "
                  f"{seg['total_excluded']/1e6:>9.1f}M "
                  f"{seg['eligible_pct']:>7.1%} "
                  f"{seg['frac_below_lw']:>9.1%}")

    # Threshold sensitivity
    print(f"\n\n  Threshold Sensitivity at Year 0:")
    print(f"  {'Threshold':>12} {'Below%':>8} {'Eligible':>10} {'Excluded':>10} {'Multiplier':>12}")
    print("  " + "─" * 52)

    for threshold in [1500, 2000, 2200, 2500, 3000, 4000, 5000]:
        seg = compute_eligible_population(year=0, threshold_monthly=threshold)
        multiplier = 258e6 / seg['total_eligible'] if seg['total_eligible'] > 0 else float('inf')
        print(f"  ${threshold:>10,}/mo {seg['frac_below_lw']:>7.1%} "
              f"{seg['total_eligible']/1e6:>9.1f}M "
              f"{seg['total_excluded']/1e6:>9.1f}M "
              f"{multiplier:>10.2f}x")
