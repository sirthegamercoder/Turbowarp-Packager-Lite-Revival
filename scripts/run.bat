@echo off

if exist ".venv\" (
    call .venv\Scripts\activate.bat
) else (
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r src\requirements.txt
)

python src\Main.py