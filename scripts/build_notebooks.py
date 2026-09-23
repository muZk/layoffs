"""Execute the independent notebook in an isolated directory and package its inputs."""
from pathlib import Path
import shutil, tempfile, zipfile
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
ROOT=Path(__file__).resolve().parents[1]
N=ROOT/'notebooks'
(N/'data').mkdir(exist_ok=True)
shutil.copy2(ROOT/'research/hiring/company-history.json',N/'data/company-history.json')
with tempfile.TemporaryDirectory(prefix='layoffs-notebook-') as tmp:
    work=Path(tmp)
    shutil.copytree(ROOT/'data/normalized',work/'data/normalized')
    shutil.copy2(N/'data/company-history.json',work/'data/company-history.json')
    nb=nbformat.read(N/'explorar_despidos.ipynb',as_version=4)
    NotebookClient(nb,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(work)}}).execute()
    nbformat.write(nb,N/'explorar_despidos.ipynb')
    (N/'explorar_despidos.html').write_text(HTMLExporter().from_notebook_node(nb)[0])
with zipfile.ZipFile(N/'ejemplo-exploratorio.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in ['explorar_despidos.ipynb','explorar_despidos.html','README.md','requirements.txt','respaldo-editorial.md']:
        z.write(N/name,name)
    z.write(N/'data/company-history.json','data/company-history.json')
    for p in sorted((ROOT/'data/normalized').iterdir()):
        if p.is_file():z.write(p,p.relative_to(ROOT))
print('Notebook ejecutado en aislamiento, HTML y paquete regenerados.')
