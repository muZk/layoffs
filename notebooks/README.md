# Análisis exploratorio

| Notebook | Pregunta | Resultado ejecutado |
|---|---|---|
| [explorar_despidos.ipynb](explorar_despidos.ipynb) | ¿Qué contienen los anuncios, cómo contar las razones y cómo revisar su evidencia? | [HTML](explorar_despidos.html) |
| [exploracion_hallazgos.ipynb](exploracion_hallazgos.ipynb) | ¿Qué cambia al cruzar razones, funciones, plantilla e industrias? | [HTML](exploracion_hallazgos.html) |

El primero es la entrada principal. El segundo conserva comparaciones exploratorias, sensibilidades y límites; no convierte cada diferencia encontrada en un resultado confirmatorio. Ambos contienen código y resultados. Los HTML permiten leerlos sin Jupyter.

## Ejecutar

Desde la raíz del repositorio:

```sh
python3 -m pip install -r notebooks/requirements.txt
python3 scripts/validate_causes.py
python3 scripts/build_normalized.py
python3 scripts/build_notebooks.py
```

También se pueden abrir los `.ipynb` y ejecutar todas las celdas desde `notebooks/`. El generador prueba ambos en una carpeta temporal con los insumos mínimos y actualiza notebook y HTML. No usa los artículos ni modifica los insumos de investigación.

## Dependencias

- `data/normalized/`: tablas, SQLite y manifest con hashes.
- `research/hiring/company-history.json`: observaciones de plantilla, fechas, fuentes y exclusiones.
- `research/hiring/industry-review.json`: decisiones y fuentes de la clasificación exploratoria de industrias.
- `research/ai-tracker-comparison/`: snapshot del tracker y decisiones para compararlo.
- `notebooks/data/fonts/`: Lato y su licencia, para reproducir el estilo de los gráficos.

Los insumos se mantienen en una sola ubicación. No hay copias JSON adicionales dentro de `notebooks/data/`. Los notebooks nuevos de hallazgos editoriales y los PDF permanecen locales y no forman parte de esta entrega.

## Qué verifica la ejecución

El notebook principal comprueba hashes, IDs, frecuencias, pares y recuentos de referencia. El de comparaciones reproduce cruces y sensibilidades. Pasar estas comprobaciones demuestra consistencia de cálculo, no causalidad, representatividad ni veracidad independiente de las fuentes. Ejecutar hoy no amplía la cobertura fechada de los datos.
