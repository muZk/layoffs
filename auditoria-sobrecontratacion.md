# ¿Fue solo corregir la sobre-contratación?

Nota de estado (2026-09-15). Este documento audita la sobre-contratación cuando `over_hiring` todavía era un tag de causa. En el modelo final del dataset, `over_hiring` ya no existe como causa. Sobre-contratación (`hire_overcorrection`) pasó a ser un eje-lente aparte, no una causa. El análisis de dotación que sigue queda como registro histórico de esa auditoría.

Una explicación habitual de los despidos tech de 2026 es que las empresas solo estaban deshaciendo el exceso de contratación de la pandemia. Al reconstruir la dotación de las empresas públicas en dos ventanas, pandemia (FY2020→FY2022) y reciente (2023 hasta antes del corte), la respuesta es que la sobre-contratación no es una sola cosa. Hay al menos tres formas distintas, y como explicación general de 2026 no alcanza.

## Alcance

La dotación reportada (10-K / 20-F) solo existe para empresas públicas. De los 161 despidos, 67 son de empresas públicas; las otras 94 son privadas o adquiridas, sin filings. La sobre-contratación, entonces, nunca es comparable en todo el universo. Se excluyen empresas que dejaron de ser públicas antes del corte, bases muy chicas o roll-ups, y crecimiento por fusión.

## La trayectoria (no un flag)

| Empresa | Pandemia FY20→FY22 | Reciente 2023→hoy | Forma |
|---|---|---|---|
| Block | +127% | −21% | corrigiendo el boom |
| ZoomInfo | +103% | −10% | corrigiendo el boom |
| Upwork | +57% | −21% (bajo su nivel 2020) | corrigiendo el boom |
| Shopify | +66% | −8% (ya cortó en 2022–23) | corrigiendo el boom |
| Coinbase | +261% | bajó y luego +45% | segundo ciclo (cripto) |
| Pinterest | +57% | +31% | siguió creciendo |
| MercadoLibre | +161% | +44% | siguió creciendo |
| Snowflake | +136% | +12% | siguió creciendo |
| Amazon | +19% | +3% | plano |
| Angi | −10% | −26% | nunca infló, se achica |
| Oracle | +6% (ex-Cerner) | −14% | el salto FY23 es Cerner (M&A) |

(Serie de dotación de FY2020, FY2022, FY2023 y la última antes del corte, de los 10-K/20-F. Las empresas públicas sin serie completa quedan sin clasificar; las privadas no tienen filings.)

## Las tres formas

1. Corrigiendo el boom de la pandemia. Block, ZoomInfo, Upwork, Shopify subieron fuerte en 2020-2022 y vienen achicándose desde 2023. El corte de 2026 es el último paso de una corrección que ya llevaba años, no un exceso vigente. Acá "deshacer la sobre-contratación" es real, y la IA es el nombre que se le pone al paso más nuevo.
2. Un segundo ciclo, no resaca de pandemia. Coinbase infló, deshizo ese exceso hacia 2023 y volvió a crecer 45% antes de este corte. Su ritmo lo marca el ciclo cripto, no la pandemia.
3. Nunca hubo exceso que corregir. MercadoLibre, Pinterest y Snowflake siguieron creciendo hasta el corte; Angi se achica desde 2020; Oracle ex-Cerner está plano y su salto de dotación es la compra de Cerner. Para este grupo, "corrigieron la sobre-contratación" simplemente no aplica.

El dato que ordena el conjunto es MercadoLibre. Es el único caso donde la IA queda como causa sin otra explicación, y es de las que más creció (+161% en pandemia, +44% reciente). El caso más limpio de sustitución por IA no es una empresa deshaciendo un exceso, es una que estaba contratando a toda máquina.

## Conclusión

Con la misma ventana para todas las públicas, la sobre-contratación reciente no distingue a las que culparon a la IA de las que no; y vista como trayectoria, es real en un grupo (los que aún deshacen el boom), irrelevante en otro (los que nunca inflaron o siguen creciendo), y un ciclo aparte en un tercero. "Recortaron para deshacer la sobre-contratación" es, igual que "lo hizo la IA", una media verdad que se estira a titular. Es un factor entre varios en cada caso, no la causa por sí sola; por eso no sirve como explicación única ni como comparación.
