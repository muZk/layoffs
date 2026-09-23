# Explorar despidos con Python y SQL

[Notebook ejecutable](explorar_despidos.ipynb) · [Resultados en HTML](explorar_despidos.html) · [Paquete independiente con datos](ejemplo-exploratorio.zip)

Una exploración de 228 anuncios de enero–junio de 2026. Explica la procedencia y el alcance de los datos, cuenta razones, cruza explicaciones vinculadas a IA, consulta fuentes y analiza funciones y vacíos. No presupone haber leído otro artículo.

## Usarlo de forma independiente

Descomprimir `ejemplo-exploratorio.zip` y abrir `explorar_despidos.ipynb` en Jupyter o un editor compatible. El paquete contiene:

```text
explorar_despidos.ipynb
explorar_despidos.html
requirements.txt
data/normalized/
data/company-history.json
```

Elegir un kernel Python con pandas y matplotlib y ejecutar **Run All**. Los resultados ya están guardados como ejemplo. No necesita internet, credenciales, el JSON canónico ni los artículos del repositorio. SQLite se abre en modo de solo lectura.

El notebook busca `data/normalized/` o `normalized/` desde la carpeta de trabajo y sus carpetas superiores. También se puede configurar `DATA_DIR` en la primera celda de código.

`requirements.txt` recoge las versiones con las que se ejecutó. Para instalar ese entorno: `python -m pip install -r requirements.txt` dentro del paquete. Se necesita una interfaz compatible con notebooks para la ejecución interactiva; el HTML puede leerse sin ella.

## Qué se comprueba

Los hashes de SQLite y CSV se comparan con el manifest. Las frecuencias y todos los pares de razones se calculan independientemente con pandas y SQL; también se comprueban IDs únicos y cobertura. Estas comprobaciones detectan inconsistencias de cálculo, no demuestran causalidad ni corrigen las limitaciones de las fuentes.

La ejecución se comprobó en una carpeta aislada que contenía únicamente los datos normalizados. La cobertura externa sigue siendo la documentada en el manifest: ejecutar hoy no actualiza los anuncios.

## Actualizar datos y resultados

Al recibir una exportación nueva, reemplazar toda la carpeta `data/normalized/`, incluido su manifest, y volver a ejecutar. Dentro del repositorio, la exportación puede regenerarse con `python3 scripts/build_normalized.py` después de validar la base con `python3 scripts/validate_causes.py`.

Los resultados guardados y el HTML son snapshots. Para regenerarlos desde la carpeta del notebook:

```sh
python -m jupyter nbconvert --to notebook --execute --inplace explorar_despidos.ipynb
python -m jupyter nbconvert --to html explorar_despidos.ipynb
```

El HTML contiene resultados y código, pero no ejecuta consultas nuevas.

## Evidencia y crecimiento histórico

Las secciones 10–14 permiten revisar autorías, negaciones, ejemplos, Oracle y vacíos con enlaces a las fuentes. Las secciones 15–16 recalculan crecimiento y sensibilidad desde `data/company-history.json`, incluido en el paquete. Esta copia procede de `research/hiring/company-history.json`; conserva observaciones fechadas, fuentes, exclusiones y cambios de perímetro. No lee las medianas precalculadas. La sección 17 comprueba valores de referencia para detectar cuándo una actualización exige revisar las afirmaciones publicadas.

[Mapa de afirmaciones y respaldo](respaldo-editorial.md). La reproducción comprueba cálculos; la evidencia cualitativa sigue requiriendo lectura de las fuentes originales.

Para regenerar la entrega dentro del repositorio: `python3 report/build.py` y después `python3 scripts/build_notebooks.py`. El segundo comando copia el historial actualizado, ejecuta el notebook en una carpeta temporal que solo contiene los datos necesarios y regenera HTML y ZIP. La ejecución aislada evita dependencias ocultas de los artículos o de archivos del repositorio.
