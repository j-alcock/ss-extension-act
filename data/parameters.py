"""
Calibrated parameters for UBI Extractor models.

Sources:
- Equity risk premium: Damodaran (2024), Dimson-Marsh-Staunton (2023)
- Market microstructure: SEC MIDAS data, CBOE volatility indices
- Macro: BEA, BLS, Federal Reserve FRED
- Sovereign fund benchmarks: NBIM, APFC, GIC annual reports
"""

# === POPULATION & UBI TARGETS ===
US_POPULATION = 330_000_000
TARGET_UBI_MONTHLY = 1000  # $/month per person
TARGET_UBI_ANNUAL = TARGET_UBI_MONTHLY * 12
TOTAL_ANNUAL_COST = TARGET_UBI_ANNUAL * US_POPULATION  # ~$3.96T

# === EQUITY MARKET PARAMETERS ===
US_EQUITY_MARKET_CAP = 55e12  # $55T (2024 estimate)
GLOBAL_EQUITY_MARKET_CAP = 110e12  # $110T

# Historical equity risk premium (geometric, real)
EQUITY_RISK_PREMIUM_MEAN = 0.05  # 5% real
EQUITY_RISK_PREMIUM_STD = 0.17  # 17% annual volatility
RISK_FREE_RATE_REAL = 0.015  # 1.5% real

# Total real equity return
EQUITY_REAL_RETURN_MEAN = EQUITY_RISK_PREMIUM_MEAN + RISK_FREE_RATE_REAL
EQUITY_REAL_RETURN_STD = EQUITY_RISK_PREMIUM_STD

# Dividend yield (S&P 500 historical)
DIVIDEND_YIELD = 0.018  # 1.8%
BUYBACK_YIELD = 0.025  # 2.5% (shareholder yield component)
TOTAL_SHAREHOLDER_YIELD = DIVIDEND_YIELD + BUYBACK_YIELD

# === MARKET MICROSTRUCTURE ===
DAILY_EQUITY_VOLUME_USD = 600e9  # $600B/day
ANNUAL_TRADING_DAYS = 252
ANNUAL_EQUITY_VOLUME = DAILY_EQUITY_VOLUME_USD * ANNUAL_TRADING_DAYS

# Bid-ask spreads (median, large-cap)
MEDIAN_SPREAD_BPS = 2.0  # basis points
EFFECTIVE_SPREAD_BPS = 1.0  # half-spread, effective cost

# === FINANCIAL TRANSACTION TAX ===
FTT_RATE_BASELINE = 0.001  # 0.1% (10 bps)
FTT_RATE_LOW = 0.0005  # 0.05% (5 bps)
FTT_RATE_HIGH = 0.002  # 0.2% (20 bps)

# Volume elasticity to transaction costs (literature range)
VOLUME_ELASTICITY_LOW = -0.4  # Baltagi et al (2006)
VOLUME_ELASTICITY_MID = -0.8  # Central estimate
VOLUME_ELASTICITY_HIGH = -1.6  # Swedish experience

# === VOLATILITY RISK PREMIUM ===
VIX_MEAN = 19.5  # Long-run VIX average
REALIZED_VOL_MEAN = 15.5  # Long-run realized vol
VOL_RISK_PREMIUM = (VIX_MEAN - REALIZED_VOL_MEAN) / 100  # ~4% annualized
PUT_SELLING_EXCESS_RETURN = 0.035  # 3.5% above equity return (CBOE PUT index)
VOL_STRATEGY_CAPACITY_USD = 50e9  # Approximate capacity before degradation

# === SECURITIES LENDING ===
AVG_LENDING_FEE_BPS = 40  # 40 bps average across portfolio
HIGH_DEMAND_LENDING_FEE_BPS = 200  # Hard-to-borrow names
PORTFOLIO_ON_LOAN_PCT = 0.15  # 15% of holdings lent out

# === SOVEREIGN FUND BENCHMARKS ===
# Norway GPFG
NORWAY_FUND_SIZE = 1.6e12
NORWAY_SPENDING_RULE = 0.03  # 3% of fund value
NORWAY_HISTORICAL_RETURN = 0.066  # 6.6% nominal

# Alaska Permanent Fund
ALASKA_FUND_SIZE = 78e9
ALASKA_PCT_OF_MARKET_INCOME = 0.05  # Percent-of-market-value rule

# === FUND ACCUMULATION SCENARIOS ===
ACCUMULATION_PERIOD_YEARS = 30
INITIAL_SEED_CAPITAL = 500e9  # $500B initial seed
ANNUAL_CONTRIBUTION_LOW = 100e9  # $100B/year
ANNUAL_CONTRIBUTION_MID = 250e9  # $250B/year
ANNUAL_CONTRIBUTION_HIGH = 500e9  # $500B/year

# Contribution sources
FTT_REVENUE_ESTIMATE = 60e9  # After behavioral response
CORPORATE_EQUITY_STAKE_DIVIDENDS = 40e9
FEDERAL_ASSET_REVENUES = 50e9  # Mineral rights, spectrum, land
REDIRECTED_EXISTING_TRANSFERS = 100e9  # Portion of existing welfare spend

# === SOCIAL SECURITY & SAFETY NET ===
SS_TOTAL_BENEFICIARIES = 67_000_000
SS_TOTAL_ANNUAL_OUTLAYS = 1_400e9      # $1.4T/year OASDI
SS_TOTAL_ANNUAL_REVENUE = 1_200e9      # Payroll tax + benefit taxation
SS_ANNUAL_DEFICIT = 200e9              # Current annual shortfall
SS_TRUST_FUND_BALANCE = 2_700e9        # Combined OASI+DI (declining)
SS_PROJECTED_DEPLETION_YEAR = 2034     # CBO central estimate
SS_POST_DEPLETION_BENEFIT_PCT = 0.77   # Payable from ongoing revenue after depletion
SS_AVG_RETIRED_BENEFIT_MONTHLY = 1_907 # Average retired worker benefit
SS_PAYROLL_TAX_RATE = 0.124            # 12.4% combined employer+employee

# Working-age population (not yet SS-eligible)
US_WORKING_AGE_ADULTS = US_POPULATION - 72_000_000 - SS_TOTAL_BENEFICIARIES  # ~191M adults 18-66

# Non-SS safety net (annual, approximate)
MEDICARE_ANNUAL = 900e9
MEDICAID_ANNUAL = 600e9
SNAP_ANNUAL = 110e9
SSI_ANNUAL = 60e9
EITC_ANNUAL = 60e9
HOUSING_ANNUAL = 55e9
TANF_ANNUAL = 16e9
UNEMPLOYMENT_ANNUAL = 30e9
TOTAL_SAFETY_NET = (SS_TOTAL_ANNUAL_OUTLAYS + MEDICARE_ANNUAL + MEDICAID_ANNUAL +
                    SNAP_ANNUAL + SSI_ANNUAL + EITC_ANNUAL + HOUSING_ANNUAL +
                    TANF_ANNUAL + UNEMPLOYMENT_ANNUAL)  # ~$3.23T

# === GENERAL EQUILIBRIUM EFFECTS ===
# Price impact of sovereign fund buying
PRICE_IMPACT_COEFFICIENT = 0.5  # Kyle's lambda, scaled
EXPECTED_PE_EXPANSION_PCT = 0.10  # 10% PE expansion from $10T demand shock

# Equity premium compression
ERP_COMPRESSION_PER_TRILLION = 0.002  # 20bps ERP reduction per $1T fund

# === MACRO PARAMETERS ===
GDP_US = 28e12  # $28T
GDP_GROWTH_REAL = 0.02  # 2% real
INFLATION_TARGET = 0.02  # 2%
FEDERAL_BUDGET = 6.5e12
FEDERAL_REVENUE = 4.8e12
DEBT_TO_GDP = 1.24  # 124%

# === SIMULATION PARAMETERS ===
MC_NUM_PATHS = 10_000
MC_TIME_HORIZON_YEARS = 50
RANDOM_SEED = 42
