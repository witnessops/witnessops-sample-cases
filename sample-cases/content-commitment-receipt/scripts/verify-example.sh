#!/usr/bin/env sh
set -eu

SAMPLE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN=python
else
  echo "Python 3.9 or newer is required" >&2
  exit 2
fi

"$PYTHON_BIN" "$SAMPLE_DIR/tools/sample_content_commitment.py" verify \
  --artifact "$SAMPLE_DIR/lifecycle/01-pre-disclosure/example-agreement.txt" \
  --receipt "$SAMPLE_DIR/lifecycle/02-public-commitment/receipt.json" \
  --disclosure "$SAMPLE_DIR/lifecycle/03-disclosure/disclosure.json"
