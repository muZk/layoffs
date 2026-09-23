"""Build the Spanish edition using the same figures and data as the English report."""
from pathlib import Path
import re
import markdown
P=Path(__file__).resolve().parent
english=(P/'index.html').read_text()
body=markdown.markdown((P/'informe.md').read_text(),extensions=['tables','toc'])
for name in ['mechanisms','overlap','ai-mechanisms','evidence-gaps']:
    figure=next(m.group() for m in re.finditer(r'<figure class="wide">.*?</figure>',english,re.S) if f'src="assets/{name}.svg"' in m.group())
    figure=figure.replace('Download figure · SVG','Descargar figura · SVG')
    body=re.sub(r'<p><img alt="[^"]*" src="assets/'+name+r'.svg" /></p>',lambda _:figure,body)
start=english.index('<div id="matrix"');end=english.index('<p><em>Figure 3.',start)
matrix=english[start:end].replace('Scroll sideways to see every column.','Desliza hacia los lados para ver todas las columnas.').replace('Download figure · SVG','Descargar figura · SVG')
body=re.sub(r'<p><img alt="[^"]*" src="assets/matrix.svg" /></p>',lambda _:matrix,body)
for title,cause,label in [('Equipos más pequeños, menores costos','ai_productivity','Explorar los 24 registros de productividad'),('Cambiar el destino del dinero','ai_investment_reallocation','Explorar los 14 registros de inversión'),('Cuando la IA cambia el negocio','ai_market_disruption','Explorar los 7 registros de disrupción del mercado')]:
    body=re.sub(r'(<h2[^>]*>'+re.escape(title)+'</h2>)',lambda m:m[1]+f'<button class="chapter-link" data-cause="{cause}">{label}</button>',body)
body=re.sub(r'<table>(.*?)</table>',lambda m:'<table'+(' class="count-table"' if any(t in m[1] for t in ['Available detail','Detalle disponible','Attributed generic explanation','Explicación genérica atribuida']) else '')+'>'+m[1]+'</table>',body,flags=re.S)
body=re.sub(r'(<table(?: class="count-table")?>.*?</table>)',r'<div class="table-scroll wide">\1</div>',body,flags=re.S)
template=(P/'template.html').read_text()
translations={
'<html lang="en">':'<html lang="es">',
'What do companies say when they cut jobs? — Layoff research':'¿Qué cuentan las empresas cuando recortan empleo? — Informe sobre despidos',
'Skip to report':'Ir al informe','Layoff research':'Informe sobre despidos','Download the report':'Descargar el informe','draft.md':'informe.md',
'Report sections':'Secciones del informe','The data':'Los datos','The matrix':'La matriz','Denials':'Declaraciones','Open questions':'Preguntas abiertas','Every record':'Todos los registros',
'#first-what-are-we-counting':'#primero-que-estamos-contando','#the-explanations-overlap':'#las-explicaciones-se-superponen','#what-does-an-ai-denial-actually-deny':'#que-se-niega-al-negar-un-vinculo-con-la-ia','#the-gaps-are-part-of-the-findings':'#los-vacios-tambien-son-parte-de-los-hallazgos',
'Read the evidence':'Consultar la evidencia',
'Every record remains accessible. Open an entry for its attributed causes, sources and unresolved issues.':'Todos los registros están disponibles. Abre una ficha para consultar las causas atribuidas, sus fuentes y las cuestiones pendientes. Las fichas conservan el inglés.',
'>Scope<':'>Alcance<','H1 announcement records':'Anuncios del primer semestre','Partial / unavailable sources':'Fuentes parciales o no disponibles','Selected matrix or chapter records':'Registros seleccionados','Find a company':'Buscar una empresa','Company name':'Nombre de la empresa','Show all H1 announcements':'Mostrar todos los anuncios del semestre',
'Interactive exploration requires JavaScript.':'La exploración interactiva requiere JavaScript.','Download every record':'Descargar todos los registros',' or ': ' o ','open the CSV':'abrir el CSV',
'Counts describe recorded explanations, not verified causal effects.':'Los recuentos describen las explicaciones registradas, no efectos causales verificados.',
'Reviewed data':'Datos revisados','Definitions':'Definiciones (inglés)','Methodology':'Metodología (inglés)','Editable prose':'Texto editable','report.js':'report-es.js',
'Explore the data':'Explorar los datos','explore.html':'explorar.html','>Mechanism<':'>Explicación<','All mechanisms':'Todas las explicaciones','Evidence category':'Categoría de evidencia','All evidence categories':'Todas las categorías','Mechanism specified':'Mecanismo especificado','Generic explanation only':'Solo explicación genérica','No explanation identified':'Sin explicación identificada','Evidence limited':'Evidencia limitada','No causal source recovered':'Fuente causal no recuperada',
'<a href="index-es.html" lang="es">Español</a>':'<a href="index.html" lang="en">English</a>'}
for old,new in translations.items():template=template.replace(old,new)
template=template.replace('Todos los registros remains accessible. Open an entry for its attributed causes, sources and unresolved issues.','Todos los registros están disponibles. Abre una ficha para consultar las explicaciones atribuidas, sus fuentes y las cuestiones pendientes. Las fichas de evidencia conservan el inglés.')
data=re.search(r'<script id="data" type="application/json">(.*?)</script>',english,re.S)[1]
(P/'index-es.html').write_text(template.replace('<!--ARTICLE-->',body).replace('/*DATA*/',data))
js=(P/'report.js').read_text()
for old,new in {
"label='H1 announcement records'":"label='Anuncios del primer semestre'",
"' · '+list.length+' records'":"' · '+list.length+' registros'",
'No companies match this search. Try a shorter name or change the scope.':'No hay empresas que coincidan con la búsqueda. Prueba con un nombre más corto o cambia el alcance.',
'Supporting source':'Fuente de la explicación','Context source':'Fuente del contexto','Denial source':'Fuente de la declaración',
"'Context: '":"'Contexto: '","'Denial: '":"'Negación: '",'Recorded headcount: ':'Personal afectado registrado: ','Separate metric: ':'Medida independiente: ','Issues / corrections: ':'Cuestiones pendientes / correcciones: ','Review source ':'Fuente revisada '
}.items():js=js.replace(old,new)
(P/'report-es.js').write_text(js)
print('Built Spanish edition with shared English figures and evidence records.')
