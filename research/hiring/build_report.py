"""Reproduce the exploratory hiring study, charts and downloadable company ledger."""
import json,csv,html,re,statistics,collections,shutil,hashlib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import markdown
P=Path(__file__).resolve().parent;R=P.parents[1];OUT=R/'report'
import runpy
stamp=runpy.run_path(str(OUT/'chart_branding.py'))['stamp']
rows=json.loads((P/'company-history.json').read_text());summary=json.loads((P/'summary.json').read_text());sens=json.loads((P/'sensitivity.json').read_text());cases=json.loads((P/'business-cases.json').read_text())
lookup={r['company']:r for r in rows};groups=['ai_recorded','other_recorded','unresolved'];labels={'ai_recorded':'Explicación de IA registrada','other_recorded':'Solo otras razones registradas','unresolved':'Sin explicación clasificable'}
colors=['#6741bd','#777281','#b9aecb'];font_manager.fontManager.addfont(OUT/'assets/jost-0.ttf');font_manager.fontManager.addfont(OUT/'assets/jost-1.ttf')
plt.rcParams.update({'font.family':'Jost','font.size':11,'text.color':'#252333','axes.labelcolor':'#252333','axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'figure.facecolor':'#fbfafc','axes.facecolor':'#fbfafc','savefig.facecolor':'#fbfafc','svg.fonttype':'path'})
fig,axes=plt.subplots(2,1,figsize=(10,7.8));rng=np.random.default_rng(19)
for ax,window in zip(axes,['2019_2022','2022_2025']):
 for i,g in enumerate(groups):
  vals=np.array([r['growth'][window] for r in rows if r['group']==g and window in r['growth']]);ratios=1+vals/100
  ax.scatter(ratios,i+rng.uniform(-.16,.16,len(vals)),s=31,color=colors[i],alpha=.8,edgecolors='white',linewidth=.4)
  ax.scatter(1+np.median(vals)/100,i,marker='D',s=75,color='#252333',zorder=5)
 ax.set_xscale('log');ax.set_xlim(.2,10);ax.set_xticks([.25,.5,1,2,4,8],['−75%','−50%','0%','+100%','+300%','+700%']);ax.axvline(1,color='#aaa4b1',ls=':',lw=1);ax.grid(axis='x',alpha=.15);ax.set_yticks(range(3),[f'{a}\n(n={summary[window][g]["n"]})' for a,g in zip(['AI explanation recorded','Only other reasons recorded','No classifiable explanation'],groups)]);ax.set_ylim(2.5,-.55);ax.set_title(window.replace('_','–'),loc='left',fontweight='bold',pad=12);ax.tick_params(axis='y',length=0)
axes[1].set_xlabel('Reported workforce change · logarithmic ratio scale');fig.text(.02,.01,'One dot per company. Diamond = group median. Source: Stock Analysis, with partial primary-source checks.',fontsize=10)
fig.tight_layout(rect=(0,.04,1,1))
stamp(fig,'hiring-distribution')
for ext in ['svg','png']:fig.savefig(OUT/'assets'/f'hiring-distribution.{ext}',dpi=180,bbox_inches='tight')
plt.close(fig)
# A separate portrait figure preserves readable labels on narrow screens.
fig,axes=plt.subplots(6,1,figsize=(5,9.5),sharex=True)
for i,(window,g) in enumerate((w,g) for w in ['2019_2022','2022_2025'] for g in groups):
 ax=axes[i];vals=np.array([r['growth'][window] for r in rows if r['group']==g and window in r['growth']]);color=colors[groups.index(g)]
 ax.scatter(1+vals/100,rng.uniform(-.15,.15,len(vals)),color=color,s=30,alpha=.8)
 ax.scatter(1+np.median(vals)/100,0,marker='D',color='#252333',s=55,zorder=5)
 short={'ai_recorded':'AI explanation','other_recorded':'Other reasons','unresolved':'Not specified'}[g]
 ax.set_title((window.replace('_','–')+' · ' if i%3==0 else '')+short+' · n='+str(len(vals)),loc='left',fontsize=13,pad=8)
 ax.set_xscale('log');ax.set_xlim(.2,10);ax.set_ylim(-.3,.3);ax.set_yticks([]);ax.axvline(1,color='#aaa4b1',ls=':',lw=1);ax.set_xticks([.25,.5,1,2,4,8],['−75%','−50%','0%','+100%','+300%','+700%']);ax.tick_params(axis='x',labelbottom=i in [2,5],labelsize=11);ax.grid(axis='x',alpha=.15)
axes[-1].set_xlabel('Reported workforce change',fontsize=13);fig.tight_layout(h_pad=1.4)
stamp(fig,'hiring-distribution-mobile')
fig.savefig(OUT/'assets/hiring-distribution-mobile.svg',bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(9,4.6));y=np.arange(len(cases))
h=[lookup[c['company']]['growth']['2019_2022'] for c in cases];b=[100*(c['value_2022']/c['value_2019']-1) for c in cases]
ax.barh(y-.16,h,height=.29,color=colors[0],label='Reported workforce');ax.barh(y+.16,b,height=.29,color=colors[1],label='Business measure')
for i,(a,v) in enumerate(zip(h,b)):
 ax.text(a+3,i-.16,f'~{a:.0f}%',va='center',fontsize=10);ax.text(v+3,i+.16,f'~{v:.0f}%',va='center',fontsize=10)
ax.set_yticks(y,[c['company']+' · '+c['metric'].lower() for c in cases]);ax.invert_yaxis();ax.set_xlim(0,310);ax.set_xlabel('Change from 2019 to 2022 (%)');ax.legend(loc='upper left',bbox_to_anchor=(0,-.23),ncol=2,frameon=False);ax.tick_params(axis='y',length=0);ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True);fig.tight_layout()
stamp(fig,'hiring-business')
for ext in ['svg','png']:fig.savefig(OUT/'assets'/f'hiring-business.{ext}',dpi=180,bbox_inches='tight')
plt.close(fig)
# Export a ledger for all companies, including explicit noncoverage.
package={'announcement_dataset_sha256':hashlib.sha256((OUT/'records.json').read_bytes()).hexdigest(),'reviewed':'2026-09-28','unit':'dataset company label; no parent-company substitution','coverage':'217 company labels, 88 candidate public histories, 71 usable 2022–2025 pairs and 35 usable 2019–2022 pairs','source_quality':'Secondary compilation with partial primary checks; not a harmonized census','explanation_basis':'All attributed reasons, including AI transition without further detail; matches narrative and explorer','method':'Latest dated numeric observation within each calendar year; no imputation; net workforce growth, not hires. Unknown explanations remain a separate group. Known date errors excluded or corrected. Acquisitions not numerically adjusted.','companies':rows,'summary':summary,'sensitivity':sens,'business_cases':cases,'historical_statements':json.loads((P/'historical-statements.json').read_text())}
(OUT/'hiring-research.json').write_text(json.dumps(package,ensure_ascii=False,indent=2)+'\n')
fields=['company','group','coverage_status','workforce_2019','date_2019','source_2019','workforce_2022','date_2022','source_2022','workforce_2025','date_2025','source_2025','growth_2019_2022_pct','growth_2022_2025_pct','quality_issues','perimeter_events']
with (OUT/'hiring-research.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in rows:
  d={k:r[k] for k in ['company','group','coverage_status']}
  for yr in ['2019','2022','2025']:
   o=r['endpoints'].get(yr,{});d.update({f'workforce_{yr}':o.get('value'),f'date_{yr}':o.get('date'),f'source_{yr}':o.get('source_url')})
  for win in ['2019_2022','2022_2025']:d['growth_'+win+'_pct']=r['growth'].get(win)
  for key in ['quality_issues','perimeter_events']:d[key]=json.dumps(r[key],ensure_ascii=False)
  w.writerow(d)
# Tables generated from exactly the published data.
fmt=lambda v:f'{v:+.1f}%'.replace('.',',')
table='| Período | IA registrada | Solo otras causas | Sin explicación clasificable |\n|---|---:|---:|---:|\n'
for win in ['2019_2022','2022_2025']:
 table+='| '+win.replace('_','–')+' | '+' | '.join(f"**{fmt(summary[win][g]['median'])}** · {summary[win][g]['n']} empresas" for g in groups)+' |\n'
sentable='| Comparación | IA registrada | Solo otras causas |\n|---|---:|---:|\n'
for w,key,label in [('2019_2022','exclude_documented_perimeter_events','2019–2022: excluir operaciones societarias documentadas'),('2022_2025','same_companies_both_windows','2022–2025: mismas empresas presentes en ambos períodos'),('2022_2025','december_observations_only','2022–2025: solo observaciones de diciembre'),('2022_2025','exclude_known_definition_or_scope_mismatch','2022–2025: excluir diferencias conocidas de definición o alcance')]:
 s=sens[w][key];sentable+='| '+label+' | '+' | '.join(f"{fmt(s[g]['median'])} · n={s[g]['n']}" for g in groups[:2])+' |\n'
ledger='<details><summary>Ver las empresas y las cifras utilizadas</summary><div class="table-scroll"><table><thead><tr><th>Empresa / grupo</th><th>2019</th><th>2022</th><th>2025</th><th>2019–22</th><th>2022–25</th></tr></thead><tbody>'
for r in sorted([r for r in rows if r['growth']],key=lambda r:r['company'].lower()):
 ledger+='<tr><th>'+html.escape(r['company'])+'<br><small>'+labels[r['group']]+'</small></th>'
 for y in ['2019','2022','2025']:
  o=r['endpoints'].get(y);ledger+='<td>'+ (f'<a href="{html.escape(o["source_url"])}">{o["value"]:,}</a><br><small>{o["date"]}</small>' if o else '—')+'</td>'
 for win in ['2019_2022','2022_2025']:ledger+='<td>'+(fmt(r['growth'][win]) if win in r['growth'] else '—')+'</td>'
 ledger+='</tr>'
ledger+='</tbody></table></div></details>'
text=(P/'report-template.md').read_text().replace('<!--RESULTS-->',table).replace('<!--SENSITIVITY-->',sentable).replace('<!--LEDGER-->',ledger)
(OUT/'contratacion.md').write_text(text)
body=markdown.markdown(text,extensions=['tables','toc']);body=body.replace('<img alt="Distribución del crecimiento de plantilla por grupo y período. Cada punto es una empresa y los rombos marcan las medianas." src="assets/hiring-distribution.svg" />','<picture><source media="(max-width:600px)" srcset="assets/hiring-distribution-mobile.svg"><img alt="Distribución del crecimiento de plantilla por grupo y período. Cada punto es una empresa y los rombos marcan las medianas." src="assets/hiring-distribution.svg"></picture>');body=re.sub(r'(<table>.*?</table>)',r'<div class="table-scroll">\1</div>',body,flags=re.S)
# Reuse the editorial typography; plain scientific figures remain visible on mobile.
page='''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Contratación previa y explicaciones de IA</title><link rel="stylesheet" href="report.css"><style>article img{display:block;width:100%;height:auto;margin:28px 0}article details{margin:32px 0;font:15px/1.6 var(--display)}article summary{cursor:pointer;color:var(--accent);padding:12px 0}article small{font-size:12px}article details table{min-width:850px}article details th:first-child{min-width:200px}article .table-scroll{margin:24px 0}article h1{font-size:clamp(34px,5vw,58px)}</style></head><body><a class="skip" href="#article">Ir a la investigación</a><header class="masthead"><span>Informe sobre despidos</span><a href="contratacion.md" download>Descargar la investigación</a></header><nav aria-label="Investigación"><a href="index-es.html">Artículo</a><a href="explorar.html">Explorador</a><a href="#que-encontramos">Resultados</a><a href="#metodo-y-cobertura">Método y cobertura</a><a href="hiring-research.csv" download>Descargar datos</a></nav><main><article id="article">'''+body+'''</article></main><footer>Clasificaciones revisadas: 28 de septiembre de 2026 · Crecimiento de plantilla y causas atribuidas son medidas distintas.</footer></body></html>'''
(OUT/'contratacion.html').write_text(page)
print('Built hiring study, two figures, 217-company ledger and source-linked exports.')
