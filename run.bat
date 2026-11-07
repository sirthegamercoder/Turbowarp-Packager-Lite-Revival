@echo off

if exist ".venv\" (
    call .venv\Scripts\activate.bat
) else (
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install pywebview lxml pyinstaller
)

python src\Main.py