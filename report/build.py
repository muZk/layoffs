"""Build the report and exportable figures from the reviewed dataset."""
import json,collections,html,re,shutil,textwrap,csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import markdown
P=Path(__file__).resolve().parent;ROOT=P.parent
import runpy
_brand=runpy.run_path(str(P/'chart_branding.py'))
source=ROOT/'2026-categorized.json' if (ROOT/'2026-categorized.json').exists() else P/'records.json'
D=json.loads(source.read_text());H=[r for r in D if '2026-01-01'<=r['date']<'2026-07-01'];E=[r for r in H if r['record_type']=='announcement']
PUBLIC=E
E=PUBLIC  # Narrative and explorer count all attributed reasons.
GENERIC=json.loads((ROOT/'research/explanations/taxonomy.json').read_text())
G=collections.Counter(r['cause_status'] for r in E)
GAPS=[('No explanation identified',G['unspecified']),('Evidence limited',G['unresolved']),('No causal source recovered',G['unavailable'])]
C=collections.Counter(c for r in E for c in r['causes'])
AI=['ai_productivity','ai_investment_reallocation','ai_work_redesign','ai_substitution','ai_market_disruption','ai_transition']
N={'cost_cutting':'Cost cutting','organizational_consolidation':'Teams, layers and sites','strategic_pivot':'Product / business pivot','financial_distress':'Funding / business viability','demand_decline':'Demand decline','m_and_a':'Merger integration','shutdown':'Business closure','unit_closure':'Unit or site closure','work_relocation':'Work relocation','market_exit':'Market exit','lost_contract':'Lost contract','ipo_prep':'IPO preparation','regulatory':'Regulation','performance_cull':'Performance reviews','ai_productivity':'AI productivity','ai_investment_reallocation':'AI investment','ai_work_redesign':'AI work redesign','ai_substitution':'AI substitution','ai_market_disruption':'AI market disruption'}
N.update({k:v[0] for k,v in GENERIC.items()})
N['ai_transition']='AI transition, without further detail'
font_manager.fontManager.addfont(P/'assets'/'jost-0.ttf')
font_manager.fontManager.addfont(P/'assets'/'jost-1.ttf')
INK='#252333';ACC='#6741bd';GRAY='#777281';PAPER='#fbfafc';LINE='#dedbe5'
plt.rcParams.update({'font.family':'Jost','font.size':11,'text.color':INK,'axes.labelcolor':INK,'xtick.color':GRAY,'ytick.color':INK,'svg.fonttype':'path','axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.edgecolor':LINE,'figure.facecolor':PAPER,'axes.facecolor':PAPER,'savefig.facecolor':PAPER})
def save(fig,name):
 _brand['stamp'](fig,name)
 for ext in ['svg','png']:fig.savefig(P/'assets'/f'{name}.{ext}',dpi=180,bbox_inches='tight',metadata={'Creator':'Layoff evidence report; generated from 2026-categorized.json, reviewed 2026-09-17'})
 plt.close(fig)
def bars(name,items,title,colors=None):
 fig,ax=plt.subplots(figsize=(10,max(2,len(items)*.4+.8)));labs=[a for a,b in items];vals=[b for a,b in items];y=range(len(items));ax.barh(y,vals,color=colors or ACC,height=.58);ax.set_yticks(list(y),labs);ax.invert_yaxis();ax.tick_params(axis='y',length=0,pad=12);ax.set_xlim(0,max(vals)*1.14);ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True,nbins=5));ax.set_xlabel('Announcement records');ax.grid(axis='x',alpha=.22);ax.set_axisbelow(True)
 for i,v in enumerate(vals):ax.text(v+.45,i,str(v),va='center',weight='bold')
 fig.tight_layout();save(fig,name)
items=C.most_common();bars('mechanisms',[(N[c],v) for c,v in items],'',[ACC for c,v in items])
# The explorer also exports every attributed reason, with general reasons marked explicitly.
ALL_COUNTS=collections.Counter(c for r in PUBLIC for c in r['causes'])
ALL_ITEMS=sorted(ALL_COUNTS.items(),key=lambda x:(-x[1],x[0]))
bars('all-reasons',[(N.get(c,GENERIC.get(c,[''])[0]),n) for c,n in ALL_ITEMS],'',[ACC for c,n in ALL_ITEMS])
PAIRS=collections.Counter((a,b) for r in PUBLIC for a in r['causes'] if a.startswith('ai_') for b in r['causes'] if not b.startswith('ai_'))
(P/'reason-counts.json').write_text(json.dumps({'announcement_records':len(PUBLIC),'with_attributed_reason':sum(bool(r['causes']) for r in PUBLIC),'reasons':[{'cause':c,'count':n,'detail':'general_reason' if c in GENERIC else 'change_described'} for c,n in ALL_ITEMS],'ai_pairs':[{'ai':a,'other':b,'count':n} for (a,b),n in sorted(PAIRS.items(),key=lambda x:(-x[1],x[0]))]},ensure_ascii=False,indent=2)+'\n')
bars('ai-mechanisms',[(N[c],C[c]) for c in AI],'')
bars('evidence-gaps',GAPS,'',colors=[GRAY,'#9984c9',ACC])
ai=lambda r:any(c in AI for c in r['causes'])
groups=[('AI + another reason',sum(ai(r) and any(c not in AI for c in r['causes']) for r in E)),('Only AI reasons recorded',sum(ai(r) and all(c in AI for c in r['causes']) for r in E)),('Only other reasons recorded',sum(bool(r['causes']) and not ai(r) for r in E)),('No classifiable explanation',sum(not r['causes'] for r in E))]
assert sum(n for _,n in groups)==len(E)
fig,ax=plt.subplots(figsize=(10,3.4));colors=[ACC,'#9984c9',GRAY,'#d4d0da'];left=0
for (label,n),color in zip(groups,colors):
 ax.barh([0],[n],left=left,height=.6,color=color,edgecolor=PAPER,linewidth=2);ax.text(left+n/2,0,str(n),ha='center',va='center',weight='bold',color=INK if color=='#d4d0da' else 'white',fontsize=14);left+=n
ax.set_xlim(0,len(E));ax.set_ylim(-.65,.65);ax.axis('off')
for i,((label,n),color) in enumerate(zip(groups,colors)):
 col=i%2;row=i//2;fig.add_artist(plt.Rectangle((.06+col*.49,.23-row*.105),.014,.038,transform=fig.transFigure,color=color));fig.text(.09+col*.49,.23-row*.105,label,fontsize=11)
fig.subplots_adjust(top=.94,bottom=.36,left=.04,right=.98);save(fig,'overlap')
rows=[c for c,_ in items if c not in AI]+['none'];cols=AI+['none']
rowmatch=lambda r,c:(not any(t not in AI for t in r['causes'])) if c=='none' else c in r['causes']
colmatch=lambda r,c:not ai(r) if c=='none' else c in r['causes']
M=[[sum(rowmatch(r,a) and colmatch(r,b) for r in E) for b in cols] for a in rows]
fig,ax=plt.subplots(figsize=(12,7.5));from matplotlib.colors import LinearSegmentedColormap
ax.imshow(M,cmap=LinearSegmentedColormap.from_list('evidence',[PAPER,'#d8cbed',ACC]),vmin=0,vmax=max(map(max,M)),aspect='auto')
ax.set_yticks(range(len(rows)),[N.get(c,'No other reason recorded') for c in rows]);ax.set_xticks(range(len(cols)),['AI output\ngains','AI\ninvestment','AI work\nredesign','AI\nsubstitution','AI market\ndisruption','AI transition\nwithout further detail','No AI reason\nrecorded']);ax.xaxis.tick_top();ax.tick_params(length=0,pad=10)
for i,row in enumerate(M):
 for j,n in enumerate(row):ax.text(j,i,str(n) if n else '—',ha='center',va='center',color='white' if n>30 else INK if n else GRAY)
for sp in ax.spines.values():sp.set_visible(False)
fig.tight_layout();save(fig,'matrix')
body=markdown.markdown((P/'draft.md').read_text(),extensions=['tables','toc'])
# The static Markdown retains a portable matrix image; the web report uses real controls.
# Ship the complete matrix in HTML; JavaScript adds record-selection controls.
static_matrix='<thead><tr><th scope="col">Other attributed mechanism</th>'
for col in cols:
    total=sum(colmatch(r,col) for r in E)
    static_matrix+='<th scope="col">'+html.escape(N.get(col,'No AI reason recorded'))+'<div class="matrix-total">'+str(total)+'</div></th>'
static_matrix+='</tr></thead><tbody>'
for row,counts in zip(rows,M):
    static_matrix+='<tr><th scope="row">'+html.escape(N.get(row,'No other reason recorded'))+'</th>'
    for count in counts:
        tint=f' style="background:color-mix(in srgb, var(--accent) {5+count/max(map(max,M))*32}%, transparent)"' if count else ''
        static_matrix+='<td'+tint+'><span class="matrix-count">'+str(count)+'</span></td>'
    static_matrix+='</tr>'
static_matrix+='</tbody>'
matrix_html='<div id="matrix" class="wide"><div class="chart-title">Which explanations appear together?</div><div class="controls" hidden><label><span data-explanation-label>Explanation detail</span><select id="explanation-mode"><option value="all" selected>All attributed explanations</option><option value="concrete">Concrete mechanisms only</option></select></label></div><p id="matrix-basis"></p><p class="matrix-hint">Scroll sideways to see every column.</p><div class="table-scroll" tabindex="0" role="region" aria-label="Figure 3: cause matrix, scroll horizontally"><table id="matrix-table" aria-label="Other mechanisms by AI mechanisms; overlapping record counts">'+static_matrix+'</table></div><div class="chart-author">By Nicolás Gómez from trabajoremoto.cl</div><a class="figure-download" download href="assets/matrix.svg">Download figure · SVG</a></div>'
body=re.sub(r'<p><img alt="[^"]*" src="assets/matrix.svg" /></p>',lambda _:matrix_html,body)
for filename in ['mechanisms','overlap','ai-mechanisms','evidence-gaps']:
 body=re.sub(r'(<p><img alt="([^"]*)" src="assets/'+filename+r'.svg" /></p>)',lambda m:'<figure class="wide"><img alt="'+m[2]+'" src="assets/'+filename+'.svg"><a class="figure-download" download href="assets/'+filename+'.svg">Download figure · SVG</a></figure>',body)
# Readable mobile alternatives keep chart text at native size instead of shrinking an image.
mobile_sets={'mechanisms':[(N[c],n) for c,n in items], 'ai-mechanisms':[(N[c],C[c]) for c in AI], 'evidence-gaps':GAPS, 'overlap':groups}
for name,values in mobile_sets.items():
    ceiling=len(E) if name=='overlap' else max(n for _,n in values)
    chart='<div class="mobile-chart" role="img" aria-label="'+html.escape('; '.join(f'{a}: {n}' for a,n in values))+'"><div class="chart-title">'+html.escape(_brand['TITLES'][name])+'</div><div class="chart-unit">Announcement records · scale 0–'+str(ceiling)+'</div>'
    for a,n in values:
        chart+='<div class="mobile-bar-row"><div class="mobile-bar-label"><span>'+html.escape(a)+'</span><strong>'+str(n)+'</strong></div><div class="mobile-track"><div style="width:'+str(n/ceiling*100)+'%"></div></div></div>'
    chart+='<div class="chart-author">'+html.escape(_brand['AUTHOR'])+'</div></div>'
    body=body.replace('src="assets/'+name+'.svg">','src="assets/'+name+'.svg">'+chart)
for needle,tag,label in [('Smaller teams, lower costs','ai_productivity','Explore all 24 productivity records'),('Changing where the money goes','ai_investment_reallocation','Explore all 14 investment records'),('When AI changes the business','ai_market_disruption','Explore all 7 market-disruption records')]:
 pat=r'(<h2[^>]*>'+re.escape(needle)+r'</h2>)';body=re.sub(pat,r'\1<button class="chapter-link" data-cause="'+tag+'">'+label+'</button>',body)
# Full prose tables remain horizontally scrollable at narrow widths.
body=re.sub(r'<table>(.*?)</table>',lambda m:'<table'+(' class="count-table"' if any(t in m[1] for t in ['Available detail','Detalle disponible','Attributed generic explanation','Explicación genérica atribuida']) else '')+'>'+m[1]+'</table>',body,flags=re.S)
body=re.sub(r'(<table(?: class="count-table")?>.*?</table>)',r'<div class="table-scroll wide">\1</div>',body,flags=re.S)
function_names=json.loads((ROOT/'research/functions/taxonomy.json').read_text())
meta={'records':PUBLIC,'names':N,'generic_names':GENERIC,'rows':[c for c in rows if c not in GENERIC],'columns':[c for c in cols if c not in GENERIC],'function_names':function_names}
(P/'index.html').write_text((P/'template.html').read_text().replace('<!--ARTICLE-->',body).replace('/*DATA*/',json.dumps(meta,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')))
(P/'records.json').write_text(json.dumps(PUBLIC,ensure_ascii=False,indent=2)+'\n')
with (P/'records.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in PUBLIC for k in r)))
 writer.writeheader()
 writer.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()} for r in PUBLIC)
(P/'assets'/'provenance.json').write_text(json.dumps({'source':'../records.json','review_date':'2026-09-17','unit':'retained H1 announcement records','denominator':len(E),'generated_by':'../build.py','explanation_basis':'all attributed reasons, including general reasons','figures':['all-reasons','mechanisms','overlap','matrix','ai-mechanisms','evidence-gaps']},indent=2))
print('Built report, 6 SVG + 6 PNG figures, downloadable prose and 228 H1 announcement records.')

import runpy
runpy.run_path(str(ROOT/'research/full-analysis/analyze.py'))

# Keep both language editions synchronized with the shared figures and data.
if (P/"build_es.py").exists():
 import runpy
 runpy.run_path(str(P/"build_es.py"))

if (P/"build_explorers.py").exists():
 runpy.run_path(str(P/"build_explorers.py"))

# Reproduce the linked hiring study when the research inputs are present.
if (ROOT/"research/hiring/build_report.py").exists():
 import runpy
 import contextlib, io
 with contextlib.redirect_stdout(io.StringIO()):
  runpy.run_path(str(ROOT/"research/hiring/analyze.py"))
 runpy.run_path(str(ROOT/"research/hiring/build_report.py"))

# Keep the analytical export synchronized with the canonical source.
runpy.run_path(str(ROOT/"scripts/build_normalized.py"))
