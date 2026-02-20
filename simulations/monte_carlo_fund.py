"""
Monte Carlo Simulation Engine for Sovereign Wealth Fund Trajectories

Models the stochastic evolution of a sovereign wealth fund under various
accumulation, withdrawal, and market return scenarios.

Key features:
- Regime-switching returns (bull/bear/crisis)
- Mean-reverting equity premium
- Dynamic contribution scaling
- Multiple withdrawal rules
- Stress testing and tail risk analysis

References:
- Campbell & Viceira (2002) "Strategic Asset Allocation"
- Ang (2014) "Asset Management: A Systematic Approach"
- Chambers, Dimson & Ilmanen (2012) "The Norway Model"
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.parameters import *


@dataclass
class MarketRegime:
    """Defines a market regime with characteristic return/vol parameters."""
    name: str
    mean_return: float  # annualized real return
    volatility: float   # annualized std dev
    duration_mean: float  # average years in regime
    transition_probs: dict = field(default_factory=dict)


# Calibrated regime parameters (based on Hamilton 1989, Ang & Bekaert 2002)
REGIMES = {
    'bull': MarketRegime(
        name='bull',
        mean_return=0.12,
        volatility=0.12,
        duration_mean=6.0,
        transition_probs={'bull': 0.85, 'bear': 0.12, 'crisis': 0.03}
    ),
    'bear': MarketRegime(
        name='bear',
        mean_return=-0.02,
        volatility=0.22,
        duration_mean=2.0,
        transition_probs={'bull': 0.40, 'bear': 0.50, 'crisis': 0.10}
    ),
    'crisis': MarketRegime(
        name='crisis',
        mean_return=-0.25,
        volatility=0.40,
        duration_mean=0.75,
        transition_probs={'bull': 0.30, 'bear': 0.50, 'crisis': 0.20}
    ),
}


@dataclass
class FundConfig:
    """Configuration for a sovereign wealth fund simulation."""
    initial_capital: float = INITIAL_SEED_CAPITAL
    annual_contribution: float = ANNUAL_CONTRIBUTION_MID
    contribution_growth_rate: float = GDP_GROWTH_REAL
    withdrawal_rule: str = 'percent_of_fund'  # 'percent_of_fund', 'constant_real', 'hybrid', 'smoothed'
    withdrawal_rate: float = 0.035  # 3.5% of fund
    min_withdrawal: float = 0.0
    max_withdrawal_rate: float = 0.05  # Cap at 5%
    smoothing_factor: float = 0.7  # For smoothed withdrawal rule
    use_regime_switching: bool = True
    accumulation_years: int = 20  # Years before withdrawals begin
    total_years: int = 50
    num_paths: int = MC_NUM_PATHS


class MonteCarloFundSimulator:
    """
    Simulates sovereign wealth fund evolution under uncertainty.

    The fund accumulates capital from multiple revenue sources,
    invests in global equities, and distributes UBI withdrawals
    according to a specified policy rule.
    """

    def __init__(self, config: FundConfig, seed: int = RANDOM_SEED):
        self.config = config
        self.rng = np.random.default_rng(seed)

    def _generate_regime_sequence(self, n_years: int) -> list[str]:
        """Generate a sequence of market regimes using Markov chain."""
        regimes = []
        current = 'bull'  # Start in bull market

        for _ in range(n_years):
            regimes.append(current)
            probs = REGIMES[current].transition_probs
            states = list(probs.keys())
            p = [probs[s] for s in states]
            current = self.rng.choice(states, p=p)

        return regimes

    def _generate_returns(self, n_years: int) -> tuple[np.ndarray, list[str]]:
        """
        Generate annual real returns with regime switching.

        Returns both the return series and the regime labels.
        """
        if self.config.use_regime_switching:
            regimes = self._generate_regime_sequence(n_years)
            returns = np.zeros(n_years)
            for i, regime_name in enumerate(regimes):
                regime = REGIMES[regime_name]
                returns[i] = self.rng.normal(regime.mean_return, regime.volatility)
            return returns, regimes
        else:
            returns = self.rng.normal(
                EQUITY_REAL_RETURN_MEAN,
                EQUITY_REAL_RETURN_STD,
                size=n_years
            )
            regimes = ['normal'] * n_years
            return returns, regimes

    def _compute_withdrawal(self, fund_value: float, year: int,
                            prev_withdrawal: float) -> float:
        """
        Compute withdrawal amount based on the configured policy rule.

        Rules:
        - percent_of_fund: Fixed % of current fund value (Norway model)
        - constant_real: Fixed real dollar amount, inflation-adjusted
        - hybrid: Blend of percent and constant (Yale/Stanford endowment)
        - smoothed: Exponentially smoothed percent-of-fund
        """
        if year < self.config.accumulation_years:
            return 0.0

        rule = self.config.withdrawal_rule

        if rule == 'percent_of_fund':
            withdrawal = fund_value * self.config.withdrawal_rate

        elif rule == 'constant_real':
            # Target: enough for $500/person/month initially, growing with fund
            base = self.config.min_withdrawal if self.config.min_withdrawal > 0 else (
                fund_value * self.config.withdrawal_rate
            )
            withdrawal = base * (1 + GDP_GROWTH_REAL) ** (year - self.config.accumulation_years)

        elif rule == 'hybrid':
            # Yale rule: 70% of last year's spending + 30% of target rate * fund
            target = fund_value * self.config.withdrawal_rate
            if prev_withdrawal > 0:
                withdrawal = 0.7 * prev_withdrawal * (1 + INFLATION_TARGET) + 0.3 * target
            else:
                withdrawal = target

        elif rule == 'smoothed':
            # Exponential smoothing on percent-of-fund
            target = fund_value * self.config.withdrawal_rate
            alpha = 1 - self.config.smoothing_factor
            if prev_withdrawal > 0:
                withdrawal = alpha * target + (1 - alpha) * prev_withdrawal * (1 + INFLATION_TARGET)
            else:
                withdrawal = target

        else:
            raise ValueError(f"Unknown withdrawal rule: {rule}")

        # Apply floor and ceiling
        withdrawal = max(withdrawal, 0)
        withdrawal = min(withdrawal, fund_value * self.config.max_withdrawal_rate)

        return withdrawal

    def simulate_single_path(self) -> dict:
        """
        Simulate a single fund trajectory.

        Returns dict with yearly fund values, withdrawals, contributions,
        returns, regimes, and per-capita UBI amounts.
        """
        T = self.config.total_years
        returns, regimes = self._generate_returns(T)

        fund_values = np.zeros(T + 1)
        withdrawals = np.zeros(T)
        contributions = np.zeros(T)
        ubi_per_capita = np.zeros(T)

        fund_values[0] = self.config.initial_capital

        for t in range(T):
            # Annual contribution (grows with GDP)
            contrib = self.config.annual_contribution * (
                (1 + self.config.contribution_growth_rate) ** t
            )
            contributions[t] = contrib

            # Withdrawal
            prev_w = withdrawals[t - 1] if t > 0 else 0
            withdrawal = self._compute_withdrawal(fund_values[t], t, prev_w)
            withdrawals[t] = withdrawal

            # UBI per capita (real dollars)
            # Population grows ~0.3%/year (slowing)
            pop = US_POPULATION * (1.003 ** t)
            ubi_per_capita[t] = (withdrawal / pop) if withdrawal > 0 else 0

            # Fund evolution: value + contribution - withdrawal, then returns
            pre_return_value = fund_values[t] + contrib - withdrawal
            pre_return_value = max(pre_return_value, 0)  # Can't go negative
            fund_values[t + 1] = pre_return_value * (1 + returns[t])

        return {
            'fund_values': fund_values,
            'withdrawals': withdrawals,
            'contributions': contributions,
            'returns': returns,
            'regimes': regimes,
            'ubi_per_capita': ubi_per_capita,
            'ubi_monthly': ubi_per_capita / 12,
        }

    def simulate(self) -> dict:
        """
        Run full Monte Carlo simulation across all paths.

        Returns aggregated statistics and individual path data.
        """
        N = self.config.num_paths
        T = self.config.total_years

        all_fund_values = np.zeros((N, T + 1))
        all_withdrawals = np.zeros((N, T))
        all_ubi_monthly = np.zeros((N, T))
        all_returns = np.zeros((N, T))

        paths = []
        for i in range(N):
            path = self.simulate_single_path()
            all_fund_values[i] = path['fund_values']
            all_withdrawals[i] = path['withdrawals']
            all_ubi_monthly[i] = path['ubi_monthly']
            all_returns[i] = path['returns']
            if i < 100:  # Store first 100 paths for detailed analysis
                paths.append(path)

        # Compute statistics
        percentiles = [5, 10, 25, 50, 75, 90, 95]

        fund_stats = {
            f'p{p}': np.percentile(all_fund_values, p, axis=0)
            for p in percentiles
        }
        fund_stats['mean'] = np.mean(all_fund_values, axis=0)

        ubi_stats = {
            f'p{p}': np.percentile(all_ubi_monthly, p, axis=0)
            for p in percentiles
        }
        ubi_stats['mean'] = np.mean(all_ubi_monthly, axis=0)

        withdrawal_stats = {
            f'p{p}': np.percentile(all_withdrawals, p, axis=0)
            for p in percentiles
        }
        withdrawal_stats['mean'] = np.mean(all_withdrawals, axis=0)

        # Risk metrics
        fund_final = all_fund_values[:, -1]
        prob_ruin = np.mean(fund_final < self.config.initial_capital * 0.5)
        prob_success = np.mean(fund_final > self.config.initial_capital * 5)

        # Maximum drawdown per path
        max_drawdowns = np.zeros(N)
        for i in range(N):
            cummax = np.maximum.accumulate(all_fund_values[i])
            drawdowns = (cummax - all_fund_values[i]) / np.maximum(cummax, 1)
            max_drawdowns[i] = np.max(drawdowns)

        return {
            'fund_stats': fund_stats,
            'ubi_stats': ubi_stats,
            'withdrawal_stats': withdrawal_stats,
            'prob_ruin': prob_ruin,
            'prob_success': prob_success,
            'max_drawdown_median': np.median(max_drawdowns),
            'max_drawdown_p95': np.percentile(max_drawdowns, 95),
            'paths': paths,
            'all_fund_values': all_fund_values,
            'all_ubi_monthly': all_ubi_monthly,
            'config': self.config,
        }


def run_scenario_analysis():
    """Run multiple scenarios and compare outcomes."""
    scenarios = {
        'baseline': FundConfig(
            initial_capital=500e9,
            annual_contribution=250e9,
            withdrawal_rule='smoothed',
            withdrawal_rate=0.035,
            accumulation_years=20,
            total_years=50,
            num_paths=10_000,
        ),
        'aggressive_accumulation': FundConfig(
            initial_capital=1e12,
            annual_contribution=500e9,
            withdrawal_rule='smoothed',
            withdrawal_rate=0.035,
            accumulation_years=15,
            total_years=50,
            num_paths=10_000,
        ),
        'conservative_withdrawal': FundConfig(
            initial_capital=500e9,
            annual_contribution=250e9,
            withdrawal_rule='percent_of_fund',
            withdrawal_rate=0.03,
            accumulation_years=25,
            total_years=50,
            num_paths=10_000,
        ),
        'hybrid_yale': FundConfig(
            initial_capital=500e9,
            annual_contribution=250e9,
            withdrawal_rule='hybrid',
            withdrawal_rate=0.04,
            accumulation_years=20,
            total_years=50,
            num_paths=10_000,
        ),
    }

    results = {}
    for name, config in scenarios.items():
        print(f"Running scenario: {name}...")
        sim = MonteCarloFundSimulator(config)
        results[name] = sim.simulate()

    return results


def print_results(results: dict):
    """Print formatted results for all scenarios."""
    for name, res in results.items():
        print(f"\n{'='*70}")
        print(f"SCENARIO: {name}")
        print(f"{'='*70}")

        cfg = res['config']
        print(f"  Initial capital:      ${cfg.initial_capital/1e12:.1f}T")
        print(f"  Annual contribution:  ${cfg.annual_contribution/1e9:.0f}B")
        print(f"  Withdrawal rule:      {cfg.withdrawal_rule}")
        print(f"  Withdrawal rate:      {cfg.withdrawal_rate:.1%}")
        print(f"  Accumulation period:  {cfg.accumulation_years} years")

        # Fund value at key milestones
        for year in [10, 20, 30, 40, 50]:
            if year <= cfg.total_years:
                median = res['fund_stats']['p50'][year]
                p5 = res['fund_stats']['p5'][year]
                p95 = res['fund_stats']['p95'][year]
                print(f"\n  Year {year:2d} Fund Value:")
                print(f"    Median: ${median/1e12:.2f}T  "
                      f"[5th: ${p5/1e12:.2f}T, 95th: ${p95/1e12:.2f}T]")

        # UBI at maturity (post-accumulation)
        start_year = cfg.accumulation_years
        for year_offset in [0, 5, 10, 20]:
            year = start_year + year_offset
            if year < cfg.total_years:
                median_ubi = res['ubi_stats']['p50'][year]
                p5_ubi = res['ubi_stats']['p5'][year]
                p95_ubi = res['ubi_stats']['p95'][year]
                print(f"\n  UBI at Year {year} (distribution year {year_offset}):")
                print(f"    Median: ${median_ubi:.0f}/mo  "
                      f"[5th: ${p5_ubi:.0f}/mo, 95th: ${p95_ubi:.0f}/mo]")

        print(f"\n  Risk Metrics:")
        print(f"    P(fund < 50% initial): {res['prob_ruin']:.1%}")
        print(f"    P(fund > 5x initial):  {res['prob_success']:.1%}")
        print(f"    Median max drawdown:   {res['max_drawdown_median']:.1%}")
        print(f"    95th %ile drawdown:    {res['max_drawdown_p95']:.1%}")


if __name__ == '__main__':
    print("UBI Extractor — Monte Carlo Fund Trajectory Simulation")
    print("=" * 70)
    results = run_scenario_analysis()
    print_results(results)
