"""
Composite Revenue Stack Model

Models the full set of revenue extraction mechanisms available to
a sovereign entity operating in equity markets.

Revenue Sources:
1. Equity Risk Premium (passive index holding)
2. Volatility Risk Premium (systematic options selling)
3. Securities Lending Income
4. Financial Transaction Tax
5. Corporate Equity Stakes (mandatory equity contributions)
6. Federal Asset Monetization (spectrum, mineral rights, land)
7. Market-Making Spread Capture

Each source has different capacity limits, risk profiles, and
sensitivity to the fund's own scale.

The key challenge is that these sources are not independent:
- Larger fund -> more lending income but lower ERP
- Higher FTT -> more revenue but lower volume -> less spread income
- More vol selling -> compressed VRP
"""

import numpy as np
from dataclasses import dataclass
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.parameters import *


@dataclass
class RevenueSource:
    """A single revenue source with its characteristics."""
    name: str
    annual_revenue: float       # Expected annual revenue ($)
    revenue_std: float          # Revenue volatility ($)
    capacity_limit: float       # Max feasible scale ($)
    scalability: float          # 0-1, how well it scales with fund size
    correlation_equity: float   # Correlation with equity returns
    political_feasibility: float  # 0-1, how politically achievable
    implementation_years: int   # Years to implement


class RevenueStackModel:
    """
    Models the composite revenue stack and interactions between sources.
    """

    def __init__(self, fund_size: float = 10e12):
        self.fund_size = fund_size

    def equity_risk_premium_revenue(self) -> RevenueSource:
        """
        Revenue from passive equity holdings.
        The foundation of the strategy — collect the ERP.
        """
        # ERP compresses as fund grows (GE effect)
        erp_compression = ERP_COMPRESSION_PER_TRILLION * (self.fund_size / 1e12)
        effective_erp = max(EQUITY_RISK_PREMIUM_MEAN - erp_compression, 0.02)

        revenue = self.fund_size * effective_erp
        revenue_std = self.fund_size * EQUITY_REAL_RETURN_STD

        return RevenueSource(
            name="Equity Risk Premium",
            annual_revenue=revenue,
            revenue_std=revenue_std,
            capacity_limit=GLOBAL_EQUITY_MARKET_CAP * 0.15,  # 15% of global market
            scalability=0.8,  # Degrades with scale
            correlation_equity=1.0,
            political_feasibility=0.7,
            implementation_years=5,
        )

    def volatility_risk_premium_revenue(self) -> RevenueSource:
        """
        Revenue from systematic volatility selling.

        Strategy: Sell OTM puts on broad indices, harvesting the
        persistent gap between implied and realized volatility.

        Capacity is limited — the VRP compresses with more sellers.
        """
        # Base revenue: 3-5% of notional
        notional = min(self.fund_size * 0.10, VOL_STRATEGY_CAPACITY_USD)

        # VRP compresses as more capital enters
        capital_in_vol = notional
        vrp_compression = 0.5 * (capital_in_vol / VOL_STRATEGY_CAPACITY_USD)
        effective_vrp = max(PUT_SELLING_EXCESS_RETURN - vrp_compression * PUT_SELLING_EXCESS_RETURN, 0.01)

        revenue = notional * effective_vrp

        return RevenueSource(
            name="Volatility Risk Premium",
            annual_revenue=revenue,
            revenue_std=revenue * 2.5,  # High vol of vol
            capacity_limit=VOL_STRATEGY_CAPACITY_USD,
            scalability=0.3,  # Very limited scalability
            correlation_equity=0.6,  # Correlated but not 1:1
            political_feasibility=0.5,  # Controversial (public fund selling puts)
            implementation_years=3,
        )

    def securities_lending_revenue(self) -> RevenueSource:
        """
        Revenue from lending equity holdings to short sellers.

        A sovereign fund with $10T in equities would be the largest
        securities lender in the world, with significant pricing power.
        """
        lendable = self.fund_size * PORTFOLIO_ON_LOAN_PCT
        avg_fee = AVG_LENDING_FEE_BPS / 10000

        # Pricing power: larger lender can demand higher fees
        pricing_power_bonus = min(0.001 * (self.fund_size / 1e12), 0.002)
        effective_fee = avg_fee + pricing_power_bonus

        revenue = lendable * effective_fee

        return RevenueSource(
            name="Securities Lending",
            annual_revenue=revenue,
            revenue_std=revenue * 0.3,
            capacity_limit=self.fund_size * 0.30,  # Can lend up to 30%
            scalability=0.9,  # Scales well with holdings
            correlation_equity=-0.2,  # Lending fees rise in stress
            political_feasibility=0.8,  # Low controversy
            implementation_years=2,
        )

    def ftt_revenue(self, tax_rate: float = FTT_RATE_LOW) -> RevenueSource:
        """
        Revenue from a Financial Transaction Tax.
        See general_equilibrium.py for full Laffer curve analysis.
        """
        baseline_cost = EFFECTIVE_SPREAD_BPS / 10000
        cost_increase_pct = tax_rate / baseline_cost
        volume_change = VOLUME_ELASTICITY_MID * cost_increase_pct
        new_volume = ANNUAL_EQUITY_VOLUME * max(1 + volume_change, 0.1)
        revenue = tax_rate * new_volume * 2

        return RevenueSource(
            name="Financial Transaction Tax",
            annual_revenue=revenue,
            revenue_std=revenue * 0.2,
            capacity_limit=revenue * 1.5,  # Could go higher with higher rate
            scalability=0.6,
            correlation_equity=0.3,  # Volume is procyclical
            political_feasibility=0.4,  # Highly contested
            implementation_years=3,
        )

    def corporate_equity_stakes_revenue(self) -> RevenueSource:
        """
        Revenue from mandatory corporate equity contributions.

        Model: Companies above a certain size contribute X% of new
        equity issuance to the sovereign fund annually.

        Precedent: Sweden's "Meidner Plan" (1976), though it was
        ultimately not implemented due to corporate opposition.
        """
        # Fortune 500 annual profits: ~$2T
        # If 2% of profits contributed as equity to the fund:
        contribution_rate = 0.02
        corporate_profits = 2e12
        revenue = corporate_profits * contribution_rate

        return RevenueSource(
            name="Corporate Equity Stakes",
            annual_revenue=revenue,
            revenue_std=revenue * 0.3,
            capacity_limit=corporate_profits * 0.05,
            scalability=0.7,
            correlation_equity=0.8,
            political_feasibility=0.2,  # Very difficult politically
            implementation_years=10,
        )

    def federal_asset_monetization_revenue(self) -> RevenueSource:
        """
        Revenue from monetizing federal assets.

        Sources:
        - Electromagnetic spectrum auctions (~$5-10B/year)
        - Mineral rights and drilling leases (~$10-15B/year)
        - Federal land leases (~$5-10B/year)
        - Data licensing (census, weather, GPS) (~$1-5B/year)
        """
        spectrum = 7.5e9
        minerals = 12e9
        land = 7e9
        data = 3e9
        total = spectrum + minerals + land + data

        return RevenueSource(
            name="Federal Asset Monetization",
            annual_revenue=total,
            revenue_std=total * 0.25,
            capacity_limit=total * 2,  # Could expand with new assets
            scalability=0.4,  # Finite assets
            correlation_equity=0.1,
            political_feasibility=0.6,
            implementation_years=5,
        )

    def market_making_revenue(self) -> RevenueSource:
        """
        Revenue from sovereign market-making operations.

        The fund could operate as a market-maker, capturing bid-ask
        spreads. However, there are serious conflicts of interest
        when a government entity makes markets.
        """
        # Top market makers earn $5-10B/year
        # A sovereign entity with privileged access could earn more
        # but would face enormous regulatory and fairness issues
        revenue = 5e9  # Conservative

        return RevenueSource(
            name="Market Making",
            annual_revenue=revenue,
            revenue_std=revenue * 0.5,
            capacity_limit=15e9,
            scalability=0.4,
            correlation_equity=0.2,
            political_feasibility=0.1,  # Extremely controversial
            implementation_years=7,
        )

    def compute_full_stack(self) -> dict:
        """
        Compute the full revenue stack with interactions.
        """
        sources = [
            self.equity_risk_premium_revenue(),
            self.volatility_risk_premium_revenue(),
            self.securities_lending_revenue(),
            self.ftt_revenue(),
            self.corporate_equity_stakes_revenue(),
            self.federal_asset_monetization_revenue(),
            self.market_making_revenue(),
        ]

        total_revenue = sum(s.annual_revenue for s in sources)
        total_variance = sum(s.revenue_std ** 2 for s in sources)

        # Cross-correlations reduce total variance
        # (diversification benefit across uncorrelated sources)
        diversified_std = np.sqrt(total_variance * 0.7)  # Rough correlation adjustment

        per_capita_annual = total_revenue / US_POPULATION
        per_capita_monthly = per_capita_annual / 12

        # Feasibility-weighted revenue (weight by political feasibility)
        feasible_revenue = sum(s.annual_revenue * s.political_feasibility for s in sources)
        feasible_per_capita = (feasible_revenue / US_POPULATION) / 12

        return {
            'sources': sources,
            'total_revenue': total_revenue,
            'total_std': diversified_std,
            'per_capita_annual': per_capita_annual,
            'per_capita_monthly': per_capita_monthly,
            'feasible_revenue': feasible_revenue,
            'feasible_per_capita_monthly': feasible_per_capita,
            'sharpe_ratio': total_revenue / diversified_std,
        }


def run_revenue_analysis():
    """Run revenue stack analysis across fund sizes."""
    print("=" * 80)
    print("REVENUE STACK ANALYSIS")
    print("=" * 80)

    for fund_size in [2.5e12, 5e12, 10e12, 15e12]:
        print(f"\n--- Fund Size: ${fund_size/1e12:.1f}T ---")
        model = RevenueStackModel(fund_size)
        stack = model.compute_full_stack()

        print(f"\n  {'Source':<30} {'Revenue':>12} {'Std Dev':>12} {'Feasibility':>12}")
        print("  " + "-" * 70)

        for src in stack['sources']:
            print(f"  {src.name:<30} ${src.annual_revenue/1e9:>10.1f}B "
                  f"${src.revenue_std/1e9:>10.1f}B {src.political_feasibility:>10.0%}")

        print(f"\n  {'TOTAL':<30} ${stack['total_revenue']/1e9:>10.1f}B "
              f"${stack['total_std']/1e9:>10.1f}B")
        print(f"  Per capita (monthly):          ${stack['per_capita_monthly']:>10.0f}")
        print(f"  Feasibility-weighted UBI:      ${stack['feasible_per_capita_monthly']:>10.0f}/mo")
        print(f"  Portfolio Sharpe Ratio:         {stack['sharpe_ratio']:>10.2f}")


if __name__ == '__main__':
    run_revenue_analysis()
