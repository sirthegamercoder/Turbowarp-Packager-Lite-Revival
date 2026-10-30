#!/usr/bin/env sh
set -eu

if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r src/requirements.txt
fi

python3 src/Main.py