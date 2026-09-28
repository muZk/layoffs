# Preguntas de lectores y contraste con la colección

Consulta exploratoria: 23 de septiembre de 2026. Objetivo: orientar un artículo a preguntas presentes en conversaciones públicas, sin declararlas falsas de antemano.

## Alcance y método

Búsquedas web en Reddit y Hacker News: `site.reddit.com layoffs.fyi AI overhiring layoffs productivity`, `site.news.ycombinator.com layoffs.fyi AI layoffs`, `site.reddit.com layoffs.fyi fake numbers hiring outsourcing`, y consultas con la cadena exacta `layoffs.fyi` combinada con `2026`, `hiring`, `offshoring` y `engineers`. Las primeras consultas fueron dirigidas por hipótesis previas; las siguientes ampliaron temas. No es una muestra representativa ni exhaustiva. No permite medir cuáles son los mitos más frecuentes. No se autenticó la identidad humana de los autores; puede haber contenido sintético o promocional. No se usaron votos como estimación de prevalencia. No se investigaron X o GitHub en esta ronda.

Se leyeron páginas de Reddit y comentarios accesibles; dos aperturas de HN fallaron y sus resultados se usan solo como pistas, no como base del contraste. Algunas conversaciones son anteriores a 2026: sirven para identificar argumentos, no para demostrar hechos de 2026. Nuestro contraste utiliza exclusivamente los 228 anuncios H1 de la exportación revisada el 17 de septiembre y las series históricas asociadas; no refuta afirmaciones sobre otras poblaciones o períodos.

## Conversaciones consultadas

- [R1: Sobrecontratación, IA y Wall Street](https://www.reddit.com/r/cscareerquestions/comments/1ojz15y/companies_didnt_fire_people_because_of_ai_ai_has/). Apertura y comentarios accesibles. Argumentos contrapuestos sobre crecimiento pasado, rentabilidad, traslado de trabajo y contratación. No tomar las afirmaciones económicas de los participantes como hechos.
- [R2: ¿Por qué despedir si aumenta la productividad?](https://www.reddit.com/r/theprimeagen/comments/1t5qdd8/do_layoffs_citing_ais_productivity_boost_make_any/). Apertura y comentarios accesibles. También aparece financiar el costo de IA, en vez de sustituir tareas. El crosspost en BetterOffline no cuenta como conversación independiente.
- [R3: Carga de trabajo tras los recortes](https://www.reddit.com/r/Layoffs/comments/1v03m5m/is_ai_reducing_anyones_workload_or_is_it_mostly/). Relato de segunda mano; no verificado como evento. Sirve para formular una pregunta sobre los equipos restantes.
- [R4: ¿Dónde trabajar como SWE?](https://www.reddit.com/r/levels_fyi/comments/1up8e2h/where_should_i_work_as_a_swe_in_2026_compensation/). Usa Layoffs.fyi para plantear estabilidad y compensación; la publicación presenta además su propia visualización. No asumir que refleja a todos los trabajadores.
- [R5: ¿Menos despidos equivale a recuperación?](https://www.reddit.com/r/cscareerquestions/comments/18a0vbu/layoffsfyi_shows_theres_less_layoffs_as_a_whole/). Conversación de diciembre de 2023: contratación, salarios y empleo neto. No usar sus testimonios como evidencia de 2026.
- [Pista HN: titulares y tendencias](https://news.ycombinator.com/item?id=47380405). Solo extracto de buscador; apertura fallida.
- [Pista HN: gasto IA y recortes](https://news.ycombinator.com/item?id=39002001). Solo extracto de buscador; apertura fallida.

## Contraste editorial

| Pregunta / argumento observado | Resultado en nuestros datos | Veredicto y uso |
|---|---|---|
| Es solo una corrección de contratación pandémica (R1) | Crecimiento mediano 2019–22: IA 79,8% (15), otras 50,9% (18); 2022–25: 3,7% (28) y 4,7% (38). 12/28 IA ya se contraían. Muestra constante reciente: 3,5% y 5,2%, 15 empresas por grupo. | Matiza, no refuta sobrecontratación. Cambiar plantilla no mide exceso respecto del negocio. Prioridad alta. |
| Si es ahorro, IA es una excusa (R1/R2) | 48/72 anuncios con IA también registran otros motivos; productividad + ahorro en 12. | Ahorro y uso de IA no son excluyentes. Coexistencia no prueba sinceridad ni engaño. Prioridad alta. |
| Despedir por IA significa automatizar los puestos (R2, debate sobre otras vías) | Productividad 24, sustitución 8, inversión 14, disrupción del mercado 7; categorías solapadas. | La definición estrecha no cubre las explicaciones registradas. Ejemplos: Block, Atlassian, Tailwind. Prioridad alta. |
| Se despide para pagar IA, no por productividad (R2) | Inversión atribuida en 14; destinos incluyen productos y puestos, no solo centros de datos. | Vía documentada, no explicación universal; no conocemos montos reasignados. Integrar con el tema anterior. |
| Productividad significa que los restantes absorben más trabajo (R3) | 24 atribuciones de productividad, 22 empresariales; no medición sistemática posterior. | No resoluble con anuncios. Seguimiento o entrevistas, no titular de hallazgo. |
| Es traslado de trabajo, no automatización (R1) | 9 anuncios con work_relocation: también hay traslados dentro de país y regreso a EEUU. | Casos inspeccionables; no estiman offshoring ni permiten descartarlo por baja frecuencia. Tema secundario. |
| Menos despidos significa mejor mercado / más empleos (R5) | No tenemos contrataciones y salidas totales de 2026 ni población de empresas sin despidos. | El indicador no responde empleo neto. Nota de lectura, no resultado nuevo. |
| ¿Qué empresa o profesión es segura? ¿Protege la rentabilidad? (R4) | Funciones conocidas en 60/228; sin beneficios y exposición homogéneos, ni modelo de riesgo. | Preocupación importante, fuera de capacidad actual. No fabricar ranking. |

## Recomendación

Organizar el artículo en torno a sobrecontratación, ahorro/IA como falsa disyuntiva y distintas vías de relación con IA. Integrar financiación de nuevas apuestas dentro de esas vías. Conservar estabilidad, carga de trabajo y empleo neto como preguntas para investigación adicional, sin convertir la ausencia de datos en un hallazgo central. Las negaciones no justifican una sección principal.

Cálculos: `../../notebooks/explorar_despidos.html` (grupos, atribuciones, contratación y sensibilidad); `../../data/normalized/layoffs.sqlite` (`announcement_causes`, `announcements`); `../hiring/summary.json`, `../hiring/sensitivity.json`. El material social no cambia clasificaciones de eventos y no verifica las explicaciones empresariales.
