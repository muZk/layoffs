"""Apply the explicit tracker-first policy once, with an immutable before/after audit."""
import copy,csv,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
A=R/'coverage/ai-tracker-baseline-2026-09-28.json'
if A.exists():raise SystemExit('Already applied; do not replay.')
old=json.loads((R/'2026-categorized.json').read_text());data=copy.deepcopy(old)
rows=list(csv.DictReader((P/'comparison.csv').open())); target={x['record_id']:x for x in rows if x['status']=='tracker_only_ai'}
ledger=json.loads((P/'consistency-review.json').read_text());byreview={r['record_id']:r for r in ledger}
tracker='https://layoffs.fyi/ai-layoffs/'
confirmed={
9:('ai_investment_reallocation','press_reported','Reporting connects the Reality Labs reduction to reallocating investment toward AI and smart glasses. This broader context supports the tracker AI label; it does not establish task replacement.','https://roadtovr.com/meta-layoff-10-percent-reality-labs-report/','2026-01-13'),
80:('ai_investment_reallocation','press_reported','Reuters connects the March restructuring to offsetting AI investment costs. This supports an AI funding link rather than a claim that AI replaced the affected roles.','https://finance.yahoo.com/markets/stocks/articles/meta-lay-off-hundreds-employees-141106014.html','2026-03-25'),
149:('ai_work_redesign','company_stated','Internal communications reported by ET connect the May 13 restructuring with changing engineering work under AI-led development. Preserve the separate anonymous denial of replacing jobs with AI; redesign and replacement are different claims.','https://hr.economictimes.indiatimes.com/amp/news/workplace-4-0/talent-management/linkedin-cuts-350-jobs-in-india-amid-global-restructuring/131303309','2026-05-25'),
143:('ai_work_redesign','press_reported','Heise reports that development and support move from Germany to Hungary with AI assistance. The retrieved article excerpt supports AI-assisted work redesign but does not quantify substitution.','https://www.heise.de/news/Verlagerung-ins-Ausland-One-Identity-schliesst-Entwicklung-in-Deutschland-11287793.html','2026-05-13'),
210:('ai_investment_reallocation','company_stated','The parent company employee letter includes Credit Karma reductions in the same announced reallocation plan that funds an AI-native platform. Retain that plan-level context without claiming every local role was replaced by AI; possible overlap with the parent announcement remains.','https://investors.intuit.com/sec-filings/all-sec-filings/content/0000896878-26-000024/fy26q3-ex9902.htm','2026-05-21'),
135:('ai_transition','press_reported','Hoodline attributes this restructuring to an AI-oriented strategy. Keep the press attribution alongside the company explanation about priorities and layers; neither proves automated replacement of each role.','https://hoodline.com/2026/05/ticketmaster-axes-350-jobs-as-it-fast-tracks-new-tech/','2026-05-13'),
49:('ai_transition','reported_inference','NEXT.io places this reduction in an AI-led operating-cost strategy. This is the publication interpretation, not a company statement that specific jobs were automated.','https://next.io/news/people/draftkings-reduces-workforce-company-embraces-ai/','2026-02-24'),
}
for r in data:
 key=r['record_id'];n=int(key.split('-')[-1])
 if key not in target:continue
 t=target[key];l=byreview[key]
 if n==197:
  src='https://techcrunch.com/2025/08/26/verily-is-closing-its-medical-device-program-as-alphabet-shifts-more-resources-to-ai/'
  summary='The tracker explanation names the devices-program closure announced in August 2025, while this record is the June 2026 notice for 58 positions. Retain the difference because the cited mechanism belongs to an earlier event; no assertion that AI played no role in 2026.'
  r['review']['sources']=list(dict.fromkeys(r['review']['sources']+[tracker,src]));r['review']['date']='2026-09-28'
  r['review']['note']+=' '+summary
  decision='different_event_context'
  source_date='2025-08-26'
 else:
  if n in confirmed:
   code,attr,summary,src,source_date=confirmed[n];decision='aligned_with_additional_context';access='partial' if n==143 else 'full'
  else:
   code='ai_transition';attr='reported_inference';src=tracker;source_date=None;access='full';decision='tracker_label_retained'
   summary='Layoffs.fyi classifies this specific event as AI-related. Retained as an attributed general AI link under the tracker-first policy; the precise mechanism in its explanation has not been independently corroborated. This is a tracker classification, not company confirmation or verified task replacement.'
   if n==64:summary+=' Later reporting on the visuals team may concern a different round; that timing remains unresolved, so no substitution mechanism is assigned to this February reduction reported in March.'
   if n==193:summary+=' The linked article explicitly leaves the causal link uncertain; retain that uncertainty alongside the tracker label.'
   if n==196:summary+=' The source separates performance-related exits from new AI hiring; the broader AI link is attributed to the tracker, not the company.'
  r['causes'].append(code)
  r['cause_details'][code]=dict(summary=summary,attribution=attr,scope='announced_plan' if n==210 else 'event',source_url=src,specificity='generic' if code=='ai_transition' else 'concrete',evidence_access=access)
  r['review']['sources']=list(dict.fromkeys(r['review']['sources']+[tracker,t['tracker_source'],src]));r['review']['date']='2026-09-28'
  r['review']['note']+=' '+summary
  r['reason']=' '.join(v['summary'] for v in r['cause_details'].values())
  r['cause_status']='specified' if any(v['specificity']=='concrete' for v in r['cause_details'].values()) else 'generic'
 r['tracker_review']=dict(date='2026-09-28',decision=decision,note=summary,source_url=src,source_publication_date=source_date,tracker_snapshot='research/ai-tracker-comparison/layoffs-fyi-ai-2026-09-28.json')
 l.update(decision=decision,note=summary,sources=r['review']['sources'],after_causes=r['causes'],source_review='targeted_followup' if n in confirmed or n==197 else 'tracker_classification_retained_with_unresolved_detail')
for t in rows:
 if t['status']=='ours_only_ai':
  l=byreview[t['record_id']];l['decision']='additional_attributed_ai_event';l['note']='La ausencia del listado del tracker no invalida la atribución conservada en cause_details. Se mantiene nuestra ampliación con la fuente y el alcance ya documentados; no se presupone que el tracker haya descartado el caso.'
changes=[dict(before=b,after=a) for b,a in zip(old,data) if b!=a]
A.write_text(json.dumps(dict(date='2026-09-28',method='Tracker labels are the baseline; access gaps or absent company confirmation do not remove an attribution. Keep additional event-linked attributions and override only documented event/context errors. Twelve added general AI links remain attributed to the tracker alone; seven have added context. Verily remains an exception for a different event.',events=changes),ensure_ascii=False,indent=2)+'\n')
(P/'pre-baseline-summary.json').write_text((P/'summary.json').read_text())
(R/'2026-categorized.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(P/'consistency-review.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
with (R/'2026-categorized.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in data for k in r)));w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in data)
print('Aligned 19 AI labels; retained Verily event-scope exception; preserved 16 additions outside tracker.')
