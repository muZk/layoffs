"""Cache public source bodies for a manually reviewed, event-specific extraction."""
import json,hashlib,concurrent.futures,io
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent/'sources';OUT.mkdir(exist_ok=True)
def fetch(url):
 p=OUT/(hashlib.sha256(url.encode()).hexdigest()[:20]+'.json')
 if p.exists():return
 out={'url':url}
 try:
  r=requests.get(url,timeout=22,headers={'User-Agent':'Mozilla/5.0'});out['http_status']=r.status_code;r.raise_for_status()
  if 'pdf' in r.headers.get('content-type',''):text='\n'.join(x.extract_text() or '' for x in PdfReader(io.BytesIO(r.content)).pages)
  else:
   s=BeautifulSoup(r.content,'html.parser')
   for x in s(['script','style','nav','footer','header']):x.decompose()
   article=s.find('article') or s.find('main') or s
   text=article.get_text(' ',strip=True)
  out['text']=text
 except Exception as e:out['error']=str(e)
 p.write_text(json.dumps(out,ensure_ascii=False))
if __name__=='__main__':
 data=json.loads((ROOT/'report/records.json').read_text())
 urls=set(u for r in data for u in r['review']['sources'] if u.startswith('http'))
 with concurrent.futures.ThreadPoolExecutor(max_workers=14) as ex:list(ex.map(fetch,sorted(urls)))
 print('Cached',len(urls),'URLs')
