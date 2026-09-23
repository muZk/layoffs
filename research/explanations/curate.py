"""Manual adjudications; generic explanations remain attributed causes, never verified effects."""
import json,csv,copy,collections
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
base=P/'baseline.json'
if not base.exists():base.write_bytes((ROOT/'2026-categorized.json').read_bytes())
B=json.loads(base.read_text());D=copy.deepcopy(B);R={int(r['record_id'].split('-')[-1]):r for r in D}
N={'organizational_realignment':['Organizational realignment','Reorganización general'],'strategic_priorities':['Strategic priorities','Prioridades estratégicas'],'operational_efficiency':['Efficiency and agility','Eficiencia y agilidad'],'market_conditions':['Economic / market conditions','Condiciones económicas y de mercado'],'ai_transition':['AI transition (unspecified mechanism)','Transición con IA (sin mecanismo concreto)']}
(P/'taxonomy.json').write_text(json.dumps(N,ensure_ascii=False,indent=2)+'\n')
for r in D:
 for e in r['cause_details'].values():e['specificity']='concrete'
reviewed=[r for r in D if r['record_type']=='announcement' and '2026-01-01'<=r['date']<'2026-07-01' and r['cause_status']=='unspecified']
assert len(reviewed)==65
for r in reviewed:r['explanation_review']={'date':'2026-09-17','outcome':'no_explanation_identified','note':'No event-specific attributed reason identified in reviewed material. Context alone is not a cause; this does not assert that no explanation exists elsewhere.'}
def add(n,key,summary,attribution='company_stated',url=None,access='full',specificity='generic'):
 r=R[n];u=url or (r.get('source_used') or r['source_url'])
 if u not in r['review']['sources']:r['review']['sources'].append(u)
 r['causes'].append(key);r['cause_details'][key]={'summary':summary,'attribution':attribution,'scope':'event','source_url':u,'specificity':specificity,'evidence_access':access}
 r['explanation_review']['outcome']='concrete' if any(e['specificity']=='concrete' for e in r['cause_details'].values()) else 'generic'
 r['explanation_review']['note']='Event-specific attributed explanation retained at its stated level of detail. Generic language does not establish a concrete operating mechanism or verified causal effect.'
 r['cause_status']='specified' if r['explanation_review']['outcome']=='concrete' else 'generic'
# Each entry was read against cached source bodies, retrieved pages, or explicitly retained review evidence.
add(11,'organizational_realignment','Company links the reduction to aligning its organizational structure with business needs and long-term growth.')
add(12,'strategic_priorities','Company says the cuts concentrate capabilities and resources on customer priorities and areas with greater growth potential.')
add(23,'operational_efficiency','Company describes targeted streamlining in two units after reviewing operations and internal processes.')
add(28,'operational_efficiency','Company attributes the changes to greater agility, simpler work and faster decisions.',url='https://media.kiwi.com/company-news/kiwi-com-update/')
add(35,'strategic_priorities','Company says organizational changes align resources with long-term business priorities.')
add(36,'strategic_priorities','Company links the reduction to aligning resources with its highest priorities.',url='https://www.theregister.com/2026/02/04/workday_layoffs_400_jobs/')
add(40,'operational_efficiency','Company says smaller, more agile teams will accelerate decisions and execution.',url='https://cosmeticsbusiness.com/glossier-to-cut-more-than-50-jobs')
add(49,'strategic_priorities','Company says teams are being reorganized around its highest priorities and investment areas.')
add(56,'organizational_consolidation','Company identifies areas of duplication among the criteria for the current cuts.',url='https://www.cnbc.com/2026/02/26/ebay-layoffs-800-workforce.html',specificity='concrete')
add(60,'organizational_realignment','Company describes a regular organizational review to position teams to innovate and deliver for customers.',url='https://finance.yahoo.com/news/amazon-cuts-more-jobs-time-212928090.html')
add(64,'market_conditions','Company reported economic reasons for the layoffs to the provincial government; the reason is not further specified.')
add(69,'market_conditions','Company connects the restructuring to its review of market conditions and evolving business needs.')
add(69,'strategic_priorities','Company says the restructuring aligns resources with product development, customer experience and sustainable growth.')
stone='https://jovempan.com.br/economia/macroeconomia/stone-faz-demissao-em-massa-e-desliga-cerca-de-400-funcionarios/'
add(70,'operational_efficiency','Company describes structural adjustments as part of simplification and efficiency efforts.',url=stone)
add(70,'ai_transition','An unnamed source says progress in AI initiatives contributed to the decision; no concrete mechanism is given.','press_reported',stone)
add(74,'strategic_priorities','Company attributes targeted cuts to alignment with its long-term strategy.')
add(78,'strategic_priorities','Company explains the cuts through organizational alignment with strategic priorities and long-term growth.')
add(80,'organizational_realignment','Company says team restructurings are intended to help achieve their goals.',url='https://techcrunch.com/2026/03/25/meta-is-cutting-several-hundred-jobs/')
add(94,'organizational_realignment','An anonymous account describes reorganization and a change of focus as the reason communicated for the cuts. This is not a verified company statement.','press_reported')
add(95,'ai_transition','CEO connects the cuts to becoming a leaner, AI-centered organization, without naming affected tasks.')
add(102,'organizational_realignment','Company says eOS is restructuring to align with technology developments, signed agreements and anticipated customers.')
add(103,'organizational_realignment','New leadership says cuts follow its review after the acquisition; no duplicate-role or savings mechanism is attributed.',url='https://www.marketscreener.com/news/bending-spoons-cuts-eventbrite-staff-rolls-out-product-changes-after-takeover-ce7e50dedf8df62c')
add(106,'organizational_realignment','Company describes ongoing workforce adjustments in response to market developments and customer needs.')
add(111,'ai_transition','Company includes AI-driven technological changes among market shifts motivating the restructuring.')
add(111,'market_conditions','Company also cites changing customer expectations and software competition as reasons for the restructuring.')
add(117,'ai_transition','Company frames the cuts around technology change and greater use of AI for operational efficiency; affected tasks are not specified.')
add(117,'operational_efficiency','Company describes internal streamlining and optimization of how it works.')
add(120,'strategic_priorities','Company links adjustments to core activities, resource allocation and technological focus. AI product development alone is not a workforce mechanism.')
add(141,'ai_transition','Company attributes cuts broadly to increased AI adoption across products and operations, without detailing which work changes.')
add(147,'ai_transition','Company attributes role adjustments to preparing for the AI era, without specifying an operating mechanism.')
add(149,'organizational_realignment','Company describes regular business planning intended to position it for future success.',url='https://www.hcamag.com/us/news/general/linkedin-cuts-5-of-staff-despite-record-revenue-reuters-reports/575160')
add(152,'ai_transition','CEO describes a transition to an AI-native company in the internal communication about the cuts.')
add(152,'strategic_priorities','Company says it is aligning its team with current business priorities.')
add(160,'organizational_consolidation','CEO links the cuts to flatter organizational structures and avoiding a heavily layered organization.',specificity='concrete')
add(168,'strategic_priorities','Company frames the cuts as redirecting resources toward cloud computing, sales and product development.',url='https://finance.yahoo.com/technology/ai/articles/cary-sas-cuts-300-positions-133919519.html')
add(169,'organizational_realignment','Employee accounts describe a marketing reorganization; no company rationale is available.','worker_reported',access='prior_review')
add(172,'ai_transition','Company says broader adoption of AI changes its investment priorities and team needs; the concrete staffing mechanism is unspecified.')
add(178,'operational_efficiency','Company says its role review seeks a focused, efficient organization aligned with current business needs.',url='https://production.humanresourcesonline.net/lazada-to-undertake-workforce-reduction-across-southeast-asia-amid-organisational-review')
add(182,'operational_efficiency','Company says a leaner organization will allow greater focus and flexibility following its review.')
add(184,'ai_transition','CEO presents the cuts as part of an AI push and plans AI training for remaining staff; displaced work is not identified.')
add(191,'operational_efficiency','Company attributes the changes to stronger focus, simpler decisions and faster product delivery.')
add(193,'organizational_realignment','Company describes regular review and adjustment of staffing needs; the report explicitly leaves an AI connection unclear.')
add(200,'strategic_priorities','Company email links changes in roles and teams to its next stage of strategy and operating priorities.')
add(202,'operational_efficiency','Company says the changes seek agility, focus and execution of its long-term strategy.')
add(202,'market_conditions','Laid-off employees attribute the cuts partly to prediction-market competition and economic uncertainty.','worker_reported')
add(202,'ai_transition','Laid-off employees identify greater emphasis on AI among the reasons they believe led to the cuts; no concrete staffing mechanism is specified.','worker_reported')
add(206,'ai_transition','Company links its workforce adjustment to AI-related changes in how work is conducted, without specifying the tasks or roles transformed.')
add(208,'operational_efficiency','Company filing describes general efficiency and investment priorities without identifying an operating mechanism.',url='https://ir.manh.com/static-files/88023415-72b4-44d1-abb5-d995fcfd2fc0')
add(214,'organizational_realignment','Company says its new leadership is redesigning its operating model, while withholding specific details.')
add(220,'ai_transition','Founder attributes workforce adjustments to a transition toward AI-first software development and operations.')
add(228,'market_conditions','Foundation attributes the reduction to macroeconomic uncertainty and the broader crypto-market downturn.')
add(229,'strategic_pivot','CEO explicitly says the company will stop workstreams and do fewer things, rather than redistribute the same workload across fewer staff.',specificity='concrete')
R[56]['review']['note']='Company statement identifies duplication among the current cut criteria. The Depop acquisition is separate context, not the basis for this classification.'
R[160]['review']['note']='CEO describes flattening the organization. Frontier-technology language does not by itself specify an AI mechanism; earlier growth does not establish overhiring.'
R[229]['review']['note']='CEO describes stopping workstreams rather than distributing the same work among fewer staff. This supports a strategic narrowing of activities; financial pressure is explicitly denied.'
# Avoid a second AI label for the same claim after promoting it into attributed causes.
for r in reviewed:
 if 'ai_transition' in r['causes']:r['context']=[c for c in r['context'] if c['kind']!='ai_link_unspecified']
 if r['causes']:
  r['review']['note']+=' Explanation review: attributed reasons are recorded below with explicit specificity.'
  r['reason']=' '.join(('Generic attributed reason: ' if d['specificity']=='generic' else 'Concrete attributed mechanism: ')+d['summary'] for d in r['cause_details'].values())
ledger=[{'record_id':r['record_id'],'company':r['company'],'date':r['date'],'outcome':r['explanation_review']['outcome'],'causes':r['causes'],'details':r['cause_details'],'note':r['explanation_review']['note'],'sources':r['review']['sources']} for r in reviewed]
(P/'review.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
(ROOT/'coverage/explanations-followup-2026-09-17.json').write_text(json.dumps({'reviewed':'2026-09-17','method':'manual review of all 65 source-reviewed H1 announcements previously unspecified; preserve attribution and distinguish generic reasons from concrete mechanisms','events':[{'before':b,'after':a} for b,a in zip(B,D) if b!=a]},ensure_ascii=False,indent=2)+'\n')
(ROOT/'2026-categorized.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
with (ROOT/'2026-categorized.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in D for k in r)));w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()} for r in D)
print(collections.Counter(r['explanation_review']['outcome'] for r in reviewed))
print(collections.Counter(c for r in reviewed for c in r['causes']))
