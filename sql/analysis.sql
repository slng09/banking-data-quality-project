-- Run in SQLite against data/banking_quality.sqlite
-- Source data quality by feed
SELECT feed, COUNT(*) AS source_rows FROM source GROUP BY feed;
-- Exception distribution
SELECT feed,exception_type,COUNT(*) AS events,COUNT(DISTINCT txn_id) AS affected_ids FROM exceptions GROUP BY feed,exception_type ORDER BY events DESC;
-- Missing and mismatched valid source transactions
SELECT s.txn_id,s.date,s.feed,s.amount_cents AS source_cents,t.amount_cents AS target_cents,s.currency AS source_currency,t.currency AS target_currency
FROM valid_source s LEFT JOIN target t ON s.txn_id=t.txn_id
WHERE t.txn_id IS NULL OR s.amount_cents<>t.amount_cents OR s.currency<>t.currency ORDER BY s.date,s.txn_id;
-- Daily exception trend
SELECT date,COUNT(*) AS exception_events FROM exceptions GROUP BY date ORDER BY date;
