"""Execute the two published notebooks using only their required inputs."""
from pathlib import Path
import shutil
import tempfile
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ('explorar_despidos', 'exploracion_hallazgos')
INPUTS = (
    'research/hiring/company-history.json',
    'research/hiring/industry-review.json',
    'research/ai-tracker-comparison/layoffs-fyi-ai-2026-09-28.json',
    'research/ai-tracker-comparison/consistency-review.json',
)
with tempfile.TemporaryDirectory(prefix='layoffs-notebooks-') as tmp:
    work = Path(tmp)
    shutil.copytree(ROOT / 'data/normalized', work / 'data/normalized')
    shutil.copytree(ROOT / 'notebooks/data/fonts', work / 'notebooks/data/fonts')
    for relative in INPUTS:
        target = work / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    for name in NOTEBOOKS:
        path = ROOT / 'notebooks' / (name + '.ipynb')
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        NotebookClient(notebook, timeout=180, kernel_name='python3',
                       resources={'metadata': {'path': str(work / 'notebooks')}}).execute()
        nbformat.write(notebook, path)
        path.with_suffix('.html').write_text(HTMLExporter().from_notebook_node(notebook)[0])
        print(f'{name}: execution and HTML complete')
