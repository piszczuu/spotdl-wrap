cd /D "%~dp0"
if not exist .venv\ (
    python -m venv .venv
)
venv/Scripts/activate.bat
pip install dependencies.txt
py ./main.py