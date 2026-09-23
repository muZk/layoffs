-- 228 announcements; 72 with an attributed AI reason.
SELECT COUNT(*) AS announcements, SUM(has_ai_reason) AS with_ai
FROM announcements;

-- Rank all attributed reasons (including general reasons).
SELECT cause_code, COUNT(DISTINCT record_id) AS announcements
FROM announcement_causes
GROUP BY cause_code ORDER BY announcements DESC, cause_code;

-- 12 announcements: AI productivity + cost cutting.
SELECT COUNT(DISTINCT a.record_id) AS announcements
FROM announcement_causes a
JOIN announcement_causes b USING(record_id)
WHERE a.cause_code='ai_productivity' AND b.cause_code='cost_cutting';

-- Inspect the statements and sources behind that pair.
SELECT e.record_id, e.company_label, e.record_date,
       a.cause_code, a.attribution, a.scope, a.summary, s.url
FROM announcements e
JOIN announcement_causes a USING(record_id)
LEFT JOIN sources s ON s.source_id=a.source_id
WHERE EXISTS (SELECT 1 FROM announcement_causes x
              WHERE x.record_id=e.record_id AND x.cause_code='ai_productivity')
  AND EXISTS (SELECT 1 FROM announcement_causes x
              WHERE x.record_id=e.record_id AND x.cause_code='cost_cutting')
ORDER BY e.record_id, a.cause_code;

-- Functions, counting announcements rather than positions.
SELECT f.function_code, COUNT(DISTINCT f.record_id) AS announcements,
       COUNT(DISTINCT CASE WHEN e.has_ai_reason=1 THEN e.record_id END) AS with_ai
FROM announcement_functions f JOIN announcements e USING(record_id)
GROUP BY f.function_code ORDER BY announcements DESC;

-- Unknown data and explicit exclusions remain inspectable.
SELECT SUM(industry IS NULL) AS unknown_industry,
       SUM(laid_off IS NULL) AS unknown_headcount FROM announcements;
SELECT * FROM excluded_records;
