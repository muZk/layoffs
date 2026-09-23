"""Build a typed, relational analysis export. Canonical JSON remains authoritative."""
import collections, csv, hashlib, json, sqlite3
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/normalized';OUT.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT/'2026-categorized.json'
records=json.loads(SOURCE.read_text())
def digest(s):return hashlib.sha256(s.encode()).hexdigest()[:20]
def clean(v):return None if v in (None,'','Unknown') else v
schemas={
 'companies':'company_id TEXT PRIMARY KEY, company_label TEXT NOT NULL UNIQUE',
 'sources':'source_id TEXT PRIMARY KEY, url TEXT NOT NULL UNIQUE',
 'causes':'cause_code TEXT PRIMARY KEY, is_ai INTEGER NOT NULL CHECK(is_ai IN (0,1)), specificity TEXT NOT NULL',
 'functions':'function_code TEXT PRIMARY KEY, label_es TEXT NOT NULL',
 'records':'''record_id TEXT PRIMARY KEY, company_id TEXT NOT NULL REFERENCES companies(company_id), record_date TEXT NOT NULL, record_type TEXT NOT NULL, in_report INTEGER NOT NULL CHECK(in_report IN (0,1)), exclusion_reason TEXT, laid_off INTEGER, workforce_fraction REAL CHECK(workforce_fraction IS NULL OR workforce_fraction BETWEEN 0 AND 1), raised_millions REAL, industry TEXT, funding_stage TEXT, country TEXT, headcount_scope TEXT, source_id TEXT REFERENCES sources(source_id), source_used_id TEXT REFERENCES sources(source_id), review_date TEXT, review_status TEXT NOT NULL, review_note TEXT, cause_status TEXT, affected_work_status TEXT, work_review_date TEXT, work_review_method TEXT, work_review_note TEXT, schema_version INTEGER''',
 'record_causes':'''record_id TEXT NOT NULL REFERENCES records(record_id), cause_code TEXT NOT NULL REFERENCES causes(cause_code), attribution TEXT NOT NULL, scope TEXT NOT NULL, summary TEXT NOT NULL, source_id TEXT REFERENCES sources(source_id), evidence_access TEXT, PRIMARY KEY(record_id,cause_code)''',
 'record_functions':'''record_id TEXT NOT NULL REFERENCES records(record_id), function_code TEXT NOT NULL REFERENCES functions(function_code), PRIMARY KEY(record_id,function_code)''',
 'function_evidence':'''evidence_id TEXT PRIMARY KEY, record_id TEXT NOT NULL REFERENCES records(record_id), attribution TEXT, summary TEXT, source_id TEXT REFERENCES sources(source_id), evidence_access TEXT''',
 'function_evidence_functions':'''evidence_id TEXT NOT NULL REFERENCES function_evidence(evidence_id), function_code TEXT NOT NULL REFERENCES functions(function_code), PRIMARY KEY(evidence_id,function_code)''',
 'record_sources':'''record_id TEXT NOT NULL REFERENCES records(record_id), source_id TEXT NOT NULL REFERENCES sources(source_id), role TEXT NOT NULL, PRIMARY KEY(record_id,source_id,role)''',
 'review_issues':'record_id TEXT NOT NULL REFERENCES records(record_id), issue TEXT NOT NULL, PRIMARY KEY(record_id,issue)',
 'locations':'record_id TEXT NOT NULL REFERENCES records(record_id), position INTEGER NOT NULL, location_label TEXT, PRIMARY KEY(record_id,position)',
 'context':'context_id TEXT PRIMARY KEY, record_id TEXT NOT NULL REFERENCES records(record_id), kind TEXT, summary TEXT, source_id TEXT REFERENCES sources(source_id)',
 'denials':'denial_id TEXT PRIMARY KEY, record_id TEXT NOT NULL REFERENCES records(record_id), target TEXT, speaker TEXT, summary TEXT, source_id TEXT REFERENCES sources(source_id)',
 'work_units':'unit_id TEXT PRIMARY KEY, record_id TEXT NOT NULL REFERENCES records(record_id), name TEXT, summary TEXT, source_id TEXT REFERENCES sources(source_id)',
 'work_levels':'record_id TEXT NOT NULL REFERENCES records(record_id), level TEXT NOT NULL, PRIMARY KEY(record_id,level)',
 'headcount_accounts':'account_id TEXT PRIMARY KEY, record_id TEXT NOT NULL REFERENCES records(record_id), value REAL, workforce_fraction REAL, attribution TEXT, note TEXT, source_id TEXT REFERENCES sources(source_id)',
 'workforce_metrics':'record_id TEXT PRIMARY KEY REFERENCES records(record_id), value REAL, metric TEXT, period TEXT, source_min REAL, source_max REAL, note TEXT, source_id TEXT REFERENCES sources(source_id)',
 'related_records':'record_id TEXT NOT NULL REFERENCES records(record_id), related_record_id TEXT NOT NULL REFERENCES records(record_id), relationship TEXT NOT NULL, source_id TEXT REFERENCES sources(source_id), PRIMARY KEY(record_id,related_record_id,relationship)',
 'coverage':'record_id TEXT PRIMARY KEY REFERENCES records(record_id), tracker TEXT, retrieved_date TEXT, tracker_date TEXT',
}
tables={t:[] for t in schemas};source_map={}
def sid(url):
 if not url:return None
 if url not in source_map:
  source_map[url]='src_'+digest(url);tables['sources'].append({'source_id':source_map[url],'url':url})
 return source_map[url]
def add(t,**row):tables[t].append(row)
companies={x['company']:'co_'+digest(x['company']) for x in records}
for label,key in sorted(companies.items()):add('companies',company_id=key,company_label=label)
causes={c:d['specificity'] for r in records for c,d in r['cause_details'].items()}
for c,s in sorted(causes.items()):add('causes',cause_code=c,is_ai=int(c.startswith('ai_')),specificity=s)
for c,label in json.loads((ROOT/'research/functions/taxonomy.json').read_text()).items():add('functions',function_code=c,label_es=label)
for r in records:
 date.fromisoformat(r['date'])
 key=r['record_id'];h1='2026-01-01'<=r['date']<'2026-07-01';included=h1 and r['record_type']=='announcement';review=r['review'];work=r.get('affected_work',{});wr=work.get('review',{})
 add('records',record_id=key,company_id=companies[r['company']],record_date=r['date'],record_type=r['record_type'],in_report=int(included),exclusion_reason=None if included else 'outside_2026_h1' if not h1 else 'not_new_announcement',laid_off=r['laid_off'],workforce_fraction=r['pct'],raised_millions=r['raised_mm'],industry=clean(r['industry']),funding_stage=clean(r['stage']),country=clean(r['country']),headcount_scope=r['headcount_scope'],source_id=sid(r['source_url']),source_used_id=sid(r['source_used']),review_date=review['date'],review_status=review['status'],review_note=review['note'],cause_status=r['cause_status'],affected_work_status=work.get('status'),work_review_date=wr.get('date'),work_review_method=wr.get('method'),work_review_note=wr.get('note'),schema_version=r['schema_version'])
 for c,d in r['cause_details'].items():add('record_causes',record_id=key,cause_code=c,attribution=d['attribution'],scope=d['scope'],summary=d['summary'],source_id=sid(d['source_url']),evidence_access=d.get('evidence_access'))
 for f in work.get('functions',[]):add('record_functions',record_id=key,function_code=f)
 for i,d in enumerate(work.get('details',[])):
  eid=key+'_function_'+str(i);add('function_evidence',evidence_id=eid,record_id=key,attribution=d['attribution'],summary=d['summary'],source_id=sid(d['source_url']),evidence_access=d.get('evidence_access'))
  for f in d['functions']:add('function_evidence_functions',evidence_id=eid,function_code=f)
 for role,obj in [('record_review',review),('work_review',wr),('explanation_review',r.get('explanation_review',{})),('generic_review',r.get('generic_review',{}))]:
  for url in dict.fromkeys(obj.get('sources',[])):add('record_sources',record_id=key,source_id=sid(url),role=role)
 for issue in dict.fromkeys(review['issues']):add('review_issues',record_id=key,issue=issue)
 for i,label in enumerate(r['location_hq']):add('locations',record_id=key,position=i,location_label=label)
 for level in dict.fromkeys(work.get('levels',[])):add('work_levels',record_id=key,level=level)
 for table,items,idfield,fields in [('context',r['context'],'context_id',['kind','summary']),('denials',r['denials'],'denial_id',['target','speaker','summary']),('work_units',work.get('units',[]),'unit_id',['name','summary']),('headcount_accounts',r.get('headcount_accounts',[]),'account_id',['value','attribution','note'])]:
  for i,item in enumerate(items):
   row={f:item.get(f) for f in fields};row.update({idfield:key+'_'+table+'_'+str(i),'record_id':key,'source_id':sid(item.get('source_url'))})
   if table=='headcount_accounts':row['workforce_fraction']=item.get('pct')
   add(table,**row)
 if 'reported_workforce_change' in r:
  m=r['reported_workforce_change'];bounds=m.get('source_range',[None,None]);add('workforce_metrics',record_id=key,value=m.get('value'),metric=m.get('metric'),period=m.get('period'),source_min=bounds[0],source_max=bounds[1],note=m.get('note'),source_id=sid(m.get('source_url')))
 for rel in r.get('related_records',[]):add('related_records',record_id=key,related_record_id=rel['record_id'],relationship=rel['relationship'],source_id=sid(rel['source_url']))
 if 'coverage_source' in r:
  c=r['coverage_source'];add('coverage',record_id=key,tracker=c.get('tracker'),retrieved_date=c.get('retrieved'),tracker_date=c.get('tracker_date'))
# Foreign keys are checked after loading because records can refer forward to another record.
target=OUT/'layoffs.sqlite';tmp=OUT/'layoffs.sqlite.tmp';tmp.unlink(missing_ok=True)
con=sqlite3.connect(tmp);con.row_factory=sqlite3.Row
for table,ddl in schemas.items():
 con.execute(f'CREATE TABLE {table} ({ddl})')
 for row in tables[table]:
  assert not any(isinstance(v,(list,dict)) for v in row.values()),(table,row)
  cols=list(row);con.execute(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})",list(row.values()))
con.executescript('''
CREATE INDEX cause_records ON record_causes(cause_code,record_id);
CREATE INDEX record_company_date ON records(company_id,record_date);
CREATE INDEX function_records ON record_functions(function_code,record_id);
CREATE VIEW announcements AS SELECT r.*,c.company_label,
 (SELECT COUNT(*) FROM record_causes rc WHERE rc.record_id=r.record_id) AS reason_count,
 EXISTS(SELECT 1 FROM record_causes rc JOIN causes ca USING(cause_code) WHERE rc.record_id=r.record_id AND ca.is_ai=1) AS has_ai_reason,
 (SELECT COUNT(*) FROM record_functions rf WHERE rf.record_id=r.record_id) AS function_count
 FROM records r JOIN companies c USING(company_id) WHERE r.in_report=1;
CREATE VIEW announcement_causes AS SELECT rc.* FROM record_causes rc JOIN records r USING(record_id) WHERE r.in_report=1;
CREATE VIEW announcement_functions AS SELECT rf.* FROM record_functions rf JOIN records r USING(record_id) WHERE r.in_report=1;
CREATE VIEW excluded_records AS SELECT r.record_id,c.company_label,r.record_date,r.record_type,r.exclusion_reason FROM records r JOIN companies c USING(company_id) WHERE in_report=0;
''')
assert not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert con.execute('SELECT COUNT(*) FROM announcements').fetchone()[0]==228
assert con.execute('SELECT SUM(has_ai_reason) FROM announcements').fetchone()[0]==72
expected=collections.Counter(c for r in records if '2026-01-01'<=r['date']<'2026-07-01' and r['record_type']=='announcement' for c in r['causes'])
assert dict(con.execute('SELECT cause_code,COUNT(*) FROM announcement_causes GROUP BY cause_code').fetchall())==dict(expected)
assert {r['record_id'] for r in records}=={r[0] for r in con.execute('SELECT record_id FROM records')}
for r in records:
 key=r['record_id'];assert set(r['causes'])=={x[0] for x in con.execute('SELECT cause_code FROM record_causes WHERE record_id=?',(key,))}
 assert set(r.get('affected_work',{}).get('functions',[]))=={x[0] for x in con.execute('SELECT function_code FROM record_functions WHERE record_id=?',(key,))}
views=['announcements','announcement_causes','announcement_functions','excluded_records'];manifest={}
for table in list(schemas)+views:
 rows=con.execute(f'SELECT * FROM {table} ORDER BY 1,2').fetchall();headers=[d[0] for d in con.execute(f'SELECT * FROM {table} LIMIT 0').description]
 with (OUT/(table+'.csv')).open('w',newline='') as f:
  writer=csv.writer(f);writer.writerow(headers);writer.writerows(rows)
 manifest[table]={'rows':len(rows),'columns':headers,'kind':'view' if table in views else 'table'}
con.commit();con.close();tmp.replace(target)
(OUT/'schema.sql').write_text('\n'.join(sql+';' for (sql,) in sqlite3.connect(target).execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL ORDER BY CASE type WHEN 'table' THEN 0 WHEN 'index' THEN 1 ELSE 2 END,name"))+'\n')
meta={'schema_version':1,'canonical_source':'../../2026-categorized.json','canonical_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'builder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'latest_record_review':max(r['review']['date'] for r in records),'coverage_snapshot':'2026-09-17','report_window':['2026-01-01','2026-06-30'],'unknown_policy':'Unknown and empty dimensions become NULL; unknown numeric values remain NULL, never zero. CSV empty cells represent NULL.','company_policy':'Exact source labels only; no inferred parent/entity merging. IDs are stable hashes of labels.','boolean_encoding':'0/1','percent_encoding':'Fraction in [0,1], e.g. 0.1 = 10%.','tables':manifest,'checks':['SQLite integrity','foreign keys','unique keys','scalar-only CSV fields','all record IDs preserved','per-record causes/functions preserved','all H1 cause counts match canonical JSON','228 public announcements','72 announcements with attributed AI reason'],'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.suffix in ['.csv','.sqlite','.sql']}}
(OUT/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({t:x['rows'] for t,x in manifest.items()},indent=2))
