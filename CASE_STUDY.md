# Case study — Banking Data Quality & Automated Regulatory Reporting

## Business problem
A fictional bank's CORE and CARDS feeds require consistent validation and reconciliation before downstream management and regulatory-reporting preparation.

## Solution
Created deterministic synthetic source and target extracts with controlled defects. Built a Python + SQLite pipeline to preserve raw records, apply quality rules, reconcile valid source IDs to target records, retain exception-level evidence and publish daily/feed-level KPI exports and an interactive HTML dashboard.

## Findings
Run `python src/run.py` and inspect `reports/metrics.json` and `reports/exceptions.csv` for exact reproducible results. Distinguish planted defects from unexpected findings; these numbers are illustrative, not representative of real banking systems.

## Recommendations
1. Block invalid and duplicate source records from curated reporting.
2. Implement daily completeness, amount and currency reconciliation with clear ownership.
3. Route exceptions to named owners with remediation SLAs and monitor repeat failures by feed.
4. Retain exception-level evidence for investigations and audit readiness.

## Limitations
This is a synthetic regulatory-reporting readiness prototype, not a regulator-specific return or a production control environment. It lacks production scheduling, security controls and jurisdiction-specific regulatory validation.

## Resume bullet (after reviewing the project)
Developed an independent synthetic banking data quality prototype using Python and SQL, automating transaction validation, source-to-target reconciliation, exception logging and KPI exports for management reporting.
