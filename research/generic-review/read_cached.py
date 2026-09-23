import json,re,sys
from pathlib import Path
D=json.load(open('2026-categorized.json'));S={s['url']:s for p in Path('research/functions/sources').glob('*.json') for s in [json.loads(p.read_text())]}
for n in map(int,sys.argv[1:]):
 r=next(x for x in D if x['record_id'].endswith(f'-{n:03}'));print('\n###',n,r['company'])
 urls=list(dict.fromkeys([d['source_url'] for d in r['cause_details'].values()]+[r.get('source_used') or r['source_url']]))
 for u in urls:
  s=S.get(u,{});t=s.get('text','NO CACHED BODY');print(u)
  # Display causal passages, not navigation or whole long articles.
  matches=list(re.finditer(r'company said|spokesperson|statement|restructur|efficien|reallocat|AI.first|AI.native|intelligence|said in|said that|reason|according|lay.off|cost|streamlin|החברה מסרה|תגובה|התייעל|Betrieb|effizien',t,re.I))
  ranges=[]
  for m in matches:
   a,b=max(0,m.start()-120),min(len(t),m.end()+550)
   if ranges and a<=ranges[-1][1]:ranges[-1][1]=max(b,ranges[-1][1])
   else:ranges.append([a,b])
  print('\n'.join(t[a:b] for a,b in ranges)[:5700] if ranges else t[:1600])
