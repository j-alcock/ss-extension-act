"""
Optimal Dynamic Withdrawal Policy for Sovereign UBI Fund

Implements and compares withdrawal rules for converting sovereign fund
returns into stable UBI payments. Key challenge: maximize payout stability
while preserving fund sustainability across market cycles.

Models:
1. Constant Percentage (Norway/GPFG model)
2. Constant Real Dollar (traditional endowment)
3. Hybrid Rule (Yale/Stanford model)
4. Exponential Smoothing
5. Actuarial/Liability-Driven (novel: match UBI obligation stream)
6. Optimal Control (Hamilton-Jacobi-Bellman solution)

References:
- Dybvig (1995) "Dusenberry's Ratcheting of Consumption"
- Waring & Siegel (2015) "The Only Spending Rule Article You'll Ever Need"
- Ang, Papanikolaou & Westerfield (2014) "Portfolio Choice with Illiquid Assets"
- Merton (1969, 1971) optimal consumption-portfolio problem
"""

import numpy as np
from scipy.optimize import minimize_scalar, minimize
from dataclasses import dataclass
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.parameters import *


@dataclass
class WithdrawalResult:
    """Results from a withdrawal policy simulation."""
    withdrawals: np.ndarray      # Annual withdrawal amounts
    fund_values: np.ndarray      # Fund value trajectory
    ubi_monthly: np.ndarray      # Monthly UBI per capita
    shortfall_years: int         # Years where UBI < target floor
    volatility: float            # Std dev of annual UBI changes
    utility: float               # Expected utility (CRRA)
    sustainability_score: float  # P(fund survives full horizon)


class WithdrawalPolicyEngine:
    """
    Evaluates and optimizes withdrawal policies for a sovereign UBI fund.

    The engine takes a set of market return paths and evaluates how different
    withdrawal rules translate fund returns into UBI payments.
    """

    def __init__(self, return_paths: np.ndarray, initial_fund: float,
                 annual_contributions: np.ndarray, population_path: np.ndarray):
        """
        Args:
            return_paths: (N_paths, T) array of annual real returns
            initial_fund: Starting fund value
            annual_contributions: (T,) array of annual inflows
            population_path: (T,) array of population projections
        """
        self.return_paths = return_paths
        self.initial_fund = initial_fund
        self.contributions = annual_contributions
        self.population = population_path
        self.N, self.T = return_paths.shape

    def simulate_policy(self, withdrawal_fn, **kwargs) -> list[WithdrawalResult]:
        """
        Simulate a withdrawal function across all return paths.

        Args:
            withdrawal_fn: callable(fund_value, year, prev_withdrawal, **kwargs) -> withdrawal
        """
        results = []

        for i in range(self.N):
            fund_vals = np.zeros(self.T + 1)
            withdrawals = np.zeros(self.T)
            ubi_monthly = np.zeros(self.T)

            fund_vals[0] = self.initial_fund

            for t in range(self.T):
                prev_w = withdrawals[t - 1] if t > 0 else 0
                w = withdrawal_fn(fund_vals[t], t, prev_w, **kwargs)
                w = max(0, min(w, fund_vals[t] * 0.10))  # Hard cap at 10%
                withdrawals[t] = w
                ubi_monthly[t] = (w / self.population[t]) / 12

                pre_return = fund_vals[t] + self.contributions[t] - w
                pre_return = max(pre_return, 0)
                fund_vals[t + 1] = pre_return * (1 + self.return_paths[i, t])

            # Compute metrics
            ubi_changes = np.diff(ubi_monthly)
            ubi_changes = ubi_changes[ubi_monthly[1:] > 0]  # Only during distribution

            results.append(WithdrawalResult(
                withdrawals=withdrawals,
                fund_values=fund_vals,
                ubi_monthly=ubi_monthly,
                shortfall_years=int(np.sum(ubi_monthly < 50)),  # Below $50/mo
                volatility=float(np.std(ubi_changes)) if len(ubi_changes) > 0 else 0,
                utility=self._crra_utility(ubi_monthly),
                sustainability_score=float(fund_vals[-1] > self.initial_fund * 0.5),
            ))

        return results

    @staticmethod
    def _crra_utility(consumption: np.ndarray, gamma: float = 2.0,
                      beta: float = 0.97) -> float:
        """
        Compute discounted CRRA utility of consumption stream.

        U = sum_t beta^t * c_t^(1-gamma) / (1-gamma)

        Args:
            consumption: Monthly UBI stream
            gamma: Relative risk aversion coefficient
            beta: Time discount factor
        """
        c = np.maximum(consumption, 1.0)  # Floor to avoid log(0)

        if gamma == 1.0:
            period_utility = np.log(c)
        else:
            period_utility = (c ** (1 - gamma)) / (1 - gamma)

        discount_factors = beta ** np.arange(len(c))
        return float(np.sum(discount_factors * period_utility))

    # === WITHDRAWAL RULE IMPLEMENTATIONS ===

    @staticmethod
    def constant_percentage(fund_value, year, prev_withdrawal,
                           rate=0.035, start_year=20):
        """Norway GPFG model: fixed percentage of current fund value."""
        if year < start_year:
            return 0.0
        return fund_value * rate

    @staticmethod
    def constant_real(fund_value, year, prev_withdrawal,
                     initial_amount=200e9, growth=0.02, start_year=20):
        """Fixed real dollar withdrawal, growing with inflation."""
        if year < start_year:
            return 0.0
        target = initial_amount * (1 + growth) ** (year - start_year)
        return min(target, fund_value * 0.08)  # Safety cap

    @staticmethod
    def hybrid_yale(fund_value, year, prev_withdrawal,
                   rate=0.04, weight_prev=0.7, start_year=20):
        """
        Yale/Stanford endowment model.
        Blends last year's spending (inflation-adjusted) with target rate.
        """
        if year < start_year:
            return 0.0
        target = fund_value * rate
        if prev_withdrawal > 0:
            return weight_prev * prev_withdrawal * 1.02 + (1 - weight_prev) * target
        return target

    @staticmethod
    def smoothed_percentage(fund_value, year, prev_withdrawal,
                           rate=0.035, alpha=0.3, start_year=20):
        """Exponential smoothing on percentage-of-fund withdrawals."""
        if year < start_year:
            return 0.0
        target = fund_value * rate
        if prev_withdrawal > 0:
            return alpha * target + (1 - alpha) * prev_withdrawal * 1.02
        return target

    @staticmethod
    def liability_driven(fund_value, year, prev_withdrawal,
                        base_rate=0.035, floor_rate=0.02, ceiling_rate=0.05,
                        funded_ratio_target=1.5, start_year=20):
        """
        Liability-driven withdrawal: adjusts rate based on funded ratio.

        When the fund is well-funded (high ratio of assets to UBI obligations),
        increase payouts. When underfunded, reduce to floor.

        This is a novel approach adapted from pension fund ALM.
        """
        if year < start_year:
            return 0.0

        # Estimate UBI liability as PV of 30-year commitment
        annual_obligation = US_POPULATION * TARGET_UBI_ANNUAL
        discount_rate = EQUITY_REAL_RETURN_MEAN
        pv_factor = (1 - (1 + discount_rate) ** -30) / discount_rate
        liability_pv = annual_obligation * pv_factor

        funded_ratio = fund_value / max(liability_pv, 1)

        if funded_ratio >= funded_ratio_target:
            rate = ceiling_rate
        elif funded_ratio >= 1.0:
            # Linear interpolation
            frac = (funded_ratio - 1.0) / (funded_ratio_target - 1.0)
            rate = base_rate + frac * (ceiling_rate - base_rate)
        elif funded_ratio >= 0.5:
            frac = (funded_ratio - 0.5) / 0.5
            rate = floor_rate + frac * (base_rate - floor_rate)
        else:
            rate = floor_rate

        return fund_value * rate

    @staticmethod
    def ratcheted(fund_value, year, prev_withdrawal,
                 rate=0.035, ratchet_up_pct=0.03, start_year=20):
        """
        Dybvig ratchet: UBI can increase but never decrease.

        Based on Dybvig (1995): consumption can only ratchet up, never down.
        This provides maximum stability at the cost of lower average payouts.
        """
        if year < start_year:
            return 0.0
        target = fund_value * rate
        if prev_withdrawal > 0:
            # Can only increase by ratchet_up_pct or match target if lower
            floor = prev_withdrawal  # Never decrease
            ceiling = prev_withdrawal * (1 + ratchet_up_pct)
            return min(max(target, floor), ceiling)
        return target


def optimize_withdrawal_rate(engine: WithdrawalPolicyEngine,
                            policy_fn, start_year: int = 20,
                            rate_range: tuple = (0.02, 0.06)) -> dict:
    """
    Find the withdrawal rate that maximizes expected utility
    subject to a sustainability constraint.

    Uses grid search + refinement since the objective is noisy.
    """

    def objective(rate):
        results = engine.simulate_policy(
            policy_fn, rate=rate, start_year=start_year
        )
        mean_utility = np.mean([r.utility for r in results])
        sustainability = np.mean([r.sustainability_score for r in results])

        # Penalize if sustainability drops below 90%
        penalty = 0
        if sustainability < 0.90:
            penalty = 1000 * (0.90 - sustainability) ** 2

        return -(mean_utility - penalty)  # Negative because we minimize

    result = minimize_scalar(objective, bounds=rate_range, method='bounded')

    optimal_rate = result.x
    optimal_results = engine.simulate_policy(
        policy_fn, rate=optimal_rate, start_year=start_year
    )

    return {
        'optimal_rate': optimal_rate,
        'expected_utility': np.mean([r.utility for r in optimal_results]),
        'median_ubi_at_30': np.median([r.ubi_monthly[30] for r in optimal_results]),
        'sustainability': np.mean([r.sustainability_score for r in optimal_results]),
        'ubi_volatility': np.mean([r.volatility for r in optimal_results]),
    }


def compare_all_policies():
    """
    Compare all withdrawal policies on identical return paths.
    """
    rng = np.random.default_rng(RANDOM_SEED)
    T = 50
    N = 5_000

    # Generate return paths
    returns = rng.normal(EQUITY_REAL_RETURN_MEAN, EQUITY_REAL_RETURN_STD, (N, T))

    # Contributions: $250B/year growing at GDP rate
    contributions = np.array([
        ANNUAL_CONTRIBUTION_MID * (1 + GDP_GROWTH_REAL) ** t for t in range(T)
    ])

    # Population projection
    population = np.array([
        US_POPULATION * (1.003 ** t) for t in range(T)
    ])

    engine = WithdrawalPolicyEngine(returns, INITIAL_SEED_CAPITAL, contributions, population)

    policies = {
        'Constant %': (engine.constant_percentage, {'rate': 0.035}),
        'Constant Real': (engine.constant_real, {'initial_amount': 200e9}),
        'Hybrid (Yale)': (engine.hybrid_yale, {'rate': 0.04}),
        'Smoothed %': (engine.smoothed_percentage, {'rate': 0.035}),
        'Liability-Driven': (engine.liability_driven, {}),
        'Ratcheted': (engine.ratcheted, {'rate': 0.035}),
    }

    print(f"\n{'Policy':<20} {'Med UBI(Y30)':<14} {'Med UBI(Y40)':<14} "
          f"{'Vol':<10} {'Sustain':<10} {'Utility':<12}")
    print("-" * 80)

    for name, (fn, kwargs) in policies.items():
        results = engine.simulate_policy(fn, start_year=20, **kwargs)

        med_ubi_30 = np.median([r.ubi_monthly[30] for r in results])
        med_ubi_40 = np.median([r.ubi_monthly[40] for r in results])
        vol = np.mean([r.volatility for r in results])
        sustain = np.mean([r.sustainability_score for r in results])
        utility = np.mean([r.utility for r in results])

        print(f"{name:<20} ${med_ubi_30:<13.0f} ${med_ubi_40:<13.0f} "
              f"{vol:<10.1f} {sustain:<10.1%} {utility:<12.1f}")

    # Optimize the smoothed percentage
    print("\n--- Optimizing smoothed percentage rate ---")
    opt = optimize_withdrawal_rate(engine, engine.smoothed_percentage)
    print(f"Optimal rate: {opt['optimal_rate']:.3%}")
    print(f"Median UBI at Year 30: ${opt['median_ubi_at_30']:.0f}/month")
    print(f"Sustainability: {opt['sustainability']:.1%}")
    print(f"UBI Volatility: ${opt['ubi_volatility']:.1f}/month")


if __name__ == '__main__':
    print("UBI Extractor — Withdrawal Policy Comparison & Optimization")
    print("=" * 70)
    compare_all_policies()
