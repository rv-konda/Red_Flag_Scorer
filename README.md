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

##Example
In this demo, I used FCX and SCCO, I got the following result: 
 year ticker  metrics_scored  risk_score  risk_rank
 2023    FCX               2        <NA>       <NA>
 2023   SCCO               2        <NA>       <NA>
 2024    FCX               6           1          1
 2024   SCCO               6           0          2
 2025    FCX               6           4          1
 2025   SCCO               6           3          2

 ## Result interpretation

Both companies showed very few accounting-risk signals in 2024, with FCX scoring 1 and SCCO scoring 0. Risk indicators increased in 2025 for both companies, suggesting that their financial results became less consistent with the screener’s preferred patterns. FCX scored 4 compared with SCCO’s 3, making FCX the higher-priority company for further review, although the difference is small. The result does not imply fraud; it indicates that the flagged metrics and the related financial-statement notes should be examined more closely. The 2023 totals are unavailable because several metrics require prior-year data.
