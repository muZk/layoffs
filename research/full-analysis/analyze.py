"""Descriptive analysis of all attributed explanations; no specificity exclusion."""
from pathlib import Path
import json,collections,itertools
ROOT=Path(__file__).resolve().parents[2]
D=json.loads((ROOT/'2026-categorized.json').read_text())
R=[r for r in D if r['record_type']=='announcement' and '2026-01-01'<=r['date']<'2026-07-01']
def isai(c):return c.startswith('ai_')
def hasai(r):return any(map(isai,r['causes']))
def count(keys):return dict(collections.Counter(keys).most_common())
causes=count(c for r in R for c in r['causes'])
pairs=collections.Counter(tuple(sorted(p)) for r in R for p in itertools.combinations(set(r['causes']),2))
bycause={c:{'announcements':n,'record_ids':[r['record_id'] for r in R if c in r['causes']],'attribution':count(r['cause_details'][c]['attribution'] for r in R if c in r['causes']),'scope':count(r['cause_details'][c]['scope'] for r in R if c in r['causes']),'functions_identified':sum(bool(r['affected_work']['functions']) for r in R if c in r['causes'])} for c,n in causes.items()}
functions={f:{'announcements':sum(f in r['affected_work']['functions'] for r in R),'with_ai':sum(f in r['affected_work']['functions'] and hasai(r) for r in R)} for f in sorted(set(f for r in R for f in r['affected_work']['functions']))}
results={'basis':'All attributed causes, including general reasons. Counts are announcements, not jobs or independently proven causes.','n':len(R),'with_explanation':sum(bool(r['causes']) for r in R),'ai':sum(map(hasai,R)),'groups':{'ai_and_other':sum(hasai(r) and any(not isai(c) for c in r['causes']) for r in R),'ai_only':sum(hasai(r) and all(map(isai,r['causes'])) for r in R),'other_only':sum(bool(r['causes']) and not hasai(r) for r in R),'no_classifiable_explanation':sum(not r['causes'] for r in R)},'multiple_explanations':sum(len(r['causes'])>1 for r in R),'reason_counts':causes,'pairs':[{'reasons':list(k),'announcements':n,'record_ids':[r['record_id'] for r in R if all(c in r['causes'] for c in k)]} for k,n in sorted(pairs.items(),key=lambda x:(-x[1],x[0]))],'by_reason':bycause,'functions':functions,'ai_without_identified_functions':sum(hasai(r) and not r['affected_work']['functions'] for r in R),'no_ai_without_identified_functions':sum(not hasai(r) and not r['affected_work']['functions'] for r in R),'industry':{k:{'announcements':sum(r['industry']==k for r in R),'with_ai':sum(r['industry']==k and hasai(r) for r in R)} for k in sorted(set(r['industry'] for r in R))},'source_status':count(r['review']['status'] for r in R)}
(ROOT/'research/full-analysis/results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
(ROOT/'report/analysis.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in results.items() if k not in ['by_reason','pairs','industry']},ensure_ascii=False,indent=2))
print('TOP PAIRS',[(x['reasons'],x['announcements']) for x in results['pairs'][:15]])
print('ATTRIBUTIONS', {c:v['attribution'] for c,v in bycause.items() if isai(c)})
print('INDUSTRIES',sorted(results['industry'].items(),key=lambda x:-x[1]['announcements'])[:12])
