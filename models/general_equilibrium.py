"""
General Equilibrium Model for Sovereign Fund Market Impact

Analyzes how a large sovereign wealth fund affects:
1. Asset prices (PE expansion, ERP compression)
2. Market liquidity and microstructure
3. Corporate governance and behavior
4. Labor markets and consumption
5. Fiscal sustainability

This is the critical "so what happens when you actually do this?" model.

The key insight: partial-equilibrium estimates of fund returns are overly
optimistic because the fund's own buying pressure raises prices and
compresses future returns. We model this feedback loop explicitly.

References:
- Gabaix & Koijen (2022) "In Search of the Origins of Financial Fluctuations"
- Greenwood & Vayanos (2010) "Price Pressure in the Government Bond Market"
- Kyle (1985) "Continuous Auctions and Insider Trading"
- Koijen & Yogo (2019) "A Demand System Approach to Asset Pricing"
"""

import numpy as np
from dataclasses import dataclass
from scipy.optimize import fsolve
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.parameters import *


@dataclass
class GEModelState:
    """State of the general equilibrium model at a point in time."""
    fund_size: float              # Sovereign fund AUM
    equity_market_cap: float      # Total market cap
    fund_share_of_market: float   # Fund as % of market
    equity_risk_premium: float    # Current ERP
    pe_ratio: float               # Market PE ratio
    dividend_yield: float         # Current dividend yield
    expected_return: float        # Expected real return
    ubi_withdrawal: float         # Annual UBI payout
    gdp: float                    # Nominal GDP
    consumption_effect: float     # Change in aggregate consumption
    labor_supply_effect: float    # Change in labor supply


class InelasticMarketsModel:
    """
    Implements the Gabaix-Koijen (2022) inelastic markets framework.

    Key finding: $1 of inflow to the stock market raises aggregate
    market cap by approximately $5 (multiplier of ~5). This means
    a sovereign fund buying equities has an outsized price impact.

    The multiplier arises because most equity is held by relatively
    price-insensitive investors (index funds, pensions, endowments).
    """

    def __init__(self, multiplier: float = 5.0, baseline_erp: float = 0.05,
                 baseline_pe: float = 22.0, baseline_market_cap: float = US_EQUITY_MARKET_CAP):
        self.multiplier = multiplier
        self.baseline_erp = baseline_erp
        self.baseline_pe = baseline_pe
        self.baseline_market_cap = baseline_market_cap
        self.baseline_earnings = baseline_market_cap / baseline_pe

    def price_impact(self, fund_inflow: float) -> dict:
        """
        Compute the price impact of sovereign fund buying.

        Args:
            fund_inflow: Annual net buying by sovereign fund

        Returns:
            Dict with new market cap, PE ratio, and ERP
        """
        # Gabaix-Koijen: delta_market_cap = multiplier * delta_flow
        market_cap_increase = self.multiplier * fund_inflow
        new_market_cap = self.baseline_market_cap + market_cap_increase

        # PE expansion (earnings assumed sticky in short run)
        new_pe = new_market_cap / self.baseline_earnings
        pe_change_pct = (new_pe - self.baseline_pe) / self.baseline_pe

        # ERP compression: higher prices -> lower expected returns
        new_dividend_yield = (self.baseline_earnings * DIVIDEND_YIELD * self.baseline_pe) / new_market_cap
        # Expected return = dividend yield + earnings growth + multiple expansion
        # With compressed multiples, future returns are lower
        earnings_growth = GDP_GROWTH_REAL  # Assume earnings grow with GDP
        expected_return = new_dividend_yield + earnings_growth
        new_erp = expected_return - RISK_FREE_RATE_REAL

        return {
            'new_market_cap': new_market_cap,
            'new_pe': new_pe,
            'pe_change_pct': pe_change_pct,
            'new_dividend_yield': new_dividend_yield,
            'new_erp': new_erp,
            'erp_compression': self.baseline_erp - new_erp,
            'expected_return': expected_return,
        }

    def cumulative_impact(self, annual_inflows: np.ndarray) -> list[dict]:
        """
        Model cumulative price impact of multi-year fund accumulation.

        Important: the multiplier applies to FLOW, not stock.
        Once the fund stops buying, much of the price impact persists
        (because the fund is a permanent holder), but the marginal
        impact of each new dollar diminishes as the market adjusts.
        """
        results = []
        cumulative_inflow = 0
        current_market_cap = self.baseline_market_cap

        for t, inflow in enumerate(annual_inflows):
            cumulative_inflow += inflow

            # Diminishing multiplier as market adapts
            adaptive_multiplier = self.multiplier * (0.8 ** (t / 10))

            impact = self.multiplier * inflow
            current_market_cap = self.baseline_market_cap + adaptive_multiplier * cumulative_inflow

            new_pe = current_market_cap / (self.baseline_earnings * (1 + GDP_GROWTH_REAL) ** t)
            new_dy = (self.baseline_earnings * (1 + GDP_GROWTH_REAL) ** t * 0.018 * self.baseline_pe) / current_market_cap
            new_erp = new_dy + GDP_GROWTH_REAL - RISK_FREE_RATE_REAL

            results.append({
                'year': t,
                'cumulative_inflow': cumulative_inflow,
                'market_cap': current_market_cap,
                'pe_ratio': new_pe,
                'erp': new_erp,
                'fund_share': cumulative_inflow / current_market_cap,
            })

        return results


class FTTEquilibriumModel:
    """
    Models the equilibrium effects of a Financial Transaction Tax.

    Key dynamics:
    - Higher tax -> lower volume -> lower revenue (Laffer curve)
    - Spread widening partially offsets tax (incidence on market makers)
    - Migration to untaxed venues
    - Reduction in price discovery efficiency
    """

    def __init__(self, baseline_volume: float = ANNUAL_EQUITY_VOLUME,
                 volume_elasticity: float = VOLUME_ELASTICITY_MID):
        self.baseline_volume = baseline_volume
        self.elasticity = volume_elasticity

    def equilibrium_revenue(self, tax_rate: float) -> dict:
        """
        Compute equilibrium FTT revenue accounting for behavioral response.

        The tax is levied on both sides of each transaction.
        Volume responds elastically to the effective trading cost increase.
        """
        # Effective cost increase as % of baseline spread
        baseline_cost = EFFECTIVE_SPREAD_BPS / 10000
        new_cost = baseline_cost + tax_rate
        cost_increase_pct = (new_cost - baseline_cost) / baseline_cost

        # Volume response
        volume_change = self.elasticity * cost_increase_pct
        new_volume = self.baseline_volume * (1 + volume_change)
        new_volume = max(new_volume, self.baseline_volume * 0.1)  # Floor at 10%

        # Revenue = tax_rate * volume * 2 (buyer + seller)
        gross_revenue = tax_rate * new_volume * 2

        # Deadweight loss (Harberger triangle approximation)
        volume_lost = self.baseline_volume - new_volume
        deadweight_loss = 0.5 * tax_rate * volume_lost

        # Spread widening: market makers pass through ~50% of tax
        spread_widening_bps = tax_rate * 10000 * 0.5

        return {
            'tax_rate': tax_rate,
            'tax_rate_bps': tax_rate * 10000,
            'new_volume': new_volume,
            'volume_change_pct': volume_change,
            'gross_revenue': gross_revenue,
            'deadweight_loss': deadweight_loss,
            'net_social_benefit': gross_revenue - deadweight_loss,
            'spread_widening_bps': spread_widening_bps,
            'revenue_per_capita': gross_revenue / US_POPULATION,
        }

    def find_revenue_maximizing_rate(self) -> dict:
        """Find the Laffer-curve peak: the tax rate that maximizes revenue."""
        rates = np.linspace(0.0001, 0.01, 1000)
        revenues = [self.equilibrium_revenue(r)['gross_revenue'] for r in rates]
        optimal_idx = np.argmax(revenues)
        return self.equilibrium_revenue(rates[optimal_idx])

    def laffer_curve(self, n_points: int = 100) -> dict:
        """Generate the full Laffer curve for FTT."""
        rates = np.linspace(0.0001, 0.005, n_points)
        revenues = np.array([self.equilibrium_revenue(r)['gross_revenue'] for r in rates])
        dwl = np.array([self.equilibrium_revenue(r)['deadweight_loss'] for r in rates])

        return {
            'rates': rates,
            'rates_bps': rates * 10000,
            'revenues': revenues,
            'deadweight_loss': dwl,
            'net_benefit': revenues - dwl,
        }


class LaborMarketModel:
    """
    Models the labor supply response to UBI.

    Key tension: UBI reduces the marginal incentive to work (income effect)
    but also provides a safety net that enables risk-taking and job mobility
    (substitution effect on quality of work, not quantity).

    Literature consensus (from Finland, Stockton, Kenya experiments):
    - Employment reduction: 1-4% at $1000/month UBI
    - Hours reduction: 5-10%
    - Entrepreneurship increase: 5-15%
    - Health/education improvements: significant
    """

    def __init__(self, labor_force: float = 165e6, avg_wage: float = 60_000,
                 labor_share_gdp: float = 0.60):
        self.labor_force = labor_force
        self.avg_wage = avg_wage
        self.labor_share = labor_share_gdp

    def labor_supply_response(self, monthly_ubi: float,
                               account_for_ss: bool = True) -> dict:
        """
        Estimate labor supply response to a given UBI level.

        Uses semi-elasticity estimates from:
        - Marinescu (2018) survey of NIT experiments
        - Cesarini et al (2017) lottery winners
        - Finland basic income experiment (2020)

        When account_for_ss=True, adjusts for the fact that ~67M Americans
        already receive Social Security (~$1,907/mo avg). These recipients
        are mostly retired and have near-zero labor supply elasticity to
        additional income. Only working-age non-SS recipients face the
        full labor supply income effect from UBI.
        """
        annual_ubi = monthly_ubi * 12

        if account_for_ss:
            # SS recipients (~67M) are mostly retired — ~zero labor supply effect
            # Children (~53M) don't receive UBI in adults-only designs
            # Working-age adults: ~210M — these are who respond to UBI
            ss_recipients = 67_000_000
            children = 53_000_000

            # Only labor force members can reduce labor supply
            # Their replacement rate is UBI / their wage
            worker_replacement_rate = annual_ubi / self.avg_wage

            # But scale the macro effect: only fraction of adults are workers
            working_age_adults = US_POPULATION - ss_recipients - children
            labor_force_participation = self.labor_force / working_age_adults
            effective_replacement_rate = worker_replacement_rate * labor_force_participation
        else:
            effective_replacement_rate = annual_ubi / self.avg_wage

        replacement_rate = effective_replacement_rate

        # Extensive margin (participation): elasticity ~ -0.1 to -0.3
        participation_elasticity = -0.15
        participation_change = participation_elasticity * replacement_rate

        # Intensive margin (hours): elasticity ~ -0.1 to -0.2
        hours_elasticity = -0.12
        hours_change = hours_elasticity * replacement_rate

        # Total labor supply change
        total_labor_change = participation_change + hours_change

        # GDP impact (assuming labor share and productivity unchanged)
        gdp_impact = total_labor_change * self.labor_share

        # Offsetting effects
        entrepreneurship_boost = 0.02 * replacement_rate  # More startups
        health_productivity = 0.01 * replacement_rate  # Better health -> productivity
        education_investment = 0.005 * replacement_rate  # More human capital

        net_gdp_impact = gdp_impact + entrepreneurship_boost + health_productivity + education_investment

        return {
            'monthly_ubi': monthly_ubi,
            'replacement_rate': replacement_rate,
            'account_for_ss': account_for_ss,
            'participation_change': participation_change,
            'hours_change': hours_change,
            'total_labor_change': total_labor_change,
            'gross_gdp_impact': gdp_impact,
            'entrepreneurship_boost': entrepreneurship_boost,
            'health_productivity': health_productivity,
            'education_investment': education_investment,
            'net_gdp_impact': net_gdp_impact,
            'workers_leaving': int(abs(participation_change) * self.labor_force),
        }


class FullGEModel:
    """
    Integrates all general equilibrium effects into a unified model.

    Solves for the fixed point where:
    - Fund returns reflect compressed ERP from its own buying
    - FTT revenue reflects behavioral volume response
    - Labor supply reflects UBI-induced income effects
    - GDP reflects labor market and consumption changes
    - Fund contributions reflect fiscal capacity under new GDP
    """

    def __init__(self):
        self.markets = InelasticMarketsModel()
        self.ftt = FTTEquilibriumModel()
        self.labor = LaborMarketModel()

    def solve_equilibrium(self, fund_size: float, annual_contribution: float,
                         ftt_rate: float, withdrawal_rate: float) -> GEModelState:
        """
        Solve for general equilibrium state given policy parameters.

        Uses iterative fixed-point approach:
        1. Start with partial-equilibrium estimates
        2. Feed through all channels
        3. Iterate until convergence
        """
        # Initial state
        erp = EQUITY_RISK_PREMIUM_MEAN
        gdp = GDP_US
        market_cap = US_EQUITY_MARKET_CAP

        for iteration in range(50):
            # 1. Price impact of fund
            price_impact = self.markets.price_impact(annual_contribution)
            new_market_cap = price_impact['new_market_cap']
            new_erp = price_impact['new_erp']

            # 2. Fund returns under compressed ERP
            expected_return = new_erp + RISK_FREE_RATE_REAL
            ubi_withdrawal = fund_size * withdrawal_rate

            # 3. FTT revenue
            ftt_result = self.ftt.equilibrium_revenue(ftt_rate)

            # 4. Labor market response
            monthly_ubi = (ubi_withdrawal / US_POPULATION) / 12
            labor_result = self.labor.labor_supply_response(monthly_ubi)

            # 5. GDP feedback
            new_gdp = gdp * (1 + labor_result['net_gdp_impact'])

            # 6. Market cap adjusts to GDP
            market_cap_gdp_ratio = US_EQUITY_MARKET_CAP / GDP_US
            gdp_adjusted_cap = new_gdp * market_cap_gdp_ratio

            # Blend price-impact cap with GDP-adjusted cap
            new_market_cap = 0.6 * new_market_cap + 0.4 * gdp_adjusted_cap

            # Check convergence
            if abs(new_erp - erp) < 0.0001 and abs(new_gdp - gdp) / gdp < 0.0001:
                break

            erp = new_erp
            gdp = new_gdp
            market_cap = new_market_cap

        return GEModelState(
            fund_size=fund_size,
            equity_market_cap=new_market_cap,
            fund_share_of_market=fund_size / new_market_cap,
            equity_risk_premium=erp,
            pe_ratio=price_impact['new_pe'],
            dividend_yield=price_impact['new_dividend_yield'],
            expected_return=expected_return,
            ubi_withdrawal=ubi_withdrawal,
            gdp=new_gdp,
            consumption_effect=ubi_withdrawal / new_gdp,
            labor_supply_effect=labor_result['total_labor_change'],
        )

    def sensitivity_analysis(self) -> list[dict]:
        """
        Run sensitivity analysis across fund sizes and policy parameters.
        """
        results = []

        fund_sizes = [1e12, 2.5e12, 5e12, 10e12, 15e12, 20e12]
        for fs in fund_sizes:
            annual_contrib = fs * 0.05  # 5% of fund as annual contribution
            state = self.solve_equilibrium(
                fund_size=fs,
                annual_contribution=annual_contrib,
                ftt_rate=0.0005,
                withdrawal_rate=0.035,
            )
            monthly_ubi = (state.ubi_withdrawal / US_POPULATION) / 12

            results.append({
                'fund_size_T': fs / 1e12,
                'market_cap_T': state.equity_market_cap / 1e12,
                'fund_share': state.fund_share_of_market,
                'erp': state.equity_risk_premium,
                'pe_ratio': state.pe_ratio,
                'expected_return': state.expected_return,
                'monthly_ubi': monthly_ubi,
                'gdp_T': state.gdp / 1e12,
                'gdp_change': (state.gdp - GDP_US) / GDP_US,
                'labor_effect': state.labor_supply_effect,
            })

        return results


def run_ge_analysis():
    """Run the full general equilibrium analysis."""
    print("=" * 80)
    print("GENERAL EQUILIBRIUM ANALYSIS")
    print("=" * 80)

    model = FullGEModel()

    # 1. Price impact analysis
    print("\n--- Inelastic Markets: Price Impact of Fund Accumulation ---")
    inflows = np.array([250e9] * 20)  # $250B/year for 20 years
    impacts = model.markets.cumulative_impact(inflows)
    for imp in impacts[::5]:
        print(f"  Year {imp['year']:2d}: Market Cap ${imp['market_cap']/1e12:.1f}T, "
              f"PE {imp['pe_ratio']:.1f}, ERP {imp['erp']:.2%}, "
              f"Fund Share {imp['fund_share']:.1%}")

    # 2. FTT Laffer curve
    print("\n--- Financial Transaction Tax: Laffer Curve ---")
    optimal = model.ftt.find_revenue_maximizing_rate()
    print(f"  Revenue-maximizing rate: {optimal['tax_rate_bps']:.1f} bps")
    print(f"  Max revenue: ${optimal['gross_revenue']/1e9:.1f}B/year")
    print(f"  Volume change: {optimal['volume_change_pct']:.1%}")
    print(f"  Spread widening: +{optimal['spread_widening_bps']:.1f} bps")
    print(f"  Per capita: ${optimal['revenue_per_capita']:.0f}/year")

    # 3. Labor market effects
    print("\n--- Labor Market Response ---")
    for ubi in [100, 250, 500, 750, 1000]:
        result = model.labor.labor_supply_response(ubi)
        print(f"  ${ubi}/mo UBI: Labor supply {result['total_labor_change']:+.1%}, "
              f"Net GDP {result['net_gdp_impact']:+.2%}, "
              f"Workers leaving: {result['workers_leaving']:,}")

    # 4. Full GE sensitivity
    print("\n--- Full General Equilibrium: Sensitivity to Fund Size ---")
    sensitivity = model.sensitivity_analysis()
    print(f"\n  {'Fund':>8} {'MktCap':>8} {'Share':>7} {'ERP':>6} {'PE':>6} "
          f"{'E[r]':>6} {'UBI/mo':>8} {'GDP':>7} {'dGDP':>7}")
    print("  " + "-" * 75)
    for r in sensitivity:
        print(f"  ${r['fund_size_T']:>6.1f}T ${r['market_cap_T']:>6.1f}T "
              f"{r['fund_share']:>6.1%} {r['erp']:>5.2%} {r['pe_ratio']:>5.1f} "
              f"{r['expected_return']:>5.2%} ${r['monthly_ubi']:>7.0f} "
              f"${r['gdp_T']:>5.1f}T {r['gdp_change']:>+6.2%}")


if __name__ == '__main__':
    run_ge_analysis()
