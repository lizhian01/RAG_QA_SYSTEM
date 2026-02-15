$ROOT = Split-Path $PSScriptRoot -Parent
Set-Location -Path $ROOT

if (-not (Test-Path "$ROOT\.venv")) {
    python -m venv "$ROOT\.venv"
}

. "$ROOT\.venv\Scripts\Activate.ps1"
pip install -r "$ROOT\rag_app\requirements.txt"

python "$ROOT\rag_app\scripts\extract_pdf.py"
python "$ROOT\rag_app\ingest.py"
python "$ROOT\rag_app\query.py" --query "如何解除死锁？"
