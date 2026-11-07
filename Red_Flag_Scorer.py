"""Calculate annual accounting red-flag scores from financials.csv."""

import pandas as pd


INPUT_FILE = "financials.csv"
OUTPUT_FILE = "scores.csv"

FINANCIAL_COLUMNS = [
    "revenue",
    "net_income",
    "operating_cash_flow",
    "total_assets",
    "trade_receivables",
    "inventory",
    "current_debt",
    "long_term_debt",
    "ebitda",
]


def safe_ratio(numerator, denominator):
    """Divide only when the denominator is positive."""
    return numerator / denominator.where(denominator > 0)


def score_higher_is_risk(metric, moderate_limit, strong_limit):
    """Return 0, 1 or 2 points when higher values indicate more risk."""
    points = (metric > moderate_limit).astype(int) + (metric > strong_limit).astype(int)
    return points.where(metric.notna()).astype("Int64")


def score_lower_is_risk(metric, moderate_limit, strong_limit):
    """Return 0, 1 or 2 points when lower values indicate more risk."""
    points = (metric < moderate_limit).astype(int) + (metric < strong_limit).astype(int)
    return points.where(metric.notna()).astype("Int64")


financials = pd.read_csv(INPUT_FILE).dropna(how="all")

# Convert Excel headings such as NET INCOME into net_income.
financials.columns = (
    financials.columns.str.strip()
    .str.lower()
    .str.replace(r"\s+", "_", regex=True)
)
financials = financials.rename(columns={"tckr": "ticker"})

required_columns = {"ticker", "year", *FINANCIAL_COLUMNS}
missing_columns = required_columns.difference(financials.columns)
if missing_columns:
    raise ValueError(f"Missing columns: {', '.join(sorted(missing_columns))}")

financials["ticker"] = financials["ticker"].astype("string").str.strip().str.upper()
financials["year"] = pd.to_numeric(financials["year"], errors="raise").astype(int)

# Remove thousands separators before converting the financial values to numbers.
financials[FINANCIAL_COLUMNS] = (
    financials[FINANCIAL_COLUMNS]
    .replace({",": ""}, regex=True)
    .apply(pd.to_numeric, errors="raise")
)

financials = financials.sort_values(["ticker", "year"]).reset_index(drop=True)

previous_year = financials.groupby("ticker")["year"].shift()
consecutive_year = financials["year"] - previous_year == 1
previous = financials.groupby("ticker")[FINANCIAL_COLUMNS].shift()
previous = previous.where(consecutive_year, axis=0)

financials["cfo_to_ni"] = safe_ratio(
    financials["operating_cash_flow"], financials["net_income"]
)
financials["accrual_ratio"] = safe_ratio(
    financials["net_income"] - financials["operating_cash_flow"],
    (financials["total_assets"] + previous["total_assets"]) / 2,
)
financials["receivables_change"] = safe_ratio(
    financials["trade_receivables"], financials["revenue"]
) - safe_ratio(previous["trade_receivables"], previous["revenue"])
financials["inventory_change"] = safe_ratio(
    financials["inventory"], financials["revenue"]
) - safe_ratio(previous["inventory"], previous["revenue"])
financials["debt_to_ebitda"] = safe_ratio(
    financials["current_debt"] + financials["long_term_debt"],
    financials["ebitda"],
)
revenue_growth = safe_ratio(financials["revenue"], previous["revenue"]) - 1
cfo_growth = safe_ratio(
    financials["operating_cash_flow"], previous["operating_cash_flow"]
) - 1
financials["growth_gap"] = revenue_growth - cfo_growth

financials["cfo_to_ni_score"] = score_lower_is_risk(financials["cfo_to_ni"], 1.0, 0.8)
financials["accrual_ratio_score"] = score_higher_is_risk(financials["accrual_ratio"], 0, 0.05)
financials["receivables_change_score"] = score_higher_is_risk(financials["receivables_change"], 0, 0.02)
financials["inventory_change_score"] = score_higher_is_risk(financials["inventory_change"], 0, 0.03)
financials["debt_to_ebitda_score"] = score_higher_is_risk(financials["debt_to_ebitda"], 2.0, 3.5)
financials["growth_gap_score"] = score_higher_is_risk(financials["growth_gap"], 0, 0.15)

score_columns = [
    "cfo_to_ni_score",
    "accrual_ratio_score",
    "receivables_change_score",
    "inventory_change_score",
    "debt_to_ebitda_score",
    "growth_gap_score",
]
financials["metrics_scored"] = financials[score_columns].count(axis=1)
financials["risk_score"] = financials[score_columns].sum(
    axis=1, min_count=len(score_columns)
).astype("Int64")
financials["risk_rank"] = (
    financials.groupby("year")["risk_score"]
    .rank(method="min", ascending=False)
    .astype("Int64")
)

financials = financials.sort_values(["year", "risk_rank", "ticker"])
financials.to_csv(OUTPUT_FILE, index=False)

summary_columns = ["year", "ticker", "metrics_scored", "risk_score", "risk_rank"]
print(financials[summary_columns].to_string(index=False))
print(f"Full results: {OUTPUT_FILE}")
