@echo off
cd /d "%~dp0"

if exist ".venv\" (
    call .venv\Scripts\activate.bat
) else (
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
)

python Main.py