"""Recover dated workforce series; numeric observations retain a per-company source URL."""
import requests,json,concurrent.futures,time
from pathlib import Path
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
# Company mappings, including delisted companies; mappings do not assert current listing status.
raw='''Angi:angi
FormFactor:form
MercadoLibre:meli
Meta:meta
Playtika:pltk
Ericsson:eric
Autodesk:adsk
Shopify:shop
Expedia:expe
Pinterest:pins
ASML:asml
Amazon:amzn
Gloo:gloo
Peloton:pton
Zillow:z
Smartsheet:smar
Workday:wday
Salesforce:crm
Dayforce:day
Lucid Motors:lcid
DraftKings:dkng
TrueCar:true
WiseTech:quote/asx/WTC
C3.ai:ai
Deliveroo:quote/lon/ROO
Block:xyz
Ocado:quote/lon/OCDO
eBay:ebay
MicroVision:mvis
Atlassian:team
Stone:stne
Snowflake:snow
Spotify:spot
OpenText:otex
Oracle:orcl
Sonos:sono
MARA:mara
GoPro:gpro
IAC:iac
Life360:lif
Nayax:nyax
Snap:snap
Taboola:tbla
Shutterfly:sfly
Coinbase:coin
Freshworks:frsh
PayPal:pypl
reAlpha:aire
Bill.com:bill
Cloudflare:net
Truecaller:quote/sto/TRUE.B
Upwork:upwk
ZoomInfo:g tm
Cisco:csco
Jumia:jmia
Gambling.com Group:gamb
Intuit:intu
Wix:wix
GitLab:gtlb
Robinhood:hood
Uber:uber
eToro:etor
ADP:adp
BitGo:btgo
Elastic:estc
Rackspace:rxt
Rivian:rivn
ServiceNow:now
Opendoor:open
Veritone:veri
Paytm:quote/nse/PAYTM
Manhattan Associates:manh
SentinelOne:s
Amdocs:dox
NetApp:ntap
Groupon:grpn
Trend Micro:quote/tyo/4704
Qt Company:quote/hel/QTCOM
Qualcomm:qcom
Xero:quote/asx/XRO
Lastminute:quote/swx/LMN
Gemini:gem i
Informatica:infa
Vimeo:vmeo
Cars.com:cars
Eventbrite:eb
Cyberark:cybr
Verint Systems:vrnt'''
mappings=dict(line.split(':',1) for line in raw.splitlines());mappings={k:v.replace(' ','') for k,v in mappings.items()}
D=json.loads((ROOT/'report/records.json').read_text());groups={}
for r in D:groups.setdefault(r['company'],[]).append(r)
(P/'screening.json').write_text(json.dumps([{'company':c,'record_ids':[r['record_id'] for r in rs],'ai_mechanism':any(t.startswith('ai_') for r in rs for t in r['causes']),'causes':sorted({t for r in rs for t in r['causes']}),'series_url':('https://stockanalysis.com/'+(mappings[c] if '/' in mappings[c] else 'stocks/'+mappings[c])+'/employees/') if c in mappings else None,'screen_status':'candidate_historical_public_reporting' if c in mappings else 'no_standalone_listed_series_mapped','note':'Subsidiary workforce is not replaced by parent-company headcount.'} for c,rs in groups.items()],indent=2))
screen=json.loads((P/'screening.json').read_text())
def fetch(r):
 url=r['series_url'];dest=P/'sources'/(url.split('stockanalysis.com/')[1].replace('/','_')+'.json');dest.parent.mkdir(exist_ok=True)
 if dest.exists():return json.loads(dest.read_text())
 try:
  response=requests.get(url,timeout=18);soup=BeautifulSoup(response.text,'html.parser');rows=[]
  for table in soup.select('table'):
   if 'Employees' not in table.get_text():continue
   for tr in table.select('tbody tr'):
    cells=[c.get_text(' ',strip=True) for c in tr.select('td')]
    if len(cells)>=2:rows.append(cells[:2])
  result={'company':r['company'],'source_url':url,'retrieved':'2026-09-17','http_status':response.status_code,'title':soup.title.get_text() if soup.title else None,'rows':rows,'source_note':'Secondary compilation by Stock Analysis; see primary checks separately.'}
 except Exception as e:result={'company':r['company'],'source_url':url,'rows':[],'error':str(e)}
 dest.write_text(json.dumps(result,indent=2));return result
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 results=list(ex.map(fetch,[r for r in screen if r['series_url']]))
(P/'recovered-series.json').write_text(json.dumps(results,indent=2))
print('Attempted',len(results),'recovered',sum(bool(r['rows']) for r in results))
for r in results:
 vals=[x for x in r['rows'] if any(y in x[0] for y in ['2019','2022','2025'])]
 print(r['company'],r.get('http_status'), vals or 'MISSING')
