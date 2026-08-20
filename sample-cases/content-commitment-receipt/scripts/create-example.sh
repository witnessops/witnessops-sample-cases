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

"$PYTHON_BIN" "$SAMPLE_DIR/tools/sample_content_commitment.py" commit \
  --artifact "$SAMPLE_DIR/lifecycle/01-pre-disclosure/example-agreement.txt" \
  --artifact-label "example-agreement.txt" \
  --claimed-created-at "2026-08-19T05:30:00Z" \
  --nonce-hex "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f" \
  --receipt "$SAMPLE_DIR/lifecycle/02-public-commitment/receipt.json" \
  --opening-record "$SAMPLE_DIR/lifecycle/01-pre-disclosure/opening-record.json" \
  --force

"$PYTHON_BIN" "$SAMPLE_DIR/tools/sample_content_commitment.py" disclose \
  --receipt "$SAMPLE_DIR/lifecycle/02-public-commitment/receipt.json" \
  --opening-record "$SAMPLE_DIR/lifecycle/01-pre-disclosure/opening-record.json" \
  --disclosure "$SAMPLE_DIR/lifecycle/03-disclosure/disclosure.json" \
  --force

echo "SAMPLE_REGENERATED=PASS"
