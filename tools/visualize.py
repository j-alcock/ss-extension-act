"""
Visualization Tools for UBI Extractor

Generates publication-quality charts for:
1. Fund trajectory fan charts (Monte Carlo)
2. UBI payout distributions over time
3. Laffer curve for FTT
4. General equilibrium sensitivity surfaces
5. Withdrawal policy comparison
6. Revenue stack waterfall charts
7. Implementation timeline Gantt chart
"""

import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("matplotlib not installed. Install with: pip install matplotlib")
    print("Falling back to text-based output.")

from data.parameters import *
from simulations.monte_carlo_fund import MonteCarloFundSimulator, FundConfig
from models.general_equilibrium import FTTEquilibriumModel


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_fund_trajectory_fan(result: dict, title: str = "Sovereign Fund Trajectory",
                              filename: str = "fund_trajectory.png"):
    """
    Fan chart showing probability distribution of fund value over time.
    """
    if not HAS_MPL:
        print(f"[SKIP] {filename} — matplotlib not available")
        return

    ensure_output_dir()
    fig, ax = plt.subplots(figsize=(14, 8))

    years = np.arange(len(result['fund_stats']['p50']))

    # Fan bands (light to dark)
    bands = [
        ('p5', 'p95', '#e8f0fe', '90% CI'),
        ('p10', 'p90', '#c6dbef', '80% CI'),
        ('p25', 'p75', '#9ecae1', '50% CI'),
    ]

    for low, high, color, label in bands:
        ax.fill_between(years,
                        result['fund_stats'][low] / 1e12,
                        result['fund_stats'][high] / 1e12,
                        alpha=0.7, color=color, label=label)

    # Median line
    ax.plot(years, result['fund_stats']['p50'] / 1e12,
            color='#2171b5', linewidth=2.5, label='Median')

    # Mean line (dashed)
    ax.plot(years, result['fund_stats']['mean'] / 1e12,
            color='#084594', linewidth=1.5, linestyle='--', label='Mean')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Fund Value ($ Trillions)', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('$%.0fT'))
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, len(years) - 1)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"  Saved: {filepath}")


def plot_ubi_distribution_over_time(result: dict, start_year: int = 20,
                                     filename: str = "ubi_distribution.png"):
    """
    Chart showing monthly UBI per capita over time with uncertainty bands.
    """
    if not HAS_MPL:
        print(f"[SKIP] {filename} — matplotlib not available")
        return

    ensure_output_dir()
    fig, ax = plt.subplots(figsize=(14, 8))

    T = len(result['ubi_stats']['p50'])
    years = np.arange(T)

    bands = [
        ('p5', 'p95', '#fde0dd', '90% CI'),
        ('p10', 'p90', '#fa9fb5', '80% CI'),
        ('p25', 'p75', '#f768a1', '50% CI'),
    ]

    for low, high, color, label in bands:
        ax.fill_between(years[start_year:],
                        result['ubi_stats'][low][start_year:],
                        result['ubi_stats'][high][start_year:],
                        alpha=0.6, color=color, label=label)

    ax.plot(years[start_year:], result['ubi_stats']['p50'][start_year:],
            color='#ae017e', linewidth=2.5, label='Median UBI')

    ax.axhline(y=500, color='gray', linestyle=':', alpha=0.5, label='$500/mo reference')
    ax.axhline(y=1000, color='gray', linestyle='--', alpha=0.5, label='$1000/mo reference')

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Monthly UBI per Person ($)', fontsize=12)
    ax.set_title('Monthly UBI Distribution Over Time', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax.grid(True, alpha=0.3)
    ax.set_xlim(start_year, T - 1)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"  Saved: {filepath}")


def plot_ftt_laffer_curve(filename: str = "ftt_laffer_curve.png"):
    """
    Laffer curve for the Financial Transaction Tax.
    """
    if not HAS_MPL:
        print(f"[SKIP] {filename} — matplotlib not available")
        return

    ensure_output_dir()
    fig, ax = plt.subplots(figsize=(12, 7))

    for elasticity, color, label in [
        (-0.4, '#2ca02c', 'Low elasticity (-0.4)'),
        (-0.8, '#1f77b4', 'Central (-0.8)'),
        (-1.2, '#ff7f0e', 'High elasticity (-1.2)'),
        (-1.6, '#d62728', 'Very high (-1.6)'),
    ]:
        model = FTTEquilibriumModel(volume_elasticity=elasticity)
        curve = model.laffer_curve(200)
        ax.plot(curve['rates_bps'], curve['revenues'] / 1e9,
                color=color, linewidth=2, label=label)

        # Mark the peak
        peak_idx = np.argmax(curve['revenues'])
        ax.plot(curve['rates_bps'][peak_idx], curve['revenues'][peak_idx] / 1e9,
                'o', color=color, markersize=8)

    ax.set_xlabel('Tax Rate (basis points)', fontsize=12)
    ax.set_ylabel('Annual Revenue ($ Billions)', fontsize=12)
    ax.set_title('Financial Transaction Tax — Laffer Curve', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'${x:,.0f}B'))

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"  Saved: {filepath}")


def plot_revenue_stack_waterfall(fund_size_t: float = 10.0,
                                  filename: str = "revenue_waterfall.png"):
    """
    Waterfall chart showing revenue stack composition.
    """
    if not HAS_MPL:
        print(f"[SKIP] {filename} — matplotlib not available")
        return

    ensure_output_dir()
    from models.revenue_stack import RevenueStackModel

    model = RevenueStackModel(fund_size_t * 1e12)
    stack = model.compute_full_stack()

    sources = stack['sources']
    names = [s.name for s in sources]
    values = [s.annual_revenue / 1e9 for s in sources]
    feasibility = [s.political_feasibility for s in sources]

    fig, ax = plt.subplots(figsize=(14, 8))

    # Sort by revenue
    sorted_idx = np.argsort(values)[::-1]
    names = [names[i] for i in sorted_idx]
    values = [values[i] for i in sorted_idx]
    feasibility = [feasibility[i] for i in sorted_idx]

    colors = [plt.cm.RdYlGn(f) for f in feasibility]

    bars = ax.barh(range(len(names)), values, color=colors, edgecolor='gray', linewidth=0.5)

    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=11)
    ax.set_xlabel('Annual Revenue ($ Billions)', fontsize=12)
    ax.set_title(f'Revenue Stack — ${fund_size_t:.0f}T Fund\n(Color = Political Feasibility: Red=Low, Green=High)',
                 fontsize=14, fontweight='bold')

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
                f'${val:.0f}B', va='center', fontsize=10)

    ax.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"  Saved: {filepath}")


def plot_scenario_comparison(results: dict, filename: str = "scenario_comparison.png"):
    """
    Side-by-side comparison of multiple scenarios.
    """
    if not HAS_MPL:
        print(f"[SKIP] {filename} — matplotlib not available")
        return

    ensure_output_dir()
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    # Panel 1: Fund value median trajectories
    ax = axes[0, 0]
    for i, (name, res) in enumerate(results.items()):
        years = np.arange(len(res['fund_stats']['p50']))
        ax.plot(years, res['fund_stats']['p50'] / 1e12,
                color=colors[i % len(colors)], linewidth=2, label=name)
    ax.set_title('Median Fund Value', fontweight='bold')
    ax.set_ylabel('$ Trillions')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Panel 2: Median UBI
    ax = axes[0, 1]
    for i, (name, res) in enumerate(results.items()):
        T = len(res['ubi_stats']['p50'])
        years = np.arange(T)
        ax.plot(years, res['ubi_stats']['p50'],
                color=colors[i % len(colors)], linewidth=2, label=name)
    ax.set_title('Median Monthly UBI', fontweight='bold')
    ax.set_ylabel('$/month per person')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Panel 3: Risk (P(ruin) comparison)
    ax = axes[1, 0]
    names = list(results.keys())
    ruins = [results[n]['prob_ruin'] for n in names]
    drawdowns = [results[n]['max_drawdown_median'] for n in names]
    x = range(len(names))
    ax.bar(x, [r * 100 for r in ruins], color=colors[:len(names)], alpha=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=15)
    ax.set_title('Probability of Fund Ruin (%)', fontweight='bold')
    ax.set_ylabel('%')
    ax.grid(True, alpha=0.3, axis='y')

    # Panel 4: UBI at Year 30 (distribution)
    ax = axes[1, 1]
    for i, (name, res) in enumerate(results.items()):
        ubi_at_30 = res['all_ubi_monthly'][:, min(30, res['all_ubi_monthly'].shape[1] - 1)]
        ubi_at_30 = ubi_at_30[ubi_at_30 > 0]
        if len(ubi_at_30) > 0:
            ax.hist(ubi_at_30, bins=50, alpha=0.5, color=colors[i % len(colors)],
                    label=name, density=True)
    ax.set_title('UBI Distribution at Year 30', fontweight='bold')
    ax.set_xlabel('$/month per person')
    ax.set_ylabel('Density')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.suptitle('UBI Extractor — Scenario Comparison', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filepath}")


def generate_all_charts():
    """Generate all visualization charts."""
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)

    # 1. Fund trajectory fan chart
    print("\n  Generating fund trajectory fan chart...")
    config = FundConfig(
        initial_capital=500e9,
        annual_contribution=250e9,
        withdrawal_rule='smoothed',
        withdrawal_rate=0.035,
        accumulation_years=20,
        total_years=50,
        num_paths=5_000,
    )
    sim = MonteCarloFundSimulator(config)
    result = sim.simulate()
    plot_fund_trajectory_fan(result)

    # 2. UBI distribution over time
    print("  Generating UBI distribution chart...")
    plot_ubi_distribution_over_time(result)

    # 3. FTT Laffer curve
    print("  Generating FTT Laffer curve...")
    plot_ftt_laffer_curve()

    # 4. Revenue waterfall
    print("  Generating revenue stack waterfall...")
    plot_revenue_stack_waterfall()

    # 5. Scenario comparison
    print("  Generating scenario comparison...")
    scenarios = {
        'Conservative': FundConfig(
            initial_capital=500e9, annual_contribution=200e9,
            withdrawal_rule='smoothed', withdrawal_rate=0.03,
            accumulation_years=25, total_years=50, num_paths=3_000,
        ),
        'Baseline': FundConfig(
            initial_capital=500e9, annual_contribution=250e9,
            withdrawal_rule='smoothed', withdrawal_rate=0.035,
            accumulation_years=20, total_years=50, num_paths=3_000,
        ),
        'Aggressive': FundConfig(
            initial_capital=1e12, annual_contribution=500e9,
            withdrawal_rule='hybrid', withdrawal_rate=0.04,
            accumulation_years=15, total_years=50, num_paths=3_000,
        ),
    }
    mc_results = {}
    for name, cfg in scenarios.items():
        sim = MonteCarloFundSimulator(cfg)
        mc_results[name] = sim.simulate()
    plot_scenario_comparison(mc_results)

    print("\n  All charts generated in output/ directory.")


if __name__ == '__main__':
    generate_all_charts()
