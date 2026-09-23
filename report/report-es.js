(()=>{
'use strict';
const {records:data,names,rows,columns,function_names:fnEs,generic_names:genericNames}=JSON.parse(document.getElementById('data').textContent);
const h1=data.filter(r=>r.date>='2026-01-01'&&r.date<'2026-07-01');const events=h1.filter(r=>r.record_type==='announcement');
const level=document.getElementById('explanation-mode');
const activeCauses=r=>r.causes.filter(c=>level.value==='all'||r.cause_details[c].specificity==='concrete');
const ai=r=>activeCauses(r).some(c=>c.startsWith('ai_'));
const rowMatch=(r,k)=>k==='none'?!activeCauses(r).some(c=>!c.startsWith('ai_')):activeCauses(r).includes(k);
const colMatch=(r,k)=>k==='none'?!ai(r):activeCauses(r).includes(k);
const scope=document.getElementById('scope'),search=document.getElementById('search'),causeFilter=document.getElementById('cause-filter'),evidenceFilter=document.getElementById('evidence-filter');let selected=events,label='Anuncios del primer semestre';
function make(tag,text,parent,cls){const n=document.createElement(tag);if(text!==null)n.textContent=text;if(cls)n.className=cls;if(parent)parent.appendChild(n);return n}
function link(text,url,parent){if(!/^https?:\/\//.test(url||''))return;const a=make('a',text,parent);a.href=url;a.target='_blank';a.rel='noopener noreferrer'}
const clean=s=>s.replaceAll('_',' ');
const es=document.documentElement.lang==='es';
const fnNames=es?fnEs:{engineering:'Engineering and R&D',product_design:'Product and design',data:'Data and analytics',it_security:'IT and cybersecurity',sales:'Sales and partnerships',marketing:'Marketing',support:'Customer support',people:'HR and recruitment',corporate:'Administration, finance and legal',operations:'Operations and service delivery',content:'Content and education',manufacturing:'Manufacturing'};
if(es)Object.assign(names,{cost_cutting:'Reducción de costos',organizational_consolidation:'Consolidación organizacional',strategic_pivot:'Cambio de producto o negocio',financial_distress:'Dificultades financieras',demand_decline:'Caída de la demanda',m_and_a:'Integración tras una adquisición',shutdown:'Cierre de la empresa',unit_closure:'Cierre de unidad o sede',work_relocation:'Traslado del trabajo',market_exit:'Salida de un mercado',lost_contract:'Pérdida de contrato',ipo_prep:'Preparación de salida a bolsa',regulatory:'Regulación',performance_cull:'Evaluación de desempeño',ai_productivity:'Productividad con IA',ai_investment_reallocation:'Inversión hacia IA',ai_work_redesign:'Rediseño del trabajo con IA',ai_substitution:'Sustitución por IA',ai_market_disruption:'Cambio del mercado por IA'});
genericNames.ai_transition=['AI transition, without further detail','Transición hacia IA, sin mayor detalle'];
for(const [k,v] of Object.entries(genericNames))names[k]=(es?v[1]:v[0]);
level.value='all';
document.querySelector('[data-explanation-label]').textContent=es?'Detalle de las explicaciones':'Explanation detail';
level.options[0].textContent=es?'Todas las explicaciones atribuidas':'All attributed explanations';
level.options[1].textContent=es?'Solo cambios descritos':'Described changes only';
let redrawFunctions=()=>{};
const statusNames=es?{specified:'Cambio descrito',generic:'Solo razones generales',unspecified:'Sin explicación identificada',unresolved:'Evidencia limitada',unavailable:'Fuente no recuperada'}:{specified:'Described change',generic:'General reasons only',unspecified:'No explanation identified',unresolved:'Evidence limited',unavailable:'Source not recovered'};
for(const o of evidenceFilter.options)if(statusNames[o.value])o.textContent=statusNames[o.value];
const unknown=es?'Sin función identificada':'No function identified';
const functionFilter=document.getElementById('function-filter');
document.querySelector('[data-function-label]').textContent=es?'Función afectada':'Affected function';
functionFilter.options[0].textContent=es?'Todas, incluidas las no identificadas':'All, including unidentified functions';
for(const [key,title] of [...Object.entries(fnNames),['unknown',unknown]]){const o=make('option',title,functionFilter);o.value=key}
const fnMatch=(r,k)=>k==='unknown'?!r.affected_work?.functions.length:r.affected_work?.functions.includes(k);
functionFilter.onchange=()=>render();

function render(){const list=selected.filter(r=>r.company.toLowerCase().includes(search.value.trim().toLowerCase())&&(!causeFilter.value||activeCauses(r).includes(causeFilter.value))&&(!evidenceFilter.value||r.cause_status===evidenceFilter.value)&&(!functionFilter.value||fnMatch(r,functionFilter.value)));const out=document.getElementById('records');out.replaceChildren();document.getElementById('selection').textContent=label+' · '+list.length+' registros';
if(!list.length){make('p','No hay empresas que coincidan con la búsqueda. Prueba con un nombre más corto o cambia el alcance.',out);return}
for(const r of list){const d=make('details',null,out,'record');d.id=r.record_id;const summary=make('summary',r.company+' ',d);make('span',r.date+' · '+clean(r.review.status),summary);const b=make('div',null,d,'record-content');make('p',r.review.note,b);make('p',clean(r.record_type)+' · '+statusNames[r.cause_status],b,'meta');
if(r.affected_work){const w=r.affected_work;make('h3',es?'Trabajo afectado':'Affected work',b);make('p',w.functions.length?w.functions.map(f=>fnNames[f]).join(' · '):unknown,b,'meta');make('p',w.review.note,b);
for(const e of w.details){make('p',e.summary,b);make('p',clean(e.attribution)+' · '+(e.evidence_access==='partial'?(es?'Extracto; fuente incompleta':'Extract; incomplete source'):e.evidence_access==='prior_review'?(es?'Evidencia conservada de la revisión':'Retained review evidence'):(es?'Fuente consultada':'Source reviewed')),b,'meta');link(es?'Fuente de las funciones':'Function source',e.source_url,b)}
for(const u of w.units){make('p',(es?'Unidad / alcance: ':'Unit / scope: ')+u.name+' — '+u.summary,b);link(es?'Fuente de la unidad':'Unit source',u.source_url,b)}
if(w.levels.length)make('p',(es?'Nivel, no función: ':'Level, not function: ')+w.levels.map(clean).join(', '),b,'meta');}
for(const a of r.headcount_accounts||[]){make('p',(es?'Cifra con alcance pendiente: ':'Scoped / disputed count: ')+(a.value??'—')+(a.pct?' ('+Math.round(a.pct*100)+'%)':'')+' — '+a.note,b);link(es?'Fuente de la cifra':'Count source',a.source_url,b)}
for(const c of r.causes){const e=r.cause_details[c];make('h3',names[c]||clean(c),b);make('p',(e.specificity==='generic'?(es?'Razón general':'General reason'):(es?'Cambio descrito':'Described change'))+' · '+clean(e.attribution)+' · '+clean(e.scope),b,'meta');make('p',e.summary,b);link('Fuente de la explicación',e.source_url,b)}
for(const c of r.context){make('h3','Contexto: '+clean(c.kind),b);make('p',c.summary,b);link('Fuente del contexto',c.source_url,b)}
for(const x of r.denials){make('h3','Negación: '+clean(x.target),b);make('p',clean(x.speaker)+': '+x.summary,b);link('Fuente de la declaración',x.source_url,b)}
if(r.laid_off!==null)make('p','Personal afectado registrado: '+r.laid_off.toLocaleString()+' · '+clean(r.headcount_scope),b);
if(r.reported_workforce_change){const m=r.reported_workforce_change;make('p','Medida independiente: '+(m.value??'undisclosed')+' · '+clean(m.metric)+' · '+m.period,b)}
if(r.review.issues.length)make('p','Cuestiones pendientes / correcciones: '+r.review.issues.map(clean).join('; '),b);
const links=make('div',null,b,'source-links');r.review.sources.forEach((url,i)=>link('Fuente revisada '+(i+1),url,links));}}
function choose(group,title){selected=group;label=title;search.value='';causeFilter.value='';evidenceFilter.value='';functionFilter.value='';scope.value='selection';render();document.getElementById('register').scrollIntoView();document.getElementById('register-heading').focus({preventScroll:true})}
document.getElementById('register-heading').tabIndex=-1;
function drawCauseMatrix(){
const liveRows=rows.filter(k=>k!=='none').concat(level.value==='all'?Object.keys(genericNames).filter(k=>!k.startsWith('ai_')):[],['none']);
const liveCols=columns.filter(k=>k!=='none').concat(level.value==='all'?['ai_transition']:[],['none']);
const basis=level.value==='all'?(es?'Todas las explicaciones atribuidas, incluidas las razones generales.':'All attributed explanations, including general reasons.'):(es?'Solo cambios descritos; las razones generales no cuentan en estas celdas.':'Described changes only; general reasons do not count in these cells.');
document.getElementById('matrix-basis').textContent=document.getElementById('reason-bars')?(es?'Se incluyen todas las razones atribuidas. Las celdas cuentan anuncios, no puestos.':'All attributed reasons are included. Cells count announcements, not jobs.'):basis+' '+(document.getElementById('function-matrix')?(es?'El selector también cambia la matriz de funciones. ':'This selector also changes the function matrix. '):'')+(document.getElementById('reason-bars')?(es?'El gráfico de razones y el ranking también siguen esta vista.':'The reason chart and ranking also follow this view.'):(es?'Las figuras cuentan todas las razones atribuidas.':'Figures count all attributed reasons.'));
const table=document.getElementById('matrix-table');table.replaceChildren();const head=make('thead',null,table);const tr=make('tr',null,head);make('th','Other attributed mechanism',tr).scope='col';
for(const c of liveCols){const th=make('th',null,tr);th.scope='col';const title=names[c]||'No AI explanation in this view';make('div',title,th);const g=events.filter(r=>colMatch(r,c));const btn=make('button',String(g.length),th);btn.type='button';btn.setAttribute('aria-label',title+', '+g.length+' records');btn.onclick=()=>choose(g,title)}
const body=make('tbody',null,table);
for(const row of liveRows){const tr=make('tr',null,body);const title=names[row]||'No other explanation in this view';make('th',title,tr).scope='row';for(const col of liveCols){const td=make('td',null,tr);const group=events.filter(r=>rowMatch(r,row)&&colMatch(r,col));const btn=make('button',String(group.length),td);btn.type='button';btn.disabled=!group.length;btn.dataset.count=group.length;btn.setAttribute('aria-label',title+' and '+(names[col]||'No AI explanation in this view')+': '+group.length+' records');if(group.length)td.style.background='color-mix(in srgb, var(--accent) '+(5+group.length/Math.max(1,events.filter(r=>!activeCauses(r).length).length)*32)+'%, transparent)';btn.onclick=()=>choose(group,title+' × '+(names[col]||'No AI explanation in this view'))}}
}
scope.onchange=()=>{const mode=scope.value;if(mode==='selection')return;selected=mode==='gaps'?data.filter(r=>r.review.status!=='source_reviewed'):events;label=scope.options[scope.selectedIndex].text;render()};search.oninput=render;document.getElementById('clear').onclick=()=>{scope.value='h1';search.value='';causeFilter.value='';evidenceFilter.value='';functionFilter.value='';scope.onchange()};document.querySelectorAll('[data-cause]').forEach(b=>b.onclick=()=>choose(events.filter(r=>activeCauses(r).includes(b.dataset.cause)),names[b.dataset.cause]));for(const [key,title] of Object.entries(names)){const option=make('option',title,causeFilter);option.value=key}
causeFilter.onchange=()=>{if(genericNames[causeFilter.value]&&level.value==='concrete'){level.value='all';drawCauseMatrix();redrawFunctions();refreshGroups()}render()};evidenceFilter.onchange=render;
const groupMatch=(r,k)=>k==='mixed'?ai(r)&&activeCauses(r).some(c=>!c.startsWith('ai_')):k==='ai-only'?ai(r)&&activeCauses(r).every(c=>c.startsWith('ai_')):k==='other-only'?activeCauses(r).length&&!ai(r):k==='multiple'?activeCauses(r).length>1:!activeCauses(r).length;
function drawReasonViews(){
 const container=document.getElementById('reason-bars');if(!container)return;
 const selector=document.getElementById('reason-mode');if(selector)selector.value=level.value;
 const counts=new Map();for(const r of events)for(const c of activeCauses(r))counts.set(c,(counts.get(c)||0)+1);
 const sorted=[...counts].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]));const max=Math.max(...counts.values());
 container.replaceChildren();
 for(const [c,n] of sorted){const row=make('div',null,container,'reason-row');row.dataset.causeKey=c;
 const top=make('div',null,row,'reason-label');make('span',names[c],top);const button=make('button',String(n),top);button.type='button';button.setAttribute('aria-label',names[c]+': '+n+(es?' anuncios; ver registros':' announcements; view records'));button.onclick=()=>choose(events.filter(r=>activeCauses(r).includes(c)),names[c]);
 const track=make('div',null,row,'mobile-track');track.setAttribute('aria-hidden','true');make('div',null,track).style.width=(n/max*100)+'%';}
 const count=events.filter(r=>activeCauses(r).length).length;
 document.getElementById('reason-basis').textContent=(es?'Explicaciones de ':'Explanations from ')+count+(es?' de 228 anuncios. Escala común: 0–':' of 228 announcements. Shared scale: 0–')+max+'.';
 for(const ext of ['svg','png'])document.getElementById('reason-download-'+ext).href='assets/'+(level.value==='all'?'all-reasons':'mechanisms')+'.'+ext;
 const pairs=new Map();for(const r of events){const cs=activeCauses(r);for(const a of cs.filter(c=>c.startsWith('ai_')))for(const b of cs.filter(c=>!c.startsWith('ai_'))){const key=a+'|'+b;pairs.set(key,(pairs.get(key)||0)+1)}}
 const ranking=[...pairs].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]));const cutoff=ranking[Math.min(4,ranking.length-1)]?.[1]||0;
 const list=document.getElementById('ai-pairs');list.replaceChildren();
 for(const [key,n] of ranking.filter(x=>x[1]>=cutoff)){const [a,b]=key.split('|');const row=make('li',null,list);row.dataset.pair=key;const text=make('span',null,row);make('span',names[a],text);make('span',' + '+names[b],text);const button=make('button',String(n),row);button.type='button';button.setAttribute('aria-label',names[a]+' + '+names[b]+': '+n+(es?' anuncios; ver registros':' announcements; view records'));button.onclick=()=>choose(events.filter(r=>activeCauses(r).includes(a)&&activeCauses(r).includes(b)),names[a]+' + '+names[b]);}
 document.getElementById('pair-basis').textContent=document.getElementById('reason-bars')?(es?'Todas las razones atribuidas.':'All attributed reasons.'):level.value==='all'?(es?'Incluye cambios descritos y razones generales.':'Includes described changes and general reasons.'):(es?'Solo cambios descritos.':'Described changes only.');
}
const reasonSelector=document.getElementById('reason-mode');if(reasonSelector)reasonSelector.onchange=()=>{level.value=reasonSelector.value;level.onchange()};
function refreshGroups(){
 drawReasonViews();
 document.querySelectorAll('[data-current-basis]').forEach(p=>p.textContent=(es?'Vista de los botones y matrices: ':'Buttons and matrices: ')+level.options[level.selectedIndex].textContent);
 const labels=es?{mixed:'IA y otra explicación','ai-only':'Solo explicaciones de IA','other-only':'Solo otras explicaciones',none:'Sin explicación en esta vista',multiple:'Más de una explicación'}:{mixed:'AI and another explanation','ai-only':'Only AI explanations','other-only':'Only other explanations',none:'No explanation in this view',multiple:'More than one explanation'};
 document.querySelectorAll('[data-group]').forEach(b=>{b.textContent=labels[b.dataset.group]+' · '+events.filter(r=>groupMatch(r,b.dataset.group)).length;b.onclick=()=>choose(events.filter(r=>groupMatch(r,b.dataset.group)),b.textContent)});
}
document.querySelectorAll('[data-status]').forEach(b=>b.onclick=()=>{if(b.dataset.status==='generic'){level.value='all';drawCauseMatrix();redrawFunctions();refreshGroups()}choose(events,b.textContent);evidenceFilter.value=b.dataset.status;render()});
const functionMatrix=document.getElementById('function-matrix');
if(functionMatrix){
const groupDefs=[['mixed',es?'IA y otra causa':'AI + other'],['ai-only',es?'Solo IA registrada':'Only AI recorded'],['other-only',es?'Solo otras causas':'Only other causes'],['none',es?'Sin explicación en esta vista':'No explanation in this view']];

const rowKeys=Object.keys(fnNames).sort((a,b)=>events.filter(r=>fnMatch(r,b)).length-events.filter(r=>fnMatch(r,a)).length).concat('unknown');
function matrixFunctions(){
 const detailed=document.getElementById('function-matrix-mode').value==='causes';
 const defs=detailed?[...Object.entries(names).filter(([k])=>level.value==='all'||!genericNames[k]),['none',es?'Sin explicación en esta vista':'No explanation in this view']]:groupDefs;
 const match=(r,k)=>detailed?(k==='none'?!activeCauses(r).length:activeCauses(r).includes(k)):groupMatch(r,k);
 functionMatrix.replaceChildren();const thead=make('thead',null,functionMatrix);const tr=make('tr',null,thead);make('th',es?'Función afectada':'Affected function',tr).scope='col';
 for(const [key,title] of [['total',es?'Registros':'Records'],...defs]){const th=make('th',title,tr);th.scope='col'}
 const tbody=make('tbody',null,functionMatrix);
 for(const f of rowKeys){const tr=make('tr',null,tbody);make('th',f==='unknown'?unknown:fnNames[f],tr).scope='row';
 for(const [key,title] of [['total',es?'Todas las explicaciones':'All explanations'],...defs]){const g=events.filter(r=>fnMatch(r,f)&&(key==='total'||match(r,key)));const td=make('td',null,tr);const b=make('button',String(g.length),td);b.type='button';b.disabled=!g.length;b.dataset.count=g.length;b.setAttribute('aria-label',(f==='unknown'?unknown:fnNames[f])+' × '+title+': '+g.length);if(g.length)td.style.background='color-mix(in srgb, var(--accent) '+Math.min(34,5+g.length)+'%, transparent)';b.onclick=()=>choose(g,(f==='unknown'?unknown:fnNames[f])+' × '+title)}}
}
 redrawFunctions=matrixFunctions;document.getElementById('function-matrix-mode').onchange=matrixFunctions;matrixFunctions();
 document.querySelectorAll('[data-work-status]').forEach(b=>b.onclick=()=>choose(events.filter(r=>r.affected_work.status===b.dataset.workStatus),b.textContent));
}
level.onchange=()=>{selected=events;label=es?'Anuncios del primer semestre':'H1 announcement records';scope.value='h1';causeFilter.value='';search.value='';evidenceFilter.value='';functionFilter.value='';drawCauseMatrix();redrawFunctions();refreshGroups();render()};
drawCauseMatrix();refreshGroups();render();
})();
