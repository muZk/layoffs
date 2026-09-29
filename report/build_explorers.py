"""Produce two exploratory companions from the same generated report and data."""
from pathlib import Path
import re,json,html
import markdown
P=Path(__file__).resolve().parent
D=json.loads((P/'records.json').read_text());E=[r for r in D if r['date']<'2026-07-01' and r['record_type']=='announcement'];ai=lambda r:any(c.startswith('ai_') for c in r['causes'])
groups=[('mixed',sum(ai(r) and any(not c.startswith('ai_') for c in r['causes']) for r in E)),('ai-only',sum(ai(r) and all(c.startswith('ai_') for c in r['causes']) for r in E)),('other-only',sum(bool(r['causes']) and not ai(r) for r in E)),('none',sum(not r['causes'] for r in E)),('multiple',sum(len(r['causes'])>1 for r in E))]
def function_section(es):
 names=json.loads((P.parent/'research/functions/taxonomy.json').read_text()) if es else dict(zip(['engineering','product_design','data','it_security','sales','marketing','support','people','corporate','operations','content','manufacturing'],['Engineering and R&D','Product and design','Data and analytics','IT and cybersecurity','Sales and partnerships','Marketing','Customer support','HR and recruitment','Administration, finance and legal','Operations and service delivery','Content and education','Manufacturing']))
 labels=['Funciones identificadas','Solo unidad de negocio','Sin función ni unidad identificada'] if es else ['Functions identified','Business unit only','Neither function nor unit identified']
 buttons=''.join(f'<button class="chapter-link" data-work-status="{k}">{label} · {sum(r["affected_work"]["status"]==k for r in E)}</button>' for k,label in zip(['identified','unit_only','not_identified'],labels))
 title='¿Qué trabajo se recorta y qué explicación se ofrece?' if es else 'What work is cut, and what explanation is offered?'
 intro=('Identificamos funciones concretas en <strong>62 de 228 registros</strong>. En otros 8 solo se identifica una unidad de negocio, y en 158 no identificamos ninguna de las dos. “Cloud” describe una unidad; no basta para clasificar a sus trabajadores como ingenieros.' if es else 'We identified specific functions in <strong>62 of 228 records</strong>. Another 8 identify only a business unit, and 158 identify neither. “Cloud” describes a unit; it does not establish that the affected workers are engineers.')
 hint=('Cada cifra abre sus registros. Un anuncio puede afectar a varias funciones: no sumes filas. La vista de causas individuales también permite varias columnas por registro. Son anuncios, no puestos ni tasas de riesgo por profesión.' if es else 'Each count opens its records. An announcement may affect several functions: do not sum rows. Individual causes can also put a record in multiple columns. These are announcement counts, not jobs or occupational risk rates.')
 cols=['Registros','IA y otra causa','Solo IA registrada','Solo otras causas','Sin causa específica'] if es else ['Records','AI + other','Only AI recorded','Only other causes','No specific cause']
 table='<thead><tr><th scope="col">'+('Función afectada' if es else 'Affected function')+'</th>'+''.join('<th scope="col">'+x+'</th>' for x in cols)+'</tr></thead><tbody>'
 for key in sorted(names,key=lambda k:-sum(k in r['affected_work']['functions'] for r in E))+['unknown']:
  subset=[r for r in E if (key in r['affected_work']['functions'] if key!='unknown' else not r['affected_work']['functions'])]
  vals=[len(subset),sum(ai(r) and any(not c.startswith('ai_') for c in r['causes']) for r in subset),sum(ai(r) and all(c.startswith('ai_') for c in r['causes']) for r in subset),sum(bool(r['causes']) and not ai(r) for r in subset),sum(not r['causes'] for r in subset)]
  table+='<tr><th scope="row">'+names.get(key,'Sin función identificada' if es else 'No function identified')+'</th>'+''.join('<td>'+str(v)+'</td>' for v in vals)+'</tr>'
 mode=('Agrupar explicaciones','Cuatro grupos','Causas individuales') if es else ('Group explanations','Four groups','Individual causes')
 return f'<section id="affected-functions"><h2>{title}</h2><p>{intro}</p>{buttons}<p>{hint}</p><div class="controls"><label>{mode[0]}<select id="function-matrix-mode"><option value="groups">{mode[1]}</option><option value="causes">{mode[2]}</option></select></label></div><p class="matrix-hint">'+('Desliza horizontalmente para ver todas las columnas.' if es else 'Scroll horizontally to see every column.')+f'</p><div class="table-scroll wide" tabindex="0" role="region" aria-label="{title}"><table id="function-matrix" class="function-matrix">{table}</tbody></table></div><div class="chart-author">By Nicolás Gómez from trabajoremoto.cl</div></section>'

for es in [False,True]:
 original=(P/('index-es.html' if es else 'index.html')).read_text();name='explorar' if es else 'explore';body=markdown.markdown((P/f'{name}.md').read_text(),extensions=['tables','toc'])
 for fig in ['overlap','evidence-gaps']:
  fragment=next(m.group() for m in re.finditer(r'<figure class="wide">.*?</figure>',original,re.S) if f'src="assets/{fig}.svg"' in m.group())
  body=re.sub(r'<p><img alt="[^"]*" src="assets/'+fig+r'.svg" /></p>',lambda _:fragment,body)
 start=original.index('<div id="matrix"');end=original.index('<p><em>'+('Figura' if es else 'Figure')+' 3.',start)
 body=re.sub(r'<p><img alt="[^"]*" src="assets/matrix.svg" /></p>',lambda _:original[start:end],body)
 labels=['IA y otro mecanismo','Solo mecanismos de IA registrados','Solo otros mecanismos registrados','Sin mecanismo especificado','Más de un mecanismo'] if es else ['AI and another mechanism','Only AI mechanisms recorded','Only other mechanisms recorded','No mechanism specified','More than one mechanism']
 buttons=''.join(f'<button class="chapter-link" data-group="{key}">{html.escape(label)} · {count}</button>' for (key,count),label in zip(groups,labels))
 body=body.replace('<!--GROUPS-->',buttons)
 body=body.replace('<!--FUNCTIONS-->',function_section(es))
 reason_html='<div class="chart-title">'+('Razones atribuidas a los recortes' if es else 'Reasons attributed to layoffs')+'</div><p id="reason-basis" class="reason-note"></p><div id="reason-bars" class="reason-chart"></div><div class="chart-author">By Nicolás Gómez from trabajoremoto.cl</div><p class="figure-download"><a id="reason-download-svg" href="assets/all-reasons.svg" download>SVG</a> · <a id="reason-download-png" href="assets/all-reasons.png" download>PNG</a> · <a href="reason-counts.json" download>'+('Todos los recuentos' if es else 'All counts')+'</a></p><noscript><p>'+('Consulta el gráfico completo en la descarga SVG.' if es else 'View the complete chart in the SVG download.')+'</p></noscript>'
 body=body.replace('<!--REASONS-->',reason_html)
 body=body.replace('<!--AI-PAIRS-->','<div class="chart-title">'+('Cruces de IA más frecuentes' if es else 'Most frequent AI explanation pairs')+'</div><p id="pair-basis" class="reason-note" aria-live="polite"></p><ol id="ai-pairs" class="pair-ranking"></ol><div class="chart-author">By Nicolás Gómez from trabajoremoto.cl</div><noscript><a href="reason-counts.json">'+('Consultar recuentos de los cruces' if es else 'View pair counts')+'</a></noscript>')

 labels=['Solo razones generales','Sin explicación identificada','Evidencia limitada','Fuente causal no recuperada'] if es else ['General reasons only','No explanation identified','Evidence limited','No causal source recovered']
 buttons=''.join(f'<button class="chapter-link" data-status="{key}">{label} · {sum(r["cause_status"]==key for r in E)}</button>' for key,label in zip(['generic','unspecified','unresolved','unavailable'],labels))
 body=body.replace('<!--EVIDENCE-->',buttons)
 body=re.sub(r'<div class="controls"><label><span data-explanation-label>.*?</select></label></div>',lambda m:'<div hidden>'+m.group()+'</div>',body,flags=re.S)
 body=re.sub(r'<table>(.*?)</table>',lambda m:'<table'+(' class="count-table"' if any(t in m[1] for t in ['Available detail','Detalle disponible','Attributed generic explanation','Explicación genérica atribuida','Razón general atribuida','Attributed general reason']) else '')+'>'+m[1]+'</table>',body,flags=re.S)
 body=re.sub(r'(<table(?: class="count-table")?>.*?</table>)',r'<div class="table-scroll wide">\1</div>',body,flags=re.S)
 out=re.sub(r'<article id="article">.*?</article>',lambda _:'<article id="article">'+body+'</article>',original,flags=re.S)
 out=re.sub(r'<title>.*?</title>', '<title>'+('Explorar las explicaciones de los despidos' if es else 'Explore the explanations behind the cuts')+'</title>',out)
 nav=('<a href="explore.html" lang="en">English</a><a href="index-es.html">Leer los hallazgos</a><a href="#que-explicaciones-aparecen-juntas">La matriz</a><a href="#que-informacion-sigue-faltando">Los vacíos</a><a href="#register">Filtrar registros</a>' if es else '<a href="explorar.html" lang="es">Español</a><a href="index.html">Read the findings</a><a href="#what-appears-together">The matrix</a><a href="#what-information-is-still-missing">Evidence gaps</a><a href="#register">Filter records</a>')
 out=re.sub(r'<nav[^>]*>.*?</nav>',lambda _:'<nav aria-label="'+('Explorar' if es else 'Explore')+'">'+nav+'</nav>',out,flags=re.S)
 out=out.replace('href="'+('informe.md' if es else 'draft.md')+'"',f'href="{name}.md"')
 (P/f'{name}.html').write_text(out)
print('Built English and Spanish data explorers.')
