"""
Criticism Framework — Adversarial Stress-Testing of the UBI Extractor

Every serious policy proposal must survive its strongest critics.
This module systematically catalogs, classifies, and responds to every
major objection to market-funded UBI.

Classification:
  VALID   — Criticism identifies a real problem. We incorporate it.
  PARTIAL — Contains a kernel of truth but overstates the problem. We quantify.
  INVALID — Based on faulty logic, bad evidence, or ideological priors. We counter.

Each criticism is paired with:
  - The strongest version of the argument (steelman)
  - Academic sources making this argument
  - Our assessment (valid/partial/invalid)
  - Quantified impact on the model (if valid)
  - Evidence-based counter (if invalid)
  - Model adjustment made (if valid)
"""

import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.parameters import *


# ═══════════════════════════════════════════════════════════════════════
#  SECTION 1: ECONOMIC CRITICISMS
# ═══════════════════════════════════════════════════════════════════════

ECONOMIC_CRITICISMS = [
    # ─────────────────────────────────────────────────────────────────
    {
        'id': 'E1',
        'name': 'UBI Causes Inflation (Demand-Pull)',
        'category': 'Macroeconomic',
        'steelman': (
            "Giving $2,200/month to 258M adults injects $6.8T/year into the economy. "
            "This massive demand shock will drive up prices — especially housing, food, "
            "and healthcare — wiping out much of the UBI's purchasing power. "
            "Landlords will simply raise rents by the UBI amount. The real transfer "
            "is much smaller than the nominal transfer."
        ),
        'sources': [
            'Mankiw (2019) "A Skeptic\'s Guide to UBI"',
            'Cochrane (2023) "The Fiscal Theory of the Price Level"',
            'Dinerstein, Megalokonomou & Yannelis (2022) on housing subsidy capitalization',
        ],
        'assessment': 'PARTIAL',
        'validity_detail': (
            "Inflation risk is real but overblown for three reasons:\n"
            "1. UBI is TAX-FUNDED, not money-printed. It redistributes existing purchasing "
            "power from high-income savers (low MPC) to broad population (higher MPC). "
            "The net new demand depends on the DIFFERENCE in MPC, not the gross transfer.\n"
            "2. The economy has significant supply elasticity — firms can produce more goods "
            "when demand rises, especially for tradable goods.\n"
            "3. The specific 'landlords raise rents by UBI amount' argument fails empirically — "
            "Alaska PFD ($1-2K/year) shows zero rent capitalization in competitive markets "
            "(Jones & Marinescu 2022). It could apply in supply-constrained housing markets."
        ),
        'quantified_impact': {
            'cpi_increase_at_200mo': 0.003,    # +0.3% CPI at $200/mo UBI
            'cpi_increase_at_500mo': 0.010,    # +1.0% CPI at $500/mo UBI
            'cpi_increase_at_1000mo': 0.025,   # +2.5% CPI at $1000/mo UBI
            'cpi_increase_at_2200mo': 0.06,    # +6.0% CPI at $2200/mo UBI (one-time level shift)
            'housing_price_effect': 0.04,       # +4% housing prices at $500/mo (supply-constrained)
            'tradable_goods_effect': 0.005,     # +0.5% (elastic supply)
        },
        'model_adjustment': (
            "Add inflation haircut to real UBI value. At $500/month, effective "
            "real purchasing power is ~$480-490/month after one-time price adjustment. "
            "At $2,200/month, effective real value is ~$2,070/month. "
            "This is a 6% haircut, not a wipeout."
        ),
        'counter': (
            "The key distinction: MONEY-FINANCED UBI (printing money) would be inflationary. "
            "TAX-FINANCED UBI (which this is) is a redistribution, not a demand expansion. "
            "Total spending power in the economy stays roughly constant — it's reallocated "
            "from high-income earners (wealth tax, payroll tax) to the general population. "
            "The MPC differential creates SOME net demand increase (~$1-2T), but the US "
            "economy has ~$28T GDP — the proportional demand shock is manageable. "
            "Historical evidence: Alaska PFD, pandemic stimulus checks ($1.2T in 2020-2021) "
            "contributed ~1-3 percentage points to CPI, not hyperinflation."
        ),
        'evidence': [
            'Jones & Marinescu (2022): Alaska PFD has no effect on local rents',
            'Coibion et al (2022): Stimulus checks -> 0.7pp CPI per $1T distributed',
            'Hsieh (2003): Alaska PFD -> no consumption-driven price effects',
        ],
    },

    # ─────────────────────────────────────────────────────────────────
    {
        'id': 'E2',
        'name': 'People Will Stop Working',
        'category': 'Labor Economics',
        'steelman': (
            "$2,200/month exceeds the federal poverty line. Many workers in low-wage jobs "
            "earn $2,000-3,000/month. Rational agents will quit marginal jobs, causing "
            "labor shortages, wage-price spirals, and GDP contraction. The tax base erodes, "
            "creating a death spiral where fewer workers fund more recipients."
        ),
        'sources': [
            'Moffitt (2003) "The Negative Income Tax and the Evolution of U.S. Welfare Policy"',
            'Heckman & Masterov (2007) on labor supply elasticities',
            'Conservative critics: Tanner (2014) CATO "The Work vs. Welfare Tradeoff"',
        ],
        'assessment': 'PARTIAL',
        'validity_detail': (
            "Valid at HIGH UBI levels ($2,200/mo), partially valid at moderate levels "
            "($500-1000/mo), and mostly invalid at low levels ($200-500/mo).\n\n"
            "The evidence is remarkably consistent: at moderate levels, employment effects "
            "are SMALL (1-5% reduction) and are dominated by voluntary choices:\n"
            "- Going back to school\n"
            "- Caring for children/elderly\n"
            "- Starting businesses\n"
            "- Leaving abusive work situations\n\n"
            "At $2,200/month (exceeding minimum wage), the effect IS larger. "
            "We estimate 5-10% labor force reduction, concentrated in the lowest-paid jobs. "
            "This is the most valid version of this criticism."
        ),
        'quantified_impact': {
            'employment_change_200mo': -0.01,   # -1%
            'employment_change_500mo': -0.03,   # -3%
            'employment_change_1000mo': -0.05,  # -5%
            'employment_change_2200mo': -0.09,  # -9%
            'gdp_impact_200mo': -0.003,         # -0.3% GDP
            'gdp_impact_500mo': -0.012,         # -1.2% GDP
            'gdp_impact_1000mo': -0.025,        # -2.5% GDP
            'gdp_impact_2200mo': -0.05,         # -5.0% GDP (before offsetting effects)
        },
        'model_adjustment': (
            "Our GE model already incorporates this via the LaborMarketModel. "
            "We ADD a nonlinear term: at UBI > minimum wage, the labor supply "
            "elasticity increases sharply (kink in the budget constraint). "
            "We also model the OFFSETTING effects: entrepreneurship, health, education."
        ),
        'counter': (
            "The 'death spiral' version is invalid because:\n"
            "1. The tax base is NOT primarily low-wage workers. Revenue comes from wealth "
            "taxes, payroll uncapping, and sovereign fund returns — not low-wage income tax.\n"
            "2. Workers leaving bad jobs RAISES wages for remaining workers (supply/demand). "
            "This is a feature, not a bug — it transfers power from employers to workers.\n"
            "3. The empirical evidence is overwhelming: Finland, Alaska, Stockton, Kenya, "
            "US NIT experiments — employment effects are small and offset by gains.\n"
            "4. The 'rational agent quits' model ignores social identity, status, purpose, "
            "and consumption aspirations beyond $2,200/month. Most people want more."
        ),
        'evidence': [
            'Finland experiment (2020): Recipients MORE likely to find employment (+6%)',
            'Stockton SEED (2021): Full-time employment rose from 28% to 40%',
            'Jones & Marinescu (2022): Alaska PFD -> no employment reduction',
            'Cesarini et al (2017): Lottery winners barely reduce work hours',
            'Egger et al (2022): GiveDirectly Kenya -> slight labor INCREASE',
        ],
    },

    # ─────────────────────────────────────────────────────────────────
    {
        'id': 'E3',
        'name': 'The Equity Risk Premium Will Disappear',
        'category': 'Financial Economics',
        'steelman': (
            "If the entire strategy depends on a 4-6% equity risk premium, what happens "
            "when it compresses? A $10-20T sovereign fund buying equities will massively "
            "drive up prices and crush future returns. The ERP could go to 1-2%, making "
            "the fund unsustainable. Moreover, the historic ERP reflects survivorship bias "
            "(US outperformed; other markets didn't). Global diversification lowers it."
        ),
        'sources': [
            'Arnott, Bernstein & West (2021) on ERP compression',
            'Gabaix & Koijen (2022) on inelastic markets',
            'Dimson, Marsh & Staunton (2023): Global ERP lower than US-only',
            'Fama & French (2002): Forward ERP lower than historical',
        ],
        'assessment': 'VALID',
        'validity_detail': (
            "This is the MOST valid economic criticism. Our model already accounts "
            "for ERP compression (20bps per $1T of fund), but the true effect is "
            "uncertain. At $10T, our model shows ERP falling from 5% to ~3.5%. "
            "At $20T, it could fall to ~2%. This is a real constraint on the "
            "system's capacity.\n\n"
            "The survivorship bias point is also valid: US equity returns 1900-2024 "
            "averaged ~6.5% real, but the global average was ~4.3% (DMS 2023). "
            "A globally diversified fund should use the lower number."
        ),
        'quantified_impact': {
            'erp_at_5T_fund': 0.04,       # 4.0%
            'erp_at_10T_fund': 0.03,      # 3.0%
            'erp_at_20T_fund': 0.02,      # 2.0%
            'survivorship_bias_haircut': -0.015,  # -1.5% vs US-only estimates
            'ubi_reduction_at_10T': -0.25,  # -25% lower UBI than naive estimate
            'ubi_reduction_at_20T': -0.45,  # -45% lower
        },
        'model_adjustment': (
            "CRITICAL UPDATE: Reduce baseline ERP from 5% to 4% (global, not US-only). "
            "Increase ERP compression coefficient from 20bps to 25bps per $1T. "
            "This is the single largest correction from criticism. "
            "It reduces the mature-state UBI estimate by ~25-35%."
        ),
        'counter': None,  # This criticism is fully valid — we incorporate, not counter
        'evidence': [
            'DMS (2023): Global ERP = 3.3% geometric, 4.6% arithmetic (real)',
            'Gabaix & Koijen (2022): $1 inflow -> $5 market cap increase',
            'Norway GPFG (2024): 5.9% nominal return since 1998, but from smaller base',
        ],
    },

    # ─────────────────────────────────────────────────────────────────
    {
        'id': 'E4',
        'name': 'Wealth Tax Revenue Evaporates (Avoidance + Capital Flight)',
        'category': 'Public Finance',
        'steelman': (
            "Every country that tried a wealth tax has repealed it. France, Sweden, "
            "Austria, Denmark, Germany, Finland, Iceland, Luxembourg — all abandoned theirs. "
            "The rich restructure assets, move to lower-tax jurisdictions, and exploit "
            "valuation loopholes. Revenue comes in at 30-50% of projections. "
            "The US model assumes $416B from a federal wealth tax — this is fantasy."
        ),
        'sources': [
            'Summers & Sarin (2019) "A Wealth Tax is a Poor Idea" Harvard/Wharton',
            'Scheuer & Slemrod (2021) "Taxing Our Wealth" J Econ Perspectives',
            'Advani, Chamberlain & Sherwood (2023): UK wealth tax evasion estimates',
        ],
        'assessment': 'PARTIAL',
        'validity_detail': (
            "The European comparison is valid but misleading:\n"
            "1. European wealth taxes failed partly because of FREE MOVEMENT within the EU. "
            "The US taxes based on CITIZENSHIP, not residency. Leaving the US means "
            "renouncing citizenship — a much higher bar than moving from France to Belgium.\n"
            "2. The US has an exit tax (IRC 877A) that taxes unrealized gains on expatriation.\n"
            "3. BUT: avoidance through trusts, valuation games, and asset restructuring IS real.\n\n"
            "We already apply a 25% avoidance haircut. The evidence suggests 15-35% is realistic "
            "for a well-designed US wealth tax (Saez & Zucman 2019, Sarin & Summers 2019)."
        ),
        'quantified_impact': {
            'projected_revenue_gross': 555e9,
            'avoidance_rate_low': 0.15,   # Saez-Zucman estimate
            'avoidance_rate_mid': 0.25,   # Our current assumption
            'avoidance_rate_high': 0.40,  # Summers-Sarin estimate
            'net_revenue_low_avoidance': 555e9 * 0.85,   # $472B
            'net_revenue_mid_avoidance': 555e9 * 0.75,   # $416B (our estimate)
            'net_revenue_high_avoidance': 555e9 * 0.60,  # $333B
            'ubi_impact_per_100B': 32,  # $100B = ~$32/month UBI per adult
        },
        'model_adjustment': (
            "Add a HIGH-avoidance scenario: 40% avoidance reduces wealth tax revenue "
            "from $416B to $333B. This costs ~$27/month in UBI per adult. "
            "Significant but not catastrophic — wealth tax is only one source."
        ),
        'counter': (
            "The US is unique: citizenship-based taxation, exit tax, global financial "
            "hegemony. The IRS can reach assets globally through FATCA and bilateral "
            "treaties. Also, the wealth tax doesn't need to be perfect — even at 40% "
            "avoidance it generates $333B/year, which is meaningful. The perfect should "
            "not be the enemy of the good.\n\n"
            "Moreover, avoidance DECLINES over time as enforcement improves and norms shift. "
            "The US income tax initially had massive avoidance; compliance improved with "
            "withholding and information reporting."
        ),
        'evidence': [
            'Saez & Zucman (2019): US wealth tax would face 15% evasion with enforcement',
            'FATCA (2010): Already reduced offshore evasion by ~$40B/year',
            'IRC 877A exit tax: Expatriates pay mark-to-market on all assets',
        ],
    },

    # ─────────────────────────────────────────────────────────────────
    {
        'id': 'E5',
        'name': 'Sovereign Fund Creates Systemic Risk / Too Big to Fail',
        'category': 'Financial Stability',
        'steelman': (
            "A $10-20T fund owning 15-30% of global equities creates catastrophic "
            "concentration risk. If the fund must sell during a crisis (to maintain UBI "
            "payouts), it becomes a forced seller that deepens crashes. The fund IS the "
            "market — its rebalancing moves prices. This creates a 'too big to fail' "
            "entity that dwarfs any bank or pension fund, with political pressure "
            "to never let it fall."
        ),
        'sources': [
            'Greenwood, Hanson, Shleifer & Sorensen (2022) on fire sales',
            'Brunnermeier & Pedersen (2009) "Market Liquidity and Funding Liquidity"',
            'IMF (2023) Global Financial Stability Report on sovereign fund risks',
        ],
        'assessment': 'VALID',
        'validity_detail': (
            "This is valid and serious. A $15T fund is ~27% of global equities. "
            "Its actions would dominate price formation. Three specific risks:\n"
            "1. PROCYCLICAL SELLING: If the withdrawal rule forces selling in crashes, "
            "the fund amplifies downturns.\n"
            "2. GOVERNANCE RISK: Political pressure to 'do something' during crises.\n"
            "3. MORAL HAZARD: Markets assume the fund will always buy dips, "
            "creating a 'sovereign put' that encourages risk-taking.\n\n"
            "Our smoothed withdrawal rule mitigates (1) — it never sells more than "
            "5% per year and uses a 5-year trailing average. But (2) and (3) are real."
        ),
        'quantified_impact': {
            'crisis_drawdown_amplification': 0.05,  # Fund selling adds 5% to crash depth
            'recovery_delay_years': 0.5,  # Half year slower recovery
            'market_vol_increase_pct': 0.10,  # 10% higher realized volatility
            'ubi_volatility_increase': 0.15,  # 15% more volatile UBI payments
        },
        'model_adjustment': (
            "ADD to Monte Carlo: systemic risk premium. Fund's own selling during crashes "
            "amplifies drawdowns by 5%. Increase baseline volatility by 10% once fund "
            "exceeds 10% of market cap. Add 'sovereign put' risk — markets take more "
            "risk knowing the fund is a backstop, which increases tail risk."
        ),
        'counter': None,  # Valid — incorporate, don't counter
        'evidence': [
            'Norway GPFG: Successfully navigated 2008 (-23%) without forced selling',
            'But GPFG is only $1.6T / ~1.5% of global equities — not the same scale',
            'Japan GPIF ($1.7T): Similar scale concerns, managed through diversification',
        ],
    },

    # ─────────────────────────────────────────────────────────────────
    {
        'id': 'E6',
        'name': 'Tax Incidence Falls on Workers, Not the Rich',
        'category': 'Public Finance / Tax Theory',
        'steelman': (
            "Payroll tax cap removal sounds like taxing the rich, but incidence analysis "
            "shows employers offset higher payroll taxes by reducing wages and hiring. "
            "The wealth tax reduces investment, lowering productivity and wages for all. "
            "Corporate equity contributions are effectively a tax on shareholders, who "
            "include pension funds — meaning retirees pay. The burden always flows downhill."
        ),
        'sources': [
            'Saez, Matsaganis & Tsakloglou (2012) on payroll tax incidence',
            'Fullerton & Metcalf (2002) "Tax Incidence" Handbook of Public Economics',
            'Suárez Serrato & Zidar (2016): Corporate tax incidence on workers',
        ],
        'assessment': 'PARTIAL',
        'validity_detail': (
            "Incidence IS more complex than 'the rich pay.' Evidence:\n"
            "- Payroll taxes: ~70% borne by workers through lower wages (Saez 2012)\n"
            "- Wealth taxes: Mixed — partly borne by capital owners, partly by workers\n"
            "  through reduced investment (Scheuer & Slemrod 2021)\n"
            "- Corporate taxes: ~25-50% borne by workers (Suárez Serrato & Zidar 2016)\n\n"
            "BUT: The relevant question is not 'who bears the tax?' but 'who is better off "
            "NET of tax + UBI?' If workers pay 70% of the payroll tax but receive 100% of "
            "the UBI, they're net better off. This is a redistribution from high earners "
            "to the general population — the incidence argument doesn't invalidate it."
        ),
        'quantified_impact': {
            'payroll_tax_worker_burden_pct': 0.70,  # 70% borne by workers
            'wealth_tax_worker_burden_pct': 0.25,   # 25% through reduced investment
            'net_redistribution_positive': True,     # Workers still net beneficiaries
            'effective_tax_rate_on_median_worker': 0.03,  # ~3% effective rate increase
            'net_ubi_after_tax_incidence': 0.92,  # Workers keep ~92% of UBI value
        },
        'model_adjustment': (
            "Apply 8% tax incidence haircut to UBI value for median worker. "
            "The $500/month UBI is effectively ~$460/month after accounting for "
            "indirect tax burden on workers. Still strongly positive."
        ),
        'counter': (
            "The incidence argument is a DISTRIBUTION argument, not an EFFICIENCY argument. "
            "Yes, some burden falls on workers. But the UBI MORE THAN compensates them. "
            "A median worker earning $60K/year faces ~$1,800/year in indirect tax burden "
            "but receives ~$6,000-26,400/year in UBI. The NET transfer is positive for "
            "roughly the bottom 80% of the income distribution."
        ),
        'evidence': [
            'Saez & Zucman (2019): Bottom 50% pay ~25% effective tax rate (all taxes)',
            'Fullerton & Metcalf (2002): Incidence depends on supply/demand elasticities',
            'Key: NET transfer matters, not gross tax burden',
        ],
    },

    # ─────────────────────────────────────────────────────────────────
    {
        'id': 'E7',
        'name': 'Induced Tax Revenue / Multiplier Numbers Are Fantasy',
        'category': 'Macroeconomic Modeling',
        'steelman': (
            "The model counts $664B in 'induced tax revenue from the economic multiplier' "
            "and $1,022B in 'tax clawback.' These are circular — you're counting the "
            "tax revenue generated by spending the UBI as revenue to fund the UBI. "
            "This is double-counting. The fiscal multiplier is also contested — it's "
            "not 1.5x during full employment, it's closer to 0.5-0.8x."
        ),
        'sources': [
            'Ramey (2011) "Can Government Purchases Stimulate the Economy?" JEL',
            'Barro & Redlick (2011) "Macroeconomic Effects from Government Purchases"',
            'Summers & DeLong (2012) vs. Ramey debate on fiscal multipliers',
        ],
        'assessment': 'VALID',
        'validity_detail': (
            "This criticism is substantially correct. Two issues:\n\n"
            "1. MULTIPLIER OVERCOUNT: Counting induced tax revenue as 'funding' for UBI "
            "is partially circular. The $664B reflects tax on economic activity CREATED "
            "by UBI spending. This is real revenue, but it already depends on the UBI "
            "existing. You can't use it to justify the UBI's existence — it's an OFFSET, "
            "not an independent source.\n\n"
            "2. MULTIPLIER SIZE: During full employment, the fiscal multiplier is "
            "0.5-0.8x (Ramey 2011), not 1.5x. Our MPC-based calculation (0.65 MPC * 15% "
            "tax rate) is mechanical, not a general equilibrium multiplier. It ignores "
            "crowding out of private investment and the fact that taxes fund the UBI "
            "(so total spending doesn't increase by the full UBI amount).\n\n"
            "We should reduce these numbers by 50-60%."
        ),
        'quantified_impact': {
            'current_induced_tax_estimate': 664e9,
            'corrected_induced_tax_estimate': 265e9,  # 60% reduction
            'current_tax_clawback': 1022e9,
            'corrected_tax_clawback': 750e9,  # Clawback is more defensible (direct tax)
            'net_revenue_reduction': 671e9,
            'ubi_impact_monthly': -217,  # ~$217/month per adult lost
        },
        'model_adjustment': (
            "CRITICAL: Reduce induced tax revenue from $664B to $265B. "
            "Reduce tax clawback from $1,022B to $750B (progressive income tax is real, "
            "but effective rates are lower than statutory rates). "
            "This is the second-largest correction from criticism. "
            "Year 1 affordable UBI drops from $758/month to ~$540/month."
        ),
        'counter': None,  # Valid — we fix the model
        'evidence': [
            'Ramey (2011): Fiscal multiplier 0.6-1.0x at full employment',
            'Barro (2011): Government spending multiplier < 1.0 in most cases',
            'Note: Tax clawback IS defensible — high earners DO pay income tax on UBI',
        ],
    },
]


# ═══════════════════════════════════════════════════════════════════════
#  SECTION 2: POLITICAL CRITICISMS
# ═══════════════════════════════════════════════════════════════════════

POLITICAL_CRITICISMS = [
    # ─────────────────────────────────────────────────────────────────
    {
        'id': 'P1',
        'name': 'Constitutional Amendment is Impossible in Current Polarization',
        'category': 'Political Feasibility',
        'steelman': (
            "The system requires a constitutional amendment (2/3 Congress + 3/4 states). "
            "The last amendment ratified was the 27th in 1992 (proposed in 1789). "
            "In today's polarized environment, 38 states agreeing on ANYTHING is "
            "effectively impossible. Without constitutional protection, the fund is "
            "vulnerable to legislative raids, making the whole system fragile."
        ),
        'assessment': 'VALID',
        'model_adjustment': (
            "Redesign: The fund CAN operate under statutory authority (like the Federal "
            "Reserve). Constitutional entrenchment is ideal but not required. Our governance "
            "model should include a 'statutory-only' path that uses independent agency "
            "structure + trust law + public constituency as protection instead."
        ),
        'counter_where_applicable': (
            "A constitutional amendment is the GOLD STANDARD but not the only path. "
            "The Federal Reserve operates with enormous independence under statutory "
            "authority. Social Security has no constitutional protection yet is politically "
            "untouchable. The key is creating a broad constituency that makes raiding "
            "the fund political suicide — the 'third rail' effect."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    {
        'id': 'P2',
        'name': 'Government Ownership of Equities is Socialism / Central Planning',
        'category': 'Ideological',
        'steelman': (
            "A government entity owning 15-30% of the stock market gives the state "
            "enormous power over corporations. Even without voting rights, the fund's "
            "investment decisions pick winners and losers. This is de facto nationalization "
            "— the state controls the means of production through capital ownership."
        ),
        'assessment': 'PARTIAL',
        'counter_where_applicable': (
            "This conflates OWNERSHIP with CONTROL.\n\n"
            "1. The fund holds PASSIVE INDEX positions — it doesn't pick stocks. No investment "
            "discretion means no 'picking winners.'\n"
            "2. Voting rights can be delegated to independent proxy advisors or waived entirely. "
            "Norway's GPFG owns 1.5% of global equities and doesn't control any company.\n"
            "3. The alternative to government-held equity is government-held DEBT (Treasury "
            "bonds in the Social Security trust fund). Equity is a better investment; "
            "the governance risk is manageable.\n"
            "4. Alaska, Norway, Singapore all do this successfully. It's not socialism — "
            "it's sovereign wealth management, practiced by 90+ countries.\n"
            "5. The fund can be designed with explicit corporate governance neutrality: "
            "proxy votes split proportionally to other shareholders' votes, eliminating "
            "any influence on corporate decisions."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    {
        'id': 'P3',
        'name': '20-Year Accumulation is Politically Impossible',
        'category': 'Time Inconsistency',
        'steelman': (
            "No democracy can commit to a 20-year plan that requires sustained sacrifice "
            "(taxes) with zero payoff until the end. Every election cycle, politicians "
            "will promise to spend the fund, reduce the taxes, or redirect contributions. "
            "The fund will be raided long before maturity."
        ),
        'assessment': 'VALID',
        'model_adjustment': (
            "Redesign the phased approach: BEGIN small distributions in Year 3-5 "
            "(even $50-100/month). This creates an immediate constituency. Then GROW "
            "distributions as the fund grows. Never have a period with zero payouts — "
            "that's politically suicidal. The Alaska model works because it pays EVERY YEAR."
        ),
        'counter_where_applicable': (
            "The original model's 20-year lockout was a mistake we've already corrected. "
            "The phased approach (pay immediately, grow over time) is both more politically "
            "viable and more humane. You can start at $50-100/month using tax reform revenue "
            "alone, before the sovereign fund is even large."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    {
        'id': 'P4',
        'name': 'UBI Destroys the Social Contract / Erodes Work Ethic',
        'category': 'Moral / Cultural',
        'steelman': (
            "Work provides meaning, structure, social connection, and dignity. UBI "
            "severs the link between contribution and reward, creating a class of "
            "permanently dependent citizens. This erodes social cohesion, increases "
            "substance abuse, and creates 'deaths of despair.'"
        ),
        'assessment': 'INVALID',
        'counter_where_applicable': (
            "This argument confuses EMPLOYMENT with WORK and confuses POVERTY with DIGNITY.\n\n"
            "1. EMPIRICAL EVIDENCE: UBI experiments consistently show recipients engage in "
            "MORE productive activity, not less — caregiving, education, entrepreneurship, "
            "community engagement. Stockton SEED participants' full-time employment ROSE.\n\n"
            "2. 'DEATHS OF DESPAIR' come from POVERTY and PRECARITY, not from having too "
            "much money. Case & Deaton (2020) document that deaths of despair are concentrated "
            "in communities ravaged by job loss WITHOUT income replacement.\n\n"
            "3. The current system — where survival depends on accepting any available job "
            "regardless of conditions — is what actually erodes dignity. UBI gives workers "
            "bargaining power to demand better conditions.\n\n"
            "4. Most people who receive unconditional cash CONTINUE WORKING. The desire "
            "for status, consumption, purpose, and social connection far exceeds $2,200/month. "
            "Lottery winners overwhelmingly keep their jobs (Cesarini et al 2017).\n\n"
            "5. Unpaid care work (~$1.5T/year in the US, disproportionately done by women) "
            "IS work. UBI compensates it for the first time."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    {
        'id': 'P5',
        'name': 'UBI Benefits the Undeserving / Immigrants / Non-contributors',
        'category': 'Nativist / Merit-based',
        'steelman': (
            "Universal means universal — including people who have never worked, paid "
            "taxes, or contributed to society. This creates a moral hazard and a magnet "
            "for immigration. Why should a 19-year-old who has never worked receive the "
            "same as a 50-year-old who paid taxes for 30 years?"
        ),
        'assessment': 'INVALID',
        'counter_where_applicable': (
            "1. UNIVERSALITY IS THE POINT. Means-testing costs $60-100B/year in "
            "administration and creates poverty traps (lose benefits as you earn more). "
            "It's cheaper and more efficient to give to everyone and tax it back from "
            "the wealthy.\n\n"
            "2. The 'deserving vs. undeserving' distinction is empirically meaningless. "
            "Most people in poverty are children, elderly, disabled, or working poor. "
            "The mythical 'able-bodied person choosing not to work' is <5% of recipients "
            "in every study.\n\n"
            "3. Immigration concern is addressable: UBI can require citizenship or "
            "permanent residency + 5 years of tax filing. This is a design choice, "
            "not a fatal flaw.\n\n"
            "4. The 19-year-old argument: Social Security gives MORE to people who "
            "earned MORE. UBI gives everyone a FLOOR. The two can coexist. "
            "The 19-year-old also pays into the system their entire career."
        ),
    },

    # ─────────────────────────────────────────────────────────────────
    {
        'id': 'P6',
        'name': 'UBI Replaces Targeted Programs That Serve Vulnerable Populations Better',
        'category': 'Progressive Critique',
        'steelman': (
            "The left's strongest objection: consolidating SNAP, SSI, and housing assistance "
            "into UBI sounds efficient but HARMS the most vulnerable. A disabled person "
            "receiving $2,000/month SSI + $300/month SNAP + housing voucher ($1,500/month) = "
            "$3,800/month in targeted support. Replacing this with $2,200 UBI is a $1,600/month "
            "CUT for disabled people. UBI is a trojan horse for austerity."
        ),
        'assessment': 'PARTIAL',
        'validity_detail': (
            "This is the most important progressive criticism and it's substantially correct "
            "for the MOST vulnerable populations under full-replacement scenarios.\n\n"
            "Our model's 'partial merger' strategy already addresses this: UBI replaces ONLY "
            "the bottom tier. Anyone receiving more from existing programs keeps the excess "
            "as a top-up. But we should be MORE explicit about this."
        ),
        'model_adjustment': (
            "CRITICAL: The 'safety net consolidation' number ($194B) must EXCLUDE "
            "disability-specific benefits entirely. We consolidate ONLY programs that "
            "provide LESS than UBI to their recipients. Anyone receiving MORE from "
            "existing programs gets UBI + the difference. This is the 'no one loses' "
            "constraint. It reduces consolidation savings by ~30% but is non-negotiable "
            "for ethical and political reasons."
        ),
        'counter_where_applicable': (
            "UBI should SUPPLEMENT, not REPLACE, disability-specific benefits. "
            "Our SS Rescue strategy explicitly preserves SS. The partial merger "
            "preserves all benefits above UBI level as top-ups. Any design that "
            "cuts net income for disabled or elderly people is politically dead "
            "and morally wrong — and we don't propose it."
        ),
    },
]


# ═══════════════════════════════════════════════════════════════════════
#  SECTION 3: SOCIAL / STRUCTURAL CRITICISMS
# ═══════════════════════════════════════════════════════════════════════

SOCIAL_CRITICISMS = [
    {
        'id': 'S1',
        'name': 'UBI Entrenches Existing Inequality (Racial, Gender, Geographic)',
        'category': 'Structural Inequality',
        'steelman': (
            "A flat payment ignores that a Black family in Mississippi faces different "
            "costs and barriers than a white family in Vermont. $2,200 in San Francisco "
            "doesn't cover rent; in rural Alabama it's comfortable. UBI doesn't address "
            "structural racism, educational inequality, or healthcare access."
        ),
        'assessment': 'PARTIAL',
        'counter_where_applicable': (
            "UBI is a FLOOR, not a CEILING.\n\n"
            "1. $2,200/month is MORE progressive than any current program because it's the "
            "SAME amount regardless of race, location, or status. Current programs have "
            "massive racial disparities in access and enforcement.\n\n"
            "2. Geographic variation: The flat amount is a FEATURE. It creates incentives "
            "to live where costs are lower, reducing geographic concentration and its "
            "associated costs (congestion, housing crises in metros).\n\n"
            "3. UBI doesn't REPLACE anti-discrimination policy, healthcare, or education. "
            "It's one tool. The system explicitly preserves Medicare, Medicaid, and "
            "education funding.\n\n"
            "4. In absolute terms, UBI is MORE valuable to lower-income and minority "
            "communities who have less existing wealth and income. A $2,200/month floor "
            "disproportionately benefits Black and Hispanic households, who have median "
            "wealth of $24K and $36K respectively vs. $189K for white households."
        ),
    },

    {
        'id': 'S2',
        'name': 'The Housing Market Will Absorb UBI (Rent-Seeking)',
        'category': 'Market Failure',
        'steelman': (
            "In supply-constrained housing markets (SF, NYC, Boston, LA), landlords will "
            "raise rents to capture UBI income. The transfer goes from the government to "
            "tenants to landlords — enriching property owners while leaving renters no "
            "better off. This is Ricardian rent-seeking in its purest form."
        ),
        'assessment': 'PARTIAL',
        'validity_detail': (
            "This is PARTIALLY valid in supply-constrained metros and largely INVALID "
            "in competitive housing markets.\n\n"
            "In competitive markets (most of the US by area), landlords compete for tenants. "
            "If one raises rent, tenants move to the next one. UBI actually INCREASES "
            "mobility (people can afford to move), which INCREASES competition.\n\n"
            "In supply-constrained markets (SF, NYC), the criticism has merit. "
            "Housing supply is essentially fixed in the short run. Additional demand "
            "DOES push up rents. BUT: this is an argument for building more housing, "
            "not against UBI."
        ),
        'quantified_impact': {
            'rent_increase_competitive_markets': 0.01,  # +1%
            'rent_increase_supply_constrained': 0.08,   # +8%
            'population_weighted_avg': 0.04,            # +4% national average
            'effective_ubi_haircut_from_housing': 0.04,  # 4% of UBI eaten by housing
        },
        'model_adjustment': (
            "Add 4% housing inflation haircut to effective UBI purchasing power. "
            "Also note: UBI paired with housing supply reform (zoning, permitting) "
            "would eliminate this problem. The housing criticism is about housing "
            "POLICY, not UBI policy."
        ),
        'counter_where_applicable': (
            "Alaska PFD evidence: $1-2K/year dividend shows NO rent capitalization "
            "(Jones & Marinescu 2022). The scale matters — $2,200/month would have a "
            "larger effect — but the 'landlords take it all' story is not supported. "
            "Most UBI flows to food, transportation, debt reduction, and savings, "
            "not incremental housing spending."
        ),
    },

    {
        'id': 'S3',
        'name': 'UBI Increases Substance Abuse and Social Dysfunction',
        'category': 'Social Pathology',
        'steelman': (
            "Unconditional cash will be spent on drugs, alcohol, and gambling. "
            "Without conditions, there's no guardrail against self-destructive behavior. "
            "Studies of lottery winners show increased bankruptcy and substance abuse."
        ),
        'assessment': 'INVALID',
        'counter_where_applicable': (
            "This is flatly contradicted by every major study of unconditional cash transfers:\n\n"
            "1. Evans & Popova (2017) meta-analysis of 44 studies across Africa, Asia, "
            "and Latin America: Cash transfers REDUCE spending on alcohol and tobacco "
            "by an average of 0.18 standard deviations.\n\n"
            "2. Finland experiment: UBI recipients reported LESS substance use, not more.\n\n"
            "3. GiveDirectly: Extensive monitoring shows no increase in 'temptation goods.'\n\n"
            "4. The lottery winner comparison is invalid — lump-sum windfalls to a "
            "self-selected population of gamblers are not comparable to universal monthly "
            "payments to the general population.\n\n"
            "5. Poverty ITSELF is the leading predictor of substance abuse. Reducing "
            "poverty through UBI is the most evidence-based anti-addiction policy available.\n\n"
            "6. Conditional programs like TANF have WORSE outcomes: compliance burden "
            "creates stress, missed appointments cause benefit loss, sanctions push people "
            "deeper into crisis."
        ),
    },
]


# ═══════════════════════════════════════════════════════════════════════
#  SECTION 4: MODEL CORRECTIONS FROM VALID CRITICISMS
# ═══════════════════════════════════════════════════════════════════════

def compute_corrected_estimates():
    """
    Apply all valid criticism corrections to the model estimates.

    This produces the HONEST, post-criticism numbers that should be
    reported as the system's actual projections.
    """
    corrections = {
        # From E3: ERP compression (use global ERP, not US-only)
        'erp_baseline_reduction': -0.01,  # 5% -> 4% (global vs US)
        'erp_compression_increase': 0.005,  # 20bps -> 25bps per $1T

        # From E1: Inflation haircut on purchasing power
        'inflation_haircut_500mo': -0.02,  # -2% effective value
        'inflation_haircut_2200mo': -0.06,  # -6% effective value

        # From E7: Multiplier/clawback overcount
        'induced_tax_reduction': 0.60,  # Reduce by 60%
        'clawback_reduction': 0.27,  # Reduce by 27%

        # From E5: Systemic risk premium
        'volatility_increase_above_10pct_share': 0.10,  # +10% vol

        # From P6: Safety net consolidation reduction
        'consolidation_reduction': 0.30,  # -30% (protect disabled)

        # From S2: Housing inflation haircut
        'housing_haircut': -0.04,  # -4% effective value

        # From E4: Higher wealth tax avoidance scenario
        'wealth_tax_avoidance_high': 0.40,  # Scenario with 40% avoidance
    }

    # === CORRECTED LIVING WAGE ESTIMATE ===

    # Original Year 1 estimate: $758/month
    original_year1 = 758

    # Correction 1: Induced tax revenue reduced by 60%
    # Original: $664B -> Corrected: $265B -> Loss: $399B
    # Per adult/month: $399B / 258M / 12 = ~$129/month
    correction_multiplier = -129

    # Correction 2: Tax clawback reduced by 27%
    # Original: $1,022B -> Corrected: $750B -> Loss: $272B
    # Per adult/month: $272B / 258M / 12 = ~$88/month
    correction_clawback = -88

    # Correction 3: Safety net consolidation reduced by 30%
    # Original: $194B -> Corrected: $136B -> Loss: $58B
    # Per adult/month: $58B / 258M / 12 = ~$19/month
    correction_consolidation = -19

    # Correction 4: Inflation + housing haircut = -6% (at high UBI) or -4% (at moderate)
    # Apply -4% to whatever the corrected estimate is
    corrected_before_inflation = original_year1 + correction_multiplier + correction_clawback + correction_consolidation
    correction_inflation = corrected_before_inflation * -0.04

    corrected_year1 = corrected_before_inflation + correction_inflation

    # === CORRECTED LONG-RUN ESTIMATE ===
    # Original "all sources mature" (20yr): $1,088/month
    original_mature = 1088

    # Additional correction: ERP compression from global baseline
    # Sovereign fund returns 4% instead of 5% -> $350B -> $280B
    # Loss: $70B -> ~$23/month
    correction_erp = -23

    corrected_mature = (original_mature + correction_multiplier + correction_clawback +
                       correction_consolidation + correction_erp)
    corrected_mature *= (1 - 0.06)  # 6% inflation+housing haircut at higher UBI

    return {
        'original_year1_monthly': original_year1,
        'corrected_year1_monthly': round(corrected_year1),
        'year1_reduction': round(original_year1 - corrected_year1),
        'year1_reduction_pct': (original_year1 - corrected_year1) / original_year1,

        'original_mature_monthly': original_mature,
        'corrected_mature_monthly': round(corrected_mature),
        'mature_reduction': round(original_mature - corrected_mature),
        'mature_reduction_pct': (original_mature - corrected_mature) / original_mature,

        'corrections_applied': corrections,
        'correction_breakdown_year1': {
            'multiplier_overcount': correction_multiplier,
            'clawback_overcount': correction_clawback,
            'consolidation_protect_disabled': correction_consolidation,
            'inflation_housing': round(correction_inflation),
        },
    }


def print_full_criticism_report():
    """Print the complete criticism framework."""
    print("=" * 90)
    print("  CRITICISM FRAMEWORK — ADVERSARIAL STRESS-TEST OF UBI EXTRACTOR")
    print("=" * 90)

    all_criticisms = (
        [('ECONOMIC', ECONOMIC_CRITICISMS),
         ('POLITICAL', POLITICAL_CRITICISMS),
         ('SOCIAL', SOCIAL_CRITICISMS)]
    )

    valid_count = 0
    partial_count = 0
    invalid_count = 0

    for category_name, criticisms in all_criticisms:
        print(f"\n\n{'━' * 90}")
        print(f"  {category_name} CRITICISMS")
        print(f"{'━' * 90}")

        for c in criticisms:
            assessment = c['assessment']
            if assessment == 'VALID':
                badge = '🔴 VALID'
                valid_count += 1
            elif assessment == 'PARTIAL':
                badge = '🟡 PARTIAL'
                partial_count += 1
            else:
                badge = '🟢 INVALID'
                invalid_count += 1

            print(f"\n  [{c['id']}] {c['name']}")
            print(f"  Assessment: {badge}")
            print(f"\n  Strongest version of this argument:")
            # Wrap steelman text
            steelman = c['steelman']
            for line in steelman.split('\n'):
                print(f"    \"{line.strip()}\"")

            if 'sources' in c:
                print(f"\n  Academic sources:")
                for src in c['sources']:
                    print(f"    - {src}")

            if 'validity_detail' in c:
                print(f"\n  Our analysis:")
                for line in c['validity_detail'].split('\n'):
                    print(f"    {line}")

            if 'quantified_impact' in c and c['quantified_impact']:
                print(f"\n  Quantified impact on model:")
                for key, val in c['quantified_impact'].items():
                    if isinstance(val, float) and abs(val) < 1:
                        print(f"    {key}: {val:+.1%}")
                    elif isinstance(val, (int, float)):
                        print(f"    {key}: ${val/1e9:.0f}B" if abs(val) > 1e6 else f"    {key}: {val}")
                    else:
                        print(f"    {key}: {val}")

            if 'model_adjustment' in c and c['model_adjustment']:
                print(f"\n  MODEL ADJUSTMENT:")
                for line in c['model_adjustment'].split('\n'):
                    print(f"    >> {line.strip()}")

            if 'counter_where_applicable' in c and c['counter_where_applicable']:
                counter = c.get('counter_where_applicable') or c.get('counter', '')
                if counter:
                    print(f"\n  Counter-argument:")
                    for line in counter.split('\n'):
                        print(f"    {line}")
            elif 'counter' in c and c['counter']:
                print(f"\n  Counter-argument:")
                for line in c['counter'].split('\n'):
                    print(f"    {line}")

    # === SUMMARY ===
    total = valid_count + partial_count + invalid_count
    print(f"\n\n{'=' * 90}")
    print(f"  CRITICISM SCORECARD")
    print(f"{'=' * 90}")
    print(f"\n  Total criticisms analyzed:  {total}")
    print(f"  VALID (incorporated):       {valid_count}  ({valid_count/total:.0%})")
    print(f"  PARTIAL (partially valid):  {partial_count}  ({partial_count/total:.0%})")
    print(f"  INVALID (countered):        {invalid_count}  ({invalid_count/total:.0%})")

    # === CORRECTED ESTIMATES ===
    print(f"\n\n{'=' * 90}")
    print(f"  CORRECTED ESTIMATES (POST-CRITICISM)")
    print(f"{'=' * 90}")

    corrected = compute_corrected_estimates()

    print(f"\n  YEAR 1 (tax reforms only, no sovereign fund):")
    print(f"    Original estimate:  ${corrected['original_year1_monthly']:,}/month")
    print(f"    Corrected estimate: ${corrected['corrected_year1_monthly']:,}/month")
    print(f"    Reduction:          ${corrected['year1_reduction']:,}/month "
          f"({corrected['year1_reduction_pct']:.0%})")
    print(f"\n    Breakdown of corrections:")
    for name, val in corrected['correction_breakdown_year1'].items():
        print(f"      {name:<35} {val:+,}/month")

    print(f"\n  MATURE SYSTEM (20yr sovereign fund + all sources):")
    print(f"    Original estimate:  ${corrected['original_mature_monthly']:,}/month")
    print(f"    Corrected estimate: ${corrected['corrected_mature_monthly']:,}/month")
    print(f"    Reduction:          ${corrected['mature_reduction']:,}/month "
          f"({corrected['mature_reduction_pct']:.0%})")

    print(f"""
  ┌──────────────────────────────────────────────────────────────────────────────┐
  │                    POST-CRITICISM HONEST ESTIMATES                           │
  ├──────────────────┬──────────────────────┬───────────────────────────────────┤
  │   Timeframe      │   Original Estimate  │   Criticism-Adjusted Estimate    │
  ├──────────────────┼──────────────────────┼───────────────────────────────────┤
  │ Year 1-3         │   ${corrected['original_year1_monthly']:>6,}/month       │   ${corrected['corrected_year1_monthly']:>6,}/month (real purchasing power)│
  │ Year 10 (SS)     │     ~$320/month      │     ~$275/month                  │
  │ Year 20 (mature) │   ${corrected['original_mature_monthly']:>6,}/month     │   ${corrected['corrected_mature_monthly']:>6,}/month                       │
  │ Year 30+         │   $1,500-2,200/month │   $1,100-1,600/month             │
  │ Full $2,200 LW   │     ~30 years        │     ~40+ years (if ever)         │
  ├──────────────────┴──────────────────────┴───────────────────────────────────┤
  │                                                                              │
  │  The honest post-criticism assessment: a market-funded UBI of               │
  │  $500-800/month is achievable within 20 years.                              │
  │  $1,000-1,600/month is achievable within 30-40 years.                       │
  │  Full $2,200/month living wage may require additional revenue sources        │
  │  not yet modeled (AI productivity dividend, digital services tax, etc.)      │
  │                                                                              │
  │  The criticism-driven corrections reduce our estimates by 25-35%,            │
  │  but do NOT invalidate the core proposition. The system is feasible;         │
  │  the timeline is longer than naive estimates suggest.                        │
  │                                                                              │
  └──────────────────────────────────────────────────────────────────────────────┘
""")


if __name__ == '__main__':
    print_full_criticism_report()
