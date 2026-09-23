"""Reproducible, manually adjudicated source recovery and affected-work extraction.
No function is inferred from industry, AI use, hiring destinations or keywords.
"""
import json,copy,csv,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];P=Path(__file__).parent
BASE=P/'baseline.json'
if not BASE.exists():BASE.write_text((ROOT/'2026-categorized.json').read_text())
D=json.loads(BASE.read_text());before=copy.deepcopy(D);R={int(r['record_id'].split('-')[-1]):r for r in D}
NAMES={'engineering':'Ingeniería e I+D','product_design':'Producto y diseño','data':'Datos y analítica','it_security':'TI y ciberseguridad','sales':'Ventas y alianzas','marketing':'Marketing','support':'Soporte y atención al cliente','people':'RR. HH. y selección','corporate':'Administración, finanzas y legal','operations':'Operaciones y prestación de servicios','content':'Contenido y docencia','manufacturing':'Producción y fabricación'}
(P/'taxonomy.json').write_text(json.dumps(NAMES,ensure_ascii=False,indent=2)+'\n')
def source(i):return R[i].get('source_used') or R[i]['source_url']
def recover(i,u,note,causes=None):
 r=R[i];r['source_used']=u;r['review']['sources']=list(dict.fromkeys(r['review']['sources']+[u]));r['review']['status']='source_reviewed';r['review']['date']='2026-09-17';r['review']['note']=r['reason']=note
 r['review']['issues']=[s for s in r['review']['issues'] if s not in ['limited_source_access','original_source_unavailable','source_unavailable','headcount_unverified']]
 if causes is not None:
  r['causes']=list(causes);r['cause_details']={c:{'summary':v[0],'attribution':v[1] if len(v)>1 else 'company_stated','scope':'event','source_url':u} for c,v in causes.items()}
GLOO='https://investors.gloo.com/static-files/6a6cee16-3074-4288-83a4-ce6487c4267f'
recover(27,GLOO,'Investor letter directly links targeted workforce reductions to acquisition efficiencies, AI workflows and removing duplication. IT/marketing savings are described, but the letter does not identify the terminated occupations.',{
 'ai_productivity':['CEO links workforce reductions to AI-enabled operating efficiencies.'],
 'm_and_a':['CEO links the reduction to operating efficiencies arising from acquisitions.'],
 'organizational_consolidation':['The letter says targeted reductions eliminate duplication.'],
 'cost_cutting':['The cuts and resource reallocation support the stated profitability target.']})
recover(40,source(40),'Full alternative report includes company confirmation of 54 cuts. Smaller teams and a leadership reset do not specify which work disappears or a concrete causal mechanism.',{});R[40]['laid_off']=54
recover(57,source(57),'Full report recovered: CTO attributes the February reduction from 18 to 10 to AI efficiency and cost alignment; former staff separately report support automation making roles redundant.',{
 'cost_cutting':['Company links restructuring to aligning operating costs with revenue.'],
 'ai_productivity':['CTO attributes the reduction from 18 to 10 employees to an AI-driven efficiency shift.'],
 'ai_substitution':['Former employees say Martha AI handles first-line enquiries and automation made roles redundant.','worker_reported']});R[57]['laid_off']=8
recover(66,'https://wealthtechtoday.com/2026/03/09/investcloud-layoffs-2026/','Direct CEO interview and reviewed staff communication connect Digital Wealth cuts to AI productivity, fewer operating centers and a move from bespoke implementations to standardized products.',{
 'ai_productivity':['CEO attributes the reduction partly to AI-driven productivity and faster delivery.'],
 'organizational_consolidation':['Digital Wealth operations are being concentrated into fewer centers.'],
 'strategic_pivot':['CEO describes replacing bespoke client solutions with repeatable, standardized products.']})
recover(76,'https://finance.yahoo.com/markets/stocks/articles/spotify-layoffs-podcast-group-cut-200111630.html','Full syndicated Variety report identifies the affected podcast group and editorial staff. Bloomberg separately reports fewer management layers; the mechanism is attributed to reporting, not a company admission.')
R[76]['review']['sources'].append('https://news.bloomberglaw.com/human-resources-news/spotify-lays-off-15-people-about-3-of-podcasting-staff')
R[76]['cause_details']={'organizational_consolidation':{'summary':'Bloomberg reports the podcast reorganization removes management layers.','attribution':'press_reported','scope':'event','source_url':R[76]['review']['sources'][-1]}};R[76]['causes']=['organizational_consolidation']
recover(118,'https://www.golem.de/news/e-paper-tablets-remarkable-soll-40-prozent-der-mitarbeiter-entlassen-2604-207992.html','Golem reproduces the chairman’s explanation of weaker demand and falling revenue, and obtained a fresh company response about the difficult environment and component costs.',{'demand_decline':['Chairman attributes the restructuring to weaker demand and declining revenue.']})
recover(145,source(145),'Full article recovered. Company confirms 58 fixed-term contracts were not renewed in engineering, product and data. It does not answer the questions about an AI-related motive; the explanation remains nonspecific.',{})
R[145]['headcount_scope']='contract_nonrenewals';R[145]['review']['issues'].append('fixed_term_contract_nonrenewals')
recover(152,source(152),'Full original report recovered. CEO describes an AI-native transition, but neither the statement nor reporting identifies what work is automated or how AI requires these particular cuts.',{})
recover(167,source(167),'State archive lists Automatic Data Processing, Roseland, 76 affected workers, posted in June and effective September 25. It gives no functions or causal explanation.',{})
R[167]['laid_off']=76;R[167]['headcount_scope']='announced_plan'
recover(168,'https://finance.yahoo.com/technology/ai/articles/cary-sas-cuts-300-positions-133919519.html','Full syndicated News & Observer report recovered. Company describes resource priorities, including cloud, sales and product development; these are investment destinations, not identified occupations cut.',{})
recover(170,source(170),'Full original report recovered. Sources connect the shutdown to funding and infrastructure-cost pressure, with failed acquisition discussions. Employees were asked to leave as operations wound down.',{'shutdown':['Employees were told to leave as the company wound down operations.','press_reported'],'financial_distress':['Sources attribute closure to funding shortfalls, high infrastructure costs and failed acquisition talks.','press_reported']})
recover(173,'https://finance.yahoo.com/markets/stocks/articles/market-chatter-sonos-cuts-3-195105247.html','MT Newswires reproduces the company response confirming removal of layers and identifies product, design and user-experience teams. April marketing cuts are a separate event.',{'organizational_consolidation':['Company says the cuts remove layers and streamline teams.']})
recover(178,'https://production.humanresourcesonline.net/lazada-to-undertake-workforce-reduction-across-southeast-asia-amid-organisational-review','Full report includes a direct company response but no concrete mechanism or affected functions. It also relays a report that cuts are unrelated to AI; the original speaker is not identified.',{})
R[178]['context'].append({'kind':'reported_ai_nonconnection','summary':'HRO relays Business Times reporting that the cuts are not related to AI initiatives; this is not recorded as a company denial without a named source.','source_url':source(178)})
recover(181,source(181),'Updated original report contradicts the tracker’s 70% figure: CEO says approximately 30%, while anonymous sources estimate 100 departures from a 150-person team. Keep both accounts, not a single settled count.',{
 'market_exit':['CEO confirms withdrawal from selected markets to focus on northern India.'],
 'unit_closure':['Reporting and store operators identify closures in the offline store network.','press_reported'],
 'demand_decline':['Sources attribute the reduction to missed growth expectations and weaker commercial-vehicle demand.','press_reported']})
R[181]['laid_off']=None;R[181]['pct']=None;R[181]['headcount_scope']='disputed_event_size';R[181]['review']['issues'].append('conflicting_headcount_accounts')
R[181]['headcount_accounts']=[{'value':100,'pct':0.70,'attribution':'press_reported','source_url':source(181),'note':'Anonymous sources estimate roughly 100 departures; approximate prior workforce 150.'},{'value':None,'pct':0.30,'attribution':'company_stated','source_url':source(181),'note':'CEO disputes reported scale and says remaining workforce exceeds 200.'}]
recover(189,'https://www.sec.gov/Archives/edgar/data/1810019/000181001926000058/rxt-20260610.htm','June 16 filing links a 15% reduction to legacy Public Cloud service delivery, resource reallocation toward enterprise AI and expected annual savings. It does not say all affected workers are replaced by AI.',{
 'ai_investment_reallocation':['Filing explicitly reallocates resources from legacy service delivery to enterprise AI.'],
 'strategic_pivot':['Company deemphasizes legacy Public Cloud service delivery as its operating model shifts.'],
 'cost_cutting':['Plan is expected to save $75–85 million annually, with substantial reinvestment.']})
R[189]['headcount_scope']='announced_plan'
recover(210,'https://www.aol.com/articles/credit-karma-lays-off-hundreds-153300000.html','Full syndicated report lists occupations in the WARN notice and places the 117 Credit Karma cuts within Intuit’s broader 3,000-person plan. Parent-level commentary is not treated as a separately verified subsidiary mechanism.',{})
R[210]['review']['issues'].append('overlap_with_intuit_may_plan');R[210]['related_records']=[{'record_id':'layoff-2026-155','relationship':'reported_subset','source_url':source(210)}]
R[155]['review']['issues'].append('includes_credit_karma_notice');R[155]['related_records']=[{'record_id':'layoff-2026-210','relationship':'reported_parent_plan','source_url':source(210)}];R[155]['review']['sources'].append(source(210))
recover(215,'https://www.linkedin.com/posts/liranbelenzon_the-company-were-building-at-benchsci-activity-7465420965041139714-rYRF','CEO statement directly connects the 30% reduction to redesigning teams around human–agent collaboration. Listed workflows are not an explicit inventory of terminated roles.',{'ai_work_redesign':['CEO links the reduction to a model in which scoped AI agents and employees operate as one team.']})
recover(218,'https://www.nrn.com/restaurant-technology/pizza-robot-company-picnic-shuts-down','Restaurant Business reporting confirms closure and an assignment of assets for creditor repayment on May 11. The public announcement is in May; functions are not broken down.',{'shutdown':['Company shut down and assets were assigned for liquidation.','press_reported'],'financial_distress':['Assets were transferred to an assignee to liquidate and repay creditors.','press_reported']})
recover(223,'https://2digital.news/zondacrypto-chief-disappears-employees-receive-termination-emails-as-company-descends-into-chaos/','Alternative report describes employee terminations amid payment disruption. Financial and legal turmoil are reported context, but the causal account for the specific workforce action remains nonspecific.',{})
recover(225,source(225),'Original article recovered, but its April 17 update combines April 2 and April 15 notices: headline/caption and body totals conflict. Functions are reported; a single event headcount cannot be reconciled.',{})
R[225]['laid_off']=None;R[225]['headcount_scope']='multi_round_period';R[225]['review']['issues'].append('updated_article_combines_notices')
R[225]['headcount_accounts']=[{'value':104,'attribution':'press_reported','source_url':source(225),'note':'Updated body combines April 2 and April 15 notices; original caption says 66; tracker value was 60. Do not assign the combined total to one April 9 event.'}]
recover(234,'https://yourstory.com/2026/01/elevation-capital-backed-ai-stylist-alle-shuts-shop','Full reporting of founder’s announcement confirms closure after unsuccessful product-market-fit attempts. The public announcement is January 2026, but the decision was made in October 2025.',{'shutdown':['Founder announces the business closed after repeated unsuccessful pivots.']})
R[234]['review']['issues'].append('closure_decision_in_2025');R[234]['context'].append({'kind':'event_timing','summary':'Founder says the closure decision was made in October 2025; January 2026 is the public reporting date.','source_url':source(234)})
# Do not upgrade incomplete source access merely because a headline/search extract is useful.
R[143]['review']['note']=R[143]['reason']='Indexed original report identifies development and support relocation to Budapest. Full page access remains unavailable; retrieved extracts add function detail but do not establish the complete causal account.'
R[166]['review']['note']=R[166]['reason']='Indexed original reporting recovers a company statement about market dynamics and priorities. No specific function or mechanism is established; full article access remains incomplete.'
# A field exists on every retained announcement; missing detail is a visible result.
E=[r for r in D if '2026-01-01'<=r['date']<'2026-07-01' and r['record_type']=='announcement']
for r in E:
 r['affected_work']={'status':'not_identified','functions':[],'details':[],'units':[],'levels':[], 'review':{'date':'2026-09-17','method':'manual_review_of_retrieved_sources_and_existing_evidence','note':'No explicit affected occupation identified in the material reviewed. This does not mean none were affected or that no other source can identify them.','sources':list(r['review']['sources'])}}
def work(i,functions,note,attribution='press_reported',u=None,access='full',levels=None):
 r=R[i];u=u or source(i);w=r['affected_work'];w['status']='identified';w['functions']=functions.split();w['details'].append({'functions':functions.split(),'summary':note,'attribution':attribution,'source_url':u,'evidence_access':access});w['review']['note']='Functions explicitly identified for this event; the list is not necessarily exhaustive.';w['levels']=levels or []
 assert set(w['functions'])<=set(NAMES)
 if u not in w['review']['sources']:w['review']['sources'].append(u)
def unit(i,name,note,u=None):
 w=R[i]['affected_work'];u=u or source(i);w['units'].append({'name':name,'summary':note,'source_url':u});w['status']='identified' if w['functions'] else 'unit_only';w['review']['note']='A business unit or broad scope is named; this does not supply a complete occupation breakdown.' if not w['functions'] else w['review']['note']
work(5,'sales','Company identifies go-to-market roles and customer segmentation/account coverage.','company_stated')
work(6,'engineering','The existing event review identifies three of four engineering staff, not three quarters of all staff.','company_stated',access='prior_review')
work(7,'manufacturing','Manufacturing facilities and their workers are affected; some may be retained rather than laid off.','company_stated',u=R[7]['cause_details']['organizational_consolidation']['source_url'],access='prior_review')
work(8,'product_design content','The corrected report identifies UX writing/content roles being integrated with design.','press_reported',access='prior_review')
unit(9,'Reality Labs / VR','Cuts concern the VR business; augmented-reality staff are reported outside the affected scope.')
work(15,'sales engineering','CEO identifies reductions in sales and development divisions.','company_stated')
work(18,'sales','Employee message says most impact falls on customer-facing sales teams.','company_stated')
work(19,'sales','Existing source review identifies partnership roles in the January event.','press_reported',access='prior_review')
unit(20,'Loss-making units','Employees describe closing loss-making units; no occupation inventory recovered.')
work(25,'engineering it_security','Proposed changes affect Technology and IT/Data, especially leadership; new engineering roles are also planned.','company_stated',levels=['leadership'])
work(29,'engineering','Report identifies engineers on technology and enterprise efforts.')
work(34,'engineering','Company closes the local R&D center, retaining sales/business roles.','company_stated')
work(36,'operations','Non-revenue-generating Global Customer Operations roles are identified. Do not assume all are support agents.')
work(37,'marketing product_design data','Report identifies marketing, product management and data analytics roles.')
unit(37,'Agentforce / Heroku','Affected units also include Agentforce and Heroku; unit names are not additional occupations.')
unit(38,'Consumer business','The cuts accompany the move away from the consumer business.')
work(42,'marketing sales','Most affected employees are described as relatively senior marketing and sales staff.',levels=['senior'])
work(43,'engineering','Report describes the reduced development organization and only a small remaining developer team.')
work(44,'engineering','Cuts concern the cloud division of Huawei’s Israeli development center.')
unit(44,'Cloud / Toga Networks','The specific development center and cloud division are identified.')
work(46,'content','Curriculum team producing interactive learning content was eliminated.','worker_reported')
work(47,'sales operations product_design marketing','Company explicitly names sales, operations, design and marketing in the multi-month reduction.','company_stated')
unit(48,'Salaried workforce','Hourly manufacturing, logistics and quality workers are expressly excluded; no positive occupation inventory recovered.')
work(49,'engineering people','Reporting cites employees in software engineering and recruitment who say they were laid off.','worker_reported')
work(51,'engineering product_design support','Company plan initially targets product/development and customer service, including e2open.','company_stated')
work(57,'product_design operations marketing support','Design, operations, marketing and support are reported; CTO confirms design, operations and support. This is the February eight-person round.')
work(61,'engineering','Original report explicitly identifies development employees.')
unit(66,'Digital Wealth','CEO identifies Digital Wealth as the affected division; APL and Private Markets are excluded.')
work(67,'engineering','Company spokesperson identifies more than 900 software R&D positions.','company_stated',u='https://www.theguardian.com/technology/2026/mar/12/atlassian-layoffs-software-technology-ai-push-mike-cannon-brookes-asx')
work(74,'content','Existing event review identifies technical-writing cuts without establishing AI replacement.','press_reported',access='prior_review')
work(76,'content','Variety identifies a staff writer and special-projects/editorial work among those eliminated.')
unit(76,'The Ringer / Spotify Studios','Most cuts fall in these podcast units.')
work(78,'support','Employee account says all support engineers for one product were terminated.','worker_reported')
work(89,'marketing','The April report identifies Sonos marketing cuts; separate from the June product/design round.')
work(94,'product_design engineering','Employee account identifies product and development as the main affected teams.','worker_reported')
work(98,'corporate','Filing describes the consolidation of corporate functions.','company_stated',access='prior_review')
work(102,'engineering','Sources identify development roles as the main target.')
work(112,'corporate','Report identifies shared SG&A functions. Their broad label is not split into unsupported sales/finance occupations.')
unit(112,'Poe','Poe-focused teams are also identified, without an occupation inventory.')
work(120,'marketing corporate','Original report identifies marketing and headquarters roles.')
work(121,'sales','Accessible title identifies revenue operations; normalized to commercial/sales operations, with limited source access.',access='partial')
work(123,'engineering','Report explicitly identifies developers among the affected staff.')
work(128,'sales engineering product_design marketing','Reporting names sales, product development and marketing, with affected systems and sales engineers.')
work(131,'marketing engineering product_design operations','Company names marketing, technology, product/design, real-estate and mortgage functions; the latter are grouped as operating services.','company_stated')
work(135,'engineering product_design','Reported cuts primarily affect engineering, product and design.')
work(140,'product_design content operations','Sources identify product, design, content, teaching and business operations; CUET/UPSC/judiciary are program areas.','worker_reported')
work(143,'engineering support','Indexed original report explicitly identifies development and support moving to Budapest.',access='partial')
unit(143,'Identity Manager','The affected product is Identity Manager.')
work(144,'engineering sales marketing','Reporting identifies R&D and downmarket sales/marketing cuts.')
work(145,'engineering product_design data','Company confirms non-renewal of 58 contracts in engineering, product and data.','company_stated')
work(149,'engineering product_design marketing','Report relays Reuters identification of engineering, product and marketing staff.')
work(169,'marketing','Affected employees identify a marketing reorganization.','worker_reported',access='prior_review')
work(173,'product_design','The June report identifies user experience, product and design; includes leadership positions.','press_reported',levels=['leadership'])
unit(181,'Offline store network','Store closures and a country-head departure are reported; shop-floor occupations are not individually identified.')
work(183,'manufacturing','Report connects this June reduction with ending a factory second shift; do not transfer exclusions from February.')
work(189,'operations','Filing identifies legacy service delivery, primarily in the Public Cloud unit.','company_stated')
unit(189,'Public Cloud','Public Cloud is the business unit, not an occupational category.')
work(191,'engineering data product_design','Reporting identifies Offering teams spanning product, technology, design and data; most affected held engineering/data roles.')
work(193,'engineering','Reporting identifies developer jobs.')
work(194,'operations','CEO identifies operating work being brought back to the United States.','company_stated')
work(199,'support operations','Company connects the reduction to lower need for internal customer support and deployment teams.','company_stated')
work(201,'engineering product_design operations','Original reporting names development, product and professional services.')
work(202,'engineering support sales','Sources identify software engineering, customer service and business development.')
work(204,'it_security','Original report title and corroborating reporting identify cybersecurity teams; complete original access remains limited.',access='partial')
unit(204,'Google Cloud / GTIG / Mandiant','Cybersecurity teams within Cloud are named in reporting.','https://stlawyers.ca/blog-news/google-cloud-job-cuts-june-2026/')
work(205,'people','Reporting and company memo identify the People division, including HR and recruitment.','company_stated')
work(209,'engineering product_design','Most affected employees are described as working in core software and product development.')
work(210,'engineering product_design corporate marketing it_security people content support','WARN-based reporting names engineering, product/design, legal/finance/procurement, marketing, security, talent acquisition, editorial and member success.',levels=['leadership','senior'])
work(217,'engineering product_design sales','Report identifies software engineering, product management and sales.')
work(221,'engineering','Report identifies all positions in the Sydney R&D/engineering team.')
unit(222,'Google GBike service','Accessible original reporting identifies the bike-service site; it does not establish whether workers are mechanics, drivers or other occupations.')
work(225,'it_security engineering marketing support','Updated article names IT, engineering, cybersecurity, marketing and customer service. Scope spans two April notices.',levels=['senior','leadership'])
work(229,'engineering operations','CEO describes departing staff as engineers and operators, among other builders.','company_stated')
work(233,'people corporate product_design','Accessible original caption names executives in HR, corporate development, product development, legal and procurement; full causal report remains restricted.',access='partial',levels=['leadership'])
unit(232,'2XKO development team','Game-development team is identified but not an occupational split between code, art, production and other work.')
# Preserve explanatory distinctions in unknown rows where an obvious but invalid inference is tempting.
for i,n in {
 27:'IT and marketing efficiencies are described, but terminated roles are not identified. Do not equate the savings functions with the occupations cut.',
 81:'Examples of staff using AI are not a list of laid-off occupations.',
 130:'Designers and writers are mentioned in a separate transfer to an external payroll provider; these are not confirmed layoffs in this round.',
 133:'Engineering, HR, finance and marketing are examples of AI use, not a verified list of affected functions.',
 155:'Removal of management layers and coordination-heavy roles does not identify an occupational function.',
 165:'Fewer management layers identify seniority/structure, not a specific occupation.',
 168:'Sales, cloud and product development are investment destinations, not established cut functions.',
 175:'Product strategy and agent-oriented investment do not supply an occupation inventory.',
 176:'Engineering reorganization is described, but the statement does not explicitly enumerate terminated engineering occupations.',
 215:'Engineering, operations and science describe where agents are used. The CEO does not explicitly identify the occupations eliminated.',
 234:'The public announcement is in 2026 but the closure decision was in 2025; no occupational breakdown is given.'
}.items():R[i]['affected_work']['review']['note']=n
for i in [155,165,176]:R[i]['affected_work']['levels']=['leadership']
# Every initially incomplete record has a documented recovery attempt and result.
initial={int(r['record_id'].split('-')[-1]):r for r in before if r['record_type']=='announcement' and r['date']<'2026-07-01' and r['review']['status']!='source_reviewed'}
recovery=[]
for i,old in initial.items():
 r=R[i]; recovered=r['review']['status']=='source_reviewed'
 recovery.append({'record_id':r['record_id'],'company':r['company'],'date':r['date'],'search_scope':f'{r["company"]}, {r["date"][:7]}: original source retry and event-specific alternative reporting/statements','original_source':old['source_url'],'reviewed_sources':list(dict.fromkeys(r['review']['sources']+r['affected_work']['review']['sources'])),'outcome':'source_recovered' if recovered else 'still_partial' if r['review']['status']=='partial' else 'no_event_source_recovered','note':r['review']['note'],'function_status':r['affected_work']['status']})
for r in D:r['cause_status']='specified' if r['causes'] else {'source_reviewed':'unspecified','partial':'unresolved','unavailable':'unavailable'}[r['review']['status']]
(P/'recovery-log.json').write_text(json.dumps(recovery,ensure_ascii=False,indent=2)+'\n')
(ROOT/'2026-categorized.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
with (ROOT/'2026-categorized.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in D for k in r)));w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()} for r in D)
audit={'date':'2026-09-17','scope':'37 incomplete source reviews and affected-work review for all 228 H1 announcement records','events':[{'before':a,'after':b} for a,b in zip(before,D) if a!=b]}
(ROOT/'coverage/functions-followup-2026-09-17.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print('Recovery',collections.Counter(x['outcome'] for x in recovery));print('Functions',collections.Counter(r['affected_work']['status'] for r in E));print('Tags',collections.Counter(f for r in E for f in r['affected_work']['functions']))
