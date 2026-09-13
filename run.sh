#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
fi

python3 Main.py