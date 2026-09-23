CREATE TABLE causes (cause_code TEXT PRIMARY KEY, is_ai INTEGER NOT NULL CHECK(is_ai IN (0,1)), specificity TEXT NOT NULL);
CREATE TABLE companies (company_id TEXT PRIMARY KEY, company_label TEXT NOT NULL UNIQUE);
CREATE TABLE context (context_id TEXT PRIMARY KEY, record_id TEXT NOT NULL REFERENCES records(record_id), kind TEXT, summary TEXT, source_id TEXT REFERENCES sources(source_id));
CREATE TABLE coverage (record_id TEXT PRIMARY KEY REFERENCES records(record_id), tracker TEXT, retrieved_date TEXT, tracker_date TEXT);
CREATE TABLE denials (denial_id TEXT PRIMARY KEY, record_id TEXT NOT NULL REFERENCES records(record_id), target TEXT, speaker TEXT, summary TEXT, source_id TEXT REFERENCES sources(source_id));
CREATE TABLE function_evidence (evidence_id TEXT PRIMARY KEY, record_id TEXT NOT NULL REFERENCES records(record_id), attribution TEXT, summary TEXT, source_id TEXT REFERENCES sources(source_id), evidence_access TEXT);
CREATE TABLE function_evidence_functions (evidence_id TEXT NOT NULL REFERENCES function_evidence(evidence_id), function_code TEXT NOT NULL REFERENCES functions(function_code), PRIMARY KEY(evidence_id,function_code));
CREATE TABLE functions (function_code TEXT PRIMARY KEY, label_es TEXT NOT NULL);
CREATE TABLE headcount_accounts (account_id TEXT PRIMARY KEY, record_id TEXT NOT NULL REFERENCES records(record_id), value REAL, workforce_fraction REAL, attribution TEXT, note TEXT, source_id TEXT REFERENCES sources(source_id));
CREATE TABLE locations (record_id TEXT NOT NULL REFERENCES records(record_id), position INTEGER NOT NULL, location_label TEXT, PRIMARY KEY(record_id,position));
CREATE TABLE record_causes (record_id TEXT NOT NULL REFERENCES records(record_id), cause_code TEXT NOT NULL REFERENCES causes(cause_code), attribution TEXT NOT NULL, scope TEXT NOT NULL, summary TEXT NOT NULL, source_id TEXT REFERENCES sources(source_id), evidence_access TEXT, PRIMARY KEY(record_id,cause_code));
CREATE TABLE record_functions (record_id TEXT NOT NULL REFERENCES records(record_id), function_code TEXT NOT NULL REFERENCES functions(function_code), PRIMARY KEY(record_id,function_code));
CREATE TABLE record_sources (record_id TEXT NOT NULL REFERENCES records(record_id), source_id TEXT NOT NULL REFERENCES sources(source_id), role TEXT NOT NULL, PRIMARY KEY(record_id,source_id,role));
CREATE TABLE records (record_id TEXT PRIMARY KEY, company_id TEXT NOT NULL REFERENCES companies(company_id), record_date TEXT NOT NULL, record_type TEXT NOT NULL, in_report INTEGER NOT NULL CHECK(in_report IN (0,1)), exclusion_reason TEXT, laid_off INTEGER, workforce_fraction REAL CHECK(workforce_fraction IS NULL OR workforce_fraction BETWEEN 0 AND 1), raised_millions REAL, industry TEXT, funding_stage TEXT, country TEXT, headcount_scope TEXT, source_id TEXT REFERENCES sources(source_id), source_used_id TEXT REFERENCES sources(source_id), review_date TEXT, review_status TEXT NOT NULL, review_note TEXT, cause_status TEXT, affected_work_status TEXT, work_review_date TEXT, work_review_method TEXT, work_review_note TEXT, schema_version INTEGER);
CREATE TABLE related_records (record_id TEXT NOT NULL REFERENCES records(record_id), related_record_id TEXT NOT NULL REFERENCES records(record_id), relationship TEXT NOT NULL, source_id TEXT REFERENCES sources(source_id), PRIMARY KEY(record_id,related_record_id,relationship));
CREATE TABLE review_issues (record_id TEXT NOT NULL REFERENCES records(record_id), issue TEXT NOT NULL, PRIMARY KEY(record_id,issue));
CREATE TABLE sources (source_id TEXT PRIMARY KEY, url TEXT NOT NULL UNIQUE);
CREATE TABLE work_levels (record_id TEXT NOT NULL REFERENCES records(record_id), level TEXT NOT NULL, PRIMARY KEY(record_id,level));
CREATE TABLE work_units (unit_id TEXT PRIMARY KEY, record_id TEXT NOT NULL REFERENCES records(record_id), name TEXT, summary TEXT, source_id TEXT REFERENCES sources(source_id));
CREATE TABLE workforce_metrics (record_id TEXT PRIMARY KEY REFERENCES records(record_id), value REAL, metric TEXT, period TEXT, source_min REAL, source_max REAL, note TEXT, source_id TEXT REFERENCES sources(source_id));
CREATE INDEX cause_records ON record_causes(cause_code,record_id);
CREATE INDEX function_records ON record_functions(function_code,record_id);
CREATE INDEX record_company_date ON records(company_id,record_date);
CREATE VIEW announcement_causes AS SELECT rc.* FROM record_causes rc JOIN records r USING(record_id) WHERE r.in_report=1;
CREATE VIEW announcement_functions AS SELECT rf.* FROM record_functions rf JOIN records r USING(record_id) WHERE r.in_report=1;
CREATE VIEW announcements AS SELECT r.*,c.company_label,
 (SELECT COUNT(*) FROM record_causes rc WHERE rc.record_id=r.record_id) AS reason_count,
 EXISTS(SELECT 1 FROM record_causes rc JOIN causes ca USING(cause_code) WHERE rc.record_id=r.record_id AND ca.is_ai=1) AS has_ai_reason,
 (SELECT COUNT(*) FROM record_functions rf WHERE rf.record_id=r.record_id) AS function_count
 FROM records r JOIN companies c USING(company_id) WHERE r.in_report=1;
CREATE VIEW excluded_records AS SELECT r.record_id,c.company_label,r.record_date,r.record_type,r.exclusion_reason FROM records r JOIN companies c USING(company_id) WHERE in_report=0;
