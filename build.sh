#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")"
source .venv/bin/activate
python3 compile.py