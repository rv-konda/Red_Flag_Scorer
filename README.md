# Red_Flag_Scorer

A Python tool for comparing accounting risk indicators across companies and fiscal years. It reads a (annual) financial statement CSV and exports six metrics, individual flag scores, and annual rankings to an Excel-compatible CSV.

## Metrics and scoring

Each metric scores 0 for no flag, 1 for a moderate flag, or 2 for a stronger flag under the preset thresholds. Company-years with all six scores receive a total out of 12 and a rank within the fiscal year.

- *Cash conversion* — Compares operating cash flow with net income to see how much reported profit turned into operating cash.
- *Accrual ratio* — Measures the gap between net income and operating cash flow relative to average total assets.
- *Receivables-to-revenue change* — Flags when trade receivables rise relative to revenue compared with the prior year.
- *Inventory-to-revenue change* — Flags when inventory rises relative to revenue compared with the prior year.
- *Debt to EBITDA* — Measures total debt, excluding lease liabilities, relative to EBITDA.
- *Revenue–cash flow growth gap* — Flags when year-over-year revenue growth outpaces operating cash flow growth.
The **optional explainer** sends one company-year’s calculated metrics and scores to the OpenAI API. It prints a short research note describing the flags and suggesting what to check in the filing. The scoring rules and rankings are calculated independently in `screen.py`.
