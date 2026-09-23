import json,re,datetime,statistics,collections
from pathlib import Path
P=Path(__file__).resolve().parent
screen=json.loads((P/'screening.json').read_text());recovered={r['company']:r for r in json.loads((P/'recovered-series.json').read_text())}
current=json.loads((P.parents[1]/'report/records.json').read_text())
# Use every attributed reason, matching the narrative and explorer.
assert {r['company'] for r in screen}=={r['company'] for r in current}, 'Refresh collection to match company coverage'
for r in screen:
 records=[x for x in current if x['company']==r['company']]
 r['record_ids']=[x['record_id'] for x in records]
 r['causes']=sorted({c for x in records for c in x['causes']})
 r['ai_mechanism']=any(c.startswith('ai_') for c in r['causes'])
rows=[]
for r in screen:
 series=recovered.get(r['company'],{});obs=[]
 for date,num in series.get('rows',[]):
  if not re.fullmatch('[A-Z][a-z]{2} [0-9]{1,2}, [0-9]{4}',date) or not re.fullmatch('[0-9,]+',num):continue
  obs.append({'date':datetime.datetime.strptime(date,'%b %d, %Y').strftime('%Y-%m-%d'),'value':int(num.replace(',','')),'source_url':series['source_url'],'source_type':'secondary_compilation'})
 r={**r,'group':'ai_recorded' if r['ai_mechanism'] else 'other_recorded' if r['causes'] else 'unresolved','observations':sorted(obs,key=lambda x:x['date'])}
 rows.append(r)
# Explicit, source-checked additions are separate from the collector.
overrides=json.loads((P/'primary-checks.json').read_text()) if (P/'primary-checks.json').exists() else []
for o in overrides:
 if o.get('value') is None:continue
 r=next(r for r in rows if r['company']==o['company']);r['observations']=[x for x in r['observations'] if x['date']!=o['date']]+[{k:o[k] for k in ['date','value','source_url']}|{'source_type':'primary_checked','definition':o.get('definition')}]
issues=json.loads((P/'quality-issues.json').read_text())
ma=json.loads((P/'perimeter-events.json').read_text())
for r in rows:
 r['quality_issues']=[i for i in issues if i['company']==r['company']]
 dropped={d for i in r['quality_issues'] for d in i.get('drop_dates',[])}
 r['observations']=[o for o in r['observations'] if o['date'] not in dropped]
 r['perimeter_events']=[m for m in ma if m['company']==r['company']]
 r['perimeter_review']='documented_examples_only_not_exhaustive'
 r['endpoints']={}
 for year in [2019,2022,2025]:
  vals=[o for o in r['observations'] if o['date'].startswith(str(year))]
  if vals:r['endpoints'][str(year)]=max(vals,key=lambda o:o['date'])
 r['growth']={f'{a}_{b}':100*(r['endpoints'][str(b)]['value']/r['endpoints'][str(a)]['value']-1) for a,b in [(2019,2022),(2022,2025),(2019,2025)] if str(a) in r['endpoints'] and str(b) in r['endpoints'] and r['endpoints'][str(a)]['value']>0}
 r['growth']={k:v for k,v in r['growth'].items() if not any(k in i.get('exclude_windows',[]) for i in r['quality_issues'])}
 r['coverage_status']='usable_pair' if r['growth'] else 'series_without_usable_pair' if r['observations'] else 'no_series_recovered' if r['series_url'] else 'not_mapped_to_standalone_public_history'
(P/'company-history.json').write_text(json.dumps(rows,indent=2))
summary={}
for window in ['2019_2022','2022_2025','2019_2025']:
 summary[window]={}
 for group in ['ai_recorded','other_recorded','unresolved']:
  sub=[r for r in rows if r['group']==group and window in r['growth']];x=[r['growth'][window] for r in sub]
  summary[window][group]={'n':len(x),'median':statistics.median(x) if x else None,'doubled':sum(v>=100 for v in x),'shrank':sum(v<0 for v in x),'companies':[r['company'] for r in sub]}
print(json.dumps(summary,indent=2));(P/'summary.json').write_text(json.dumps(summary,indent=2))

def stats_for(rows,window):
 return {g:{'n':len(v:=[r['growth'][window] for r in rows if r['group']==g and window in r['growth']]),'median':statistics.median(v) if v else None} for g in ['ai_recorded','other_recorded','unresolved']}
def outside_events(r,w):
 a,b=w.split('_')
 return not any(r['endpoints'][a]['date']<e['date']<=r['endpoints'][b]['date'] for e in r['perimeter_events'])
sensitivity={}
for w in ['2019_2022','2022_2025']:
 sub=[r for r in rows if w in r['growth']]
 sensitivity[w]={
 'same_companies_both_windows':stats_for([r for r in sub if '2019_2022' in r['growth'] and '2022_2025' in r['growth']],w),
 'exclude_documented_perimeter_events':stats_for([r for r in sub if outside_events(r,w)],w),
 'exclude_known_definition_or_scope_mismatch':stats_for([r for r in sub if not any(i.get('strict_exclusion') for i in r['quality_issues'])],w),
 'december_observations_only':stats_for([r for r in sub if all(r['endpoints'][y]['date'][5:7]=='12' for y in w.split('_'))],w),
 'baseline_at_least_1000':stats_for([r for r in sub if r['endpoints'][w.split('_')[0]]['value']>=1000],w)}
(P/'sensitivity.json').write_text(json.dumps(sensitivity,indent=2))
print(json.dumps(sensitivity,indent=2))
