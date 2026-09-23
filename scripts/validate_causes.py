"""Validate complete review, audit chain and CSV; print current counts."""
import collections
import csv
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'ai_substitution','ai_productivity','ai_work_redesign','ai_investment_reallocation','ai_market_disruption','cost_cutting','organizational_consolidation','strategic_pivot','m_and_a','financial_distress','demand_decline','shutdown','unit_closure','work_relocation','market_exit','lost_contract','ipo_prep','performance_cull','regulatory','overhiring_correction'}
ALLOWED |= {'organizational_realignment','strategic_priorities','operational_efficiency','market_conditions','ai_transition'}
ATTRIBUTIONS = {'company_stated','press_reported','reported_inference','worker_reported','company_and_worker_reported'}
def read(name): return json.loads((ROOT/name).read_text())
def h1_records(data): return [r for r in data if '2026-01-01' <= r['date'] < '2026-07-01']
def announcement_records(data): return [r for r in h1_records(data) if r['record_type']=='announcement']
def stats(data):
 h1=h1_records(data);events=announcement_records(data)
 ai=lambda r:any(c.startswith('ai_') for c in r['causes'])
 return {'all_records':len(data),'h1_records':len(h1),'h1_announcement_records':len(events),'review_all':dict(collections.Counter(r['review']['status'] for r in data)),'cause_status_h1_announcements':dict(collections.Counter(r['cause_status'] for r in events)),'causes_h1_announcements':dict(collections.Counter(c for r in events for c in r['causes'])),'multiple_causes':sum(len(r['causes'])>1 for r in events),'ai_reason_recorded':sum(ai(r) for r in events),'ai_and_other_reason':sum(ai(r) and any(not c.startswith('ai_') for c in r['causes']) for r in events),'no_classifiable_explanation':sum(not r['causes'] for r in events)}
def validate():
 data=read('2026-categorized.json');audit=read('full-review-2026-09-16.json')['events'];legacy=read('2026-legacy-classifications.json')['records'];original=read('cause-audit-2026-09-16.json')['events'];follow={(r['company'],r['date']):r for r in read('ai-classification-audit-2026-09-16.json')['events']};errors=[]
 def check(value,message):
  if not value:errors.append(message)
 extension=read('coverage/extension-audit-2026-09-17.json')
 check(len(audit)==len(legacy)==len(original)==163,'Historical audit coverage changed')
 expected_records=[a['after'] for a in audit]+extension['added']
 for revision in read('coverage/source-followup-2026-09-17.json')['events']:
  index=next(i for i,r in enumerate(expected_records) if r['record_id']==revision['before']['record_id'])
  check(expected_records[index]==revision['before'],'Follow-up audit before mismatch')
  expected_records[index]=revision['after']
 for revision in read('coverage/functions-followup-2026-09-17.json')['events']:
  index=next(i for i,r in enumerate(expected_records) if r['record_id']==revision['before']['record_id'])
  check(expected_records[index]==revision['before'],'Functions follow-up audit before mismatch')
  expected_records[index]=revision['after']
 for revision in read('coverage/explanations-followup-2026-09-17.json')['events']:
  index=next(i for i,r in enumerate(expected_records) if r['record_id']==revision['before']['record_id'])
  check(expected_records[index]==revision['before'],'Explanations follow-up audit before mismatch')
  expected_records[index]=revision['after']
 for revision in read('coverage/explanation-recheck-2026-09-17.json')['events']:
  index=next(i for i,r in enumerate(expected_records) if r['record_id']==revision['before']['record_id'])
  check(expected_records[index]==revision['before'],'Explanation recheck audit before mismatch')
  expected_records[index]=revision['after']
 for revision in read('coverage/generic-followup-2026-09-17.json')['events']:
  index=next(i for i,r in enumerate(expected_records) if r['record_id']==revision['before']['record_id'])
  check(expected_records[index]==revision['before'],'Generic follow-up audit before mismatch')
  expected_records[index]=revision['after']
 check(data==expected_records,'Reviewed records differ from audit chain')
 check(len(data)==163+len(extension['added']),'Coverage changed')
 check(len({r['record_id'] for r in data})==len(data),'Duplicate IDs')
 for a,old,first in zip(audit,legacy,original):
  key=a['after']['record_id'];check(a['before']==old,f'{key}: full audit mismatch');f=follow.get((old['company'],old['date']));check(not f or f['after']==old,f'{key}: earlier review mismatch');initial=f['before'] if f else old
  check(all(initial.get(k)==v for k,v in first['after'].items()),f'{key}: initial audit mismatch')
 for r in data:
  key=r['record_id']
  check(r['schema_version']==2,f'{key}: schema version');check(set(r['causes'])<=ALLOWED,f'{key}: unknown cause');check(len(set(r['causes']))==len(r['causes']),f'{key}: repeated cause');check(set(r['causes'])==set(r['cause_details']),f'{key}: evidence keys');check(r['review']['status'] in {'source_reviewed','partial','unavailable'},f'{key}: review status');check(bool(r['review']['note']),f'{key}: missing assessment')
  expected=('specified' if any(d['specificity']=='concrete' for d in r['cause_details'].values()) else 'generic') if r['causes'] else {'source_reviewed':'unspecified','partial':'unresolved','unavailable':'unavailable'}[r['review']['status']]
  check(r['cause_status']==expected,f'{key}: cause status')
  check(not any(k in r for k in ['papel_ia','ai_link','es_causa_ia','nego_ia','observations','reason_primary']),f'{key}: competing legacy axis')
  for c,detail in r['cause_details'].items():
   check(detail.get('specificity') in {'concrete','generic'},f'{key}/{c}: specificity')
   check((c in read('research/explanations/taxonomy.json'))==(detail.get('specificity')=='generic'),f'{key}/{c}: taxonomy/detail mismatch')
   check(detail['attribution'] in ATTRIBUTIONS,f'{key}/{c}: attribution');check(bool(detail['summary']) and bool(detail['scope']),f'{key}/{c}: missing evidence');check(detail['source_url'] in r['review']['sources'],f'{key}/{c}: missing source')
  for denial in r['denials']:check(denial['target'] and denial['speaker'] in {'company','anonymous_source'},f'{key}: denial scope/speaker')
  metric=r.get('reported_workforce_change',{}).get('metric','')
  if 'net_' in metric or r['record_type']!='announcement':check(r['laid_off'] is None,f'{key}: non-layoff metric counted as gross layoffs')
  if r in announcement_records(data):
   work=r.get('affected_work',{});check(work.get('status') in {'identified','unit_only','not_identified'},f'{key}: affected-work review missing')
   check(set(work.get('functions',[]))<=set(read('research/functions/taxonomy.json')),f'{key}: unknown function')
   check(bool(work.get('functions'))==(work.get('status')=='identified'),f'{key}: function status mismatch')
   check(set(work.get('functions',[]))=={f for d in work.get('details',[]) for f in d['functions']},f'{key}: function evidence mismatch')
   for d in work.get('details',[]):
    check(d['source_url'] in work['review']['sources'] and d['attribution'] in ATTRIBUTIONS,f'{key}: function provenance')
 rows=list(csv.DictReader((ROOT/'2026-categorized.csv').open(newline='')));check(len(rows)==len(data),'CSV coverage')
 for row,r in zip(rows,data):
  for k in row:
   v=r.get(k);actual=json.loads(row[k]) if isinstance(v,(list,dict)) else row[k];expected=v if isinstance(v,(list,dict)) else '' if v is None else str(v);check(actual==expected,f"{r['record_id']}: CSV {k}")
 if errors:raise SystemExit('\n'.join(errors))
 print(json.dumps(stats(data),indent=2))
if __name__=='__main__':validate()
