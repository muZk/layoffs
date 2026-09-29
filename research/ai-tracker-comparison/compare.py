"""Compare the saved public AI tracker with our H1 announcement classifications."""
import csv,json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
tracker=json.loads((OUT/'layoffs-fyi-ai-2026-09-28.json').read_text())
ours=json.loads((ROOT/'2026-categorized.json').read_text())
public={r['record_id'] for r in json.loads((ROOT/'report/records.json').read_text())}
index={(r['company'].casefold(),r['date']):r for r in ours}
# Same company/event; explicit one-day date discrepancies, not arbitrary fuzzy matching.
dates={('zoominfo','2026-05-10'):'2026-05-11',('gitlab','2026-06-02'):'2026-06-03'}
rows=[];seen=set()
for e in tracker['eventsByYear']['2026']:
 if not '2026-01-01'<=e['date']<='2026-06-30':continue
 key=(e['company'].casefold(),e['date']);r=index.get((key[0],dates.get(key,e['date'])))
 assert r, key
 seen.add(r['record_id']);ai=any(c.startswith('ai_') for c in r['causes'])
 status='excluded_period_measure' if r['record_id'] not in public else 'both_ai' if ai else 'tracker_only_ai'
 rows.append(dict(status=status,record_id=r['record_id'],company=e['company'],tracker_date=e['date'],our_date=r['date'],tracker_employees=e['count'],tracker_explanation=e.get('explanation',''),tracker_source=e.get('source',''),our_causes=';'.join(r['causes']),our_reason=r['reason']))
for r in ours:
 if r['record_id'] in public and r['record_id'] not in seen and any(c.startswith('ai_') for c in r['causes']):
  rows.append(dict(status='ours_only_ai',record_id=r['record_id'],company=r['company'],tracker_date='',our_date=r['date'],tracker_employees='',tracker_explanation='',tracker_source='',our_causes=';'.join(r['causes']),our_reason=r['reason']))
review={r['record_id']:r for r in json.loads((OUT/'consistency-review.json').read_text())}
for row in rows:
 row['review_decision']=review[row['record_id']]['decision']
 row['review_note']=review[row['record_id']]['note']
 row['our_sources']=';'.join(review[row['record_id']]['sources'])
with (OUT/'comparison.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
counts=Counter(r['status'] for r in rows)
q=[q for q in tracker['quarters'] if q['quarter'] in ['2026-Q1','2026-Q2']]
summary={'retrieved_date':'2026-09-28','api_updated_at':tracker['updatedAt'],'counts':dict(counts),'our_announcements':len(public),'our_ai':sum(r['record_id'] in public and any(c.startswith('ai_') for c in r['causes']) for r in ours),'remaining_difference_reasons':dict(Counter(row['review_decision'] for row in rows if row['status']=='tracker_only_ai')),'h1_tracker':{k:sum(v[k] for v in q) for k in ['total_events','ai_events','total_emp','ai_emp']},'date_adjustments':[{ 'company':k[0],'tracker_date':k[1],'our_date':v} for k,v in dates.items()]}
assert counts['both_ai']+counts['ours_only_ai']==sum(r['record_id'] in public and any(c.startswith('ai_') for c in r['causes']) for r in ours)
assert counts['both_ai']+counts['tracker_only_ai']+counts['excluded_period_measure']==95
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,indent=2))
