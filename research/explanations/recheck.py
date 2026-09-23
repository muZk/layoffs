"""Recheck every remaining no-explanation record; preserve the preceding audit."""
import json,csv,copy
from pathlib import Path
P=Path(__file__).resolve().parent; ROOT=P.parents[1]
base=P/'recheck-baseline.json'
if not base.exists():base.write_bytes((ROOT/'2026-categorized.json').read_bytes())
B=json.loads(base.read_text());D=copy.deepcopy(B);R={int(r['record_id'].split('-')[-1]):r for r in D}
ids=[n for n,r in R.items() if r['cause_status']=='unspecified' and r['record_type']=='announcement' and r['date']<'2026-07-01'];assert len(ids)==20
notes={
10:'Original reporting confirms cuts and a pending SPAC transaction but gives no attributed reason. Funding concerns found in later coverage do not establish why this January round occurred.',
17:'January reporting confirms layoffs following the acquisition. The March leadership letter discusses the operating model, but does not explicitly attribute this January reduction to a particular reason. Acquisition timing alone is insufficient.',
42:'Reporting identifies sales/marketing cuts and leadership changes. IPO preparation refers to the preceding November round; acquisition talks do not establish the reason for February cuts.',
46:'The curriculum leader confirms the team was laid off. Reporting explicitly says Skillsoft did not give a detailed rationale. A secondary workplace summary links parent cost plans, but no event-specific primary link was recovered.',
93:'April WARN reporting confirms the local reduction without an attributed rationale. Ownership changes and the January cuts may overlap; neither establishes a separate April explanation.',
110:'The Q1 filing confirms the April workforce reduction in subsequent events. Product launches, parallel hiring and stock-price commentary do not provide a sufficiently attributed reason for these cuts.',
145:'Reporting contains a company explanation of contract expiry/nonrenewal, which describes how employment ended rather than why those roles were eliminated. Financing and AI investment remain context.',
167:'The New Jersey WARN archive and June 29 local reporting establish 76 planned exits. No event-specific reason recovered; ADP employment surveys and anonymous discussions cannot establish the cause of this notice.',
192:'June WARN-based coverage establishes 54 Santa Clara cuts. Later July notices and broad AI-product reporting do not establish a reason for this specific event.',
197:'June WARN-based reporting identifies the San Bruno reduction. Searches surfaced earlier Verily rounds and different company Veritone; these cannot explain this event.',
198:'The Register confirms the June notice and says Salesforce had not responded. Acquisitions, buybacks and earlier AI support cuts are context, not an attributed mechanism for the 86 positions.',
203:'June reporting and WARN summaries establish the reduction; no attributable event-specific rationale recovered in the additional search.',
225:'April San Diego reporting confirms cuts but reuses an older company statement. The 2024 explanation and broader quarterly results cannot be assigned to this round; the headcount discrepancy remains flagged.'}
extra={
17:['https://vimeo.com/blog/post/what-comes-next-vimeo','https://techcrunch.com/2026/01/22/vimeo-starts-layoffs-after-acquisition-by-bending-spoons/'],
46:['https://www.edtechinnovationhub.com/news/skillsoft-lays-off-entire-codecademy-curriculum-team-senior-leader-confirms','https://builtin.com/company/codecademy-skillsoft-company/faq/workplace-perception'],
93:['https://vimeo.com/blog/post/what-comes-next-vimeo','https://whatnow.com/new-york/local-news/new-york-based-video-platform-to-layoff-130-employees/'],
110:['https://www.sec.gov/Archives/edgar/data/1840502/000184050226000009/tbla-20260331.htm','https://en.globes.co.il/en/article-taboola-lays-off-5-of-workforce-1001540177'],
167:['https://finance.yahoo.com/economy/articles/more-200-layoffs-planned-tech-160244643.html'],
198:['https://www.theregister.com/saas/2026/06/09/salesforce-layoffs-hit-amid-m3ter-acquisition-and-stock-buyback/5253162']}
def add(n,key,summary,url,specificity='generic',attribution='company_stated',scope='event'):
 r=R[n];r['causes']=[key];r['cause_details']={key:dict(summary=summary,source_url=url,specificity=specificity,attribution=attribution,scope=scope,evidence_access='full')};r['cause_status']='specified' if specificity=='concrete' else 'generic';extra[n]=[url];notes[n]=summary
add(37,'ai_substitution','Forrester analyst Charlie Dai interprets this fresh round as AI/automation replacing workers. This is an external analyst inference, not a company admission or independently established displacement; the company response discusses support staffing over the preceding year.','https://www.cio.com/article/4130028/salesforce-lays-off-staffers-as-executive-leadership-churn-continues.html','concrete','reported_inference')
add(86,'organizational_realignment','The March termination email attributes role elimination to a broader organizational change following a review of business needs. It does not specify an AI mechanism.','https://www.moneycontrol.com/news/trends/full-text-of-the-email-oracle-sent-to-30-000-laid-off-employees-at-6-am-13876386.html')
add(91,'organizational_realignment','A Meta spokesperson explains the reported reductions through regular team restructuring to achieve organizational goals; no concrete operating mechanism is given.','https://www.sfchronicle.com/tech/article/meta-layoffs-silicon-valley-22186184.php')
add(201,'operational_efficiency','CTech frames the current cuts as an efficiency effort in its headline. The article supplies no company explanation or concrete mechanism; this is the publication’s attribution.','https://www.calcalistech.com/ctechnews/article/rkxkiagbgg',attribution='press_reported')
add(210,'organizational_consolidation','Intuit’s May 20 employee letter explicitly identifies elimination of overlapping TurboTax and Credit Karma roles following integration. Local reporting places this notice within that plan; it does not show that each of the 117 positions had the same rationale.','https://investors.intuit.com/sec-filings/all-sec-filings/content/0000896878-26-000024/fy26q3-ex9902.htm','concrete',scope='named_subsidiary_within_announced_plan')
add(217,'strategic_priorities','NetApp’s statement to CRN links the reduction to aligning investment and staffing with evolving customer priorities and growth opportunities. It does not specify which operating change removes these roles.','https://www.crn.com/news/storage/2026/netapp-layoffs-will-impact-77-in-california-amid-strategic-realignment')
add(223,'unit_closure','Termination-agreement templates reported by Polish media cite liquidation of employer Orion Software, a Zondacrypto group company. This supports closure of that employing entity, not a claim that the entire exchange formally entered bankruptcy.','https://www.bankier.pl/wiadomosc/To-oficjalny-koniec-Zondacrypto-Rozwiazane-umowy-oswiadczenie-prezesa-i-zarzuty-do-sledczych-9120791.html','concrete',scope='named_employing_entity')
ledger=[]
for n in ids:
 r=R[n];outcome={'specified':'concrete','generic':'generic','unspecified':'no_explanation_identified'}[r['cause_status']]
 r['explanation_review']={'date':'2026-09-17','outcome':outcome,'method':'individual_source_reread_and_alternative_source_search','note':notes[n]}
 for u in extra.get(n,[]):
  if u not in r['review']['sources']:r['review']['sources'].append(u)
 if r['causes']:
  r['reason']=notes[n];r['review']['note']=notes[n]+' Existing overlap, count and plan-scope caveats remain applicable.'
 ledger.append(dict(record_id=r['record_id'],company=r['company'],date=r['date'],outcome=outcome,causes=r['causes'],details=r['cause_details'],note=notes[n],sources=r['review']['sources'],search_scope='Company, announcement month, layoff rationale; original reporting and alternative coverage. Unsuccessful searches are not evidence that no explanation exists.'))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
save(P/'recheck-review.json',ledger);save(ROOT/'report/explanation-recheck.json',ledger)
save(ROOT/'coverage/explanation-recheck-2026-09-17.json',dict(reviewed='2026-09-17',method='Additional individual review and alternative-source searches for all 20 no-explanation records; preserve external inferences as such.',events=[dict(before=b,after=a) for b,a in zip(B,D) if b!=a]))
save(ROOT/'2026-categorized.json',D)
with (ROOT/'2026-categorized.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in D for k in r)));w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()} for r in D)
# Publish current classifications, retaining the preceding research ledger unchanged.
old=json.loads((P/'review.json').read_text());updated={r['record_id']:r for r in ledger}
save(ROOT/'report/explanation-review.json',[updated.get(r['record_id'],r) for r in old])
