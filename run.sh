#!/usr/bin/env sh
set -eu

if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    python3 -m venv .venv
    source .venv/bin/activate
    pip install pywebview lxml pyinstaller
fi

python3 src/Main.py