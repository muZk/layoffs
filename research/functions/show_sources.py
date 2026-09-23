import json,glob,sys,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
D=json.loads((ROOT/'report/records.json').read_text());S={s['url']:s for p in (ROOT/'research/functions/sources').glob('*') for s in [json.loads(p.read_text())]}
for i in map(int,sys.argv[1:]):
 r=next(x for x in D if x['record_id'].endswith(f'-{i:03}')); print('\n###',i,r['company'])
 u=r.get('source_used') or r['source_url'];s=S.get(u,{});t=s.get('text','NO BODY');t=re.sub(r'\s+',' ',t)
 print(u)
 if len(t)>22000:
  hits=[t[max(0,m.start()-250):m.end()+550] for m in re.finditer(r'workforce|headcount|lay.off|restructur',t,re.I)];print('\n'.join(hits[:12]))
 else:print(t[:11000])
