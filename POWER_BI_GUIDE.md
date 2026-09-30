# Power BI report build guide

Import `reports/daily_kpis.csv`, `reports/feed_summary.csv`, and `reports/exception_detail.csv` using **Get Data → Text/CSV**. Set day to Date and numeric fields to numeric types.

## Executive summary
Cards: Source Rows, Valid Rows, Validation Pass %, Exception Events. Line chart: exception events by day. Bar chart: exception events by type.

## Suggested DAX (daily_kpis table)
```
Source Rows = SUM(daily_kpis[source_rows])
Valid Rows = SUM(daily_kpis[valid_rows])
Validation Pass % = DIVIDE([Valid Rows], [Source Rows])
Exception Events = SUM(daily_kpis[exception_events])
```

## Exception investigation
Use `exception_detail` to build a searchable table of transaction ID, date, feed, type, and explanation. Use `feed_summary` for the per-feed overview. Do not add feed_summary totals to daily_kpis totals; they are alternate aggregations of the same records.
