-- Run against data/quality.db in SQLite.
SELECT feed,COUNT(*) AS source_rows FROM source GROUP BY feed;
SELECT feed,type,COUNT(*) AS exception_events FROM exceptions GROUP BY feed,type ORDER BY exception_events DESC;
SELECT s.id,s.day,s.feed,s.amount_cents AS source_cents,t.amount_cents AS target_cents FROM source s LEFT JOIN target t ON s.id=t.id WHERE t.id IS NULL OR s.amount_cents<>t.amount_cents;
