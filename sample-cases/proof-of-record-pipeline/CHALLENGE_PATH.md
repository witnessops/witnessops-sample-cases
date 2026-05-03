# Challenge Path: Proof-Of-Record Pipeline Sample

## Local file-integrity challenge

From this directory:

```bash
shasum -a 256 -c MANIFEST.sha256
```

Expected result: every listed file returns `OK`.

## Receipt-reference challenge

Inspect `RECEIPT.json` and confirm it references:

```text
AUTHORITY_MAP.json
ACTION_BOUNDARY.json
CANONICAL_PAYLOAD.json
EVIDENCE_MANIFEST.json
VERIFY_RESULT.json
CHALLENGE_PATH.md
MANIFEST.sha256
```

## Evidence challenge

Inspect `EVIDENCE_MANIFEST.json` and confirm each listed `path` exists locally.

Then recompute SHA-256 for each listed file and compare it with the manifest entry.

## Boundary challenge

Inspect `AUTHORITY_MAP.json`, `ACTION_BOUNDARY.json`, and `VERIFY_RESULT.json`.

The sample must stay within these boundaries:

```text
record evidence only
sample-only source artifact
no production deployment claim
no source-system honesty claim
no legal compliance claim
no live-system or customer-data claim
```

## Failure challenge

A challenger should fail this sample if any of the following are true:

```text
MANIFEST.sha256 does not match local files
EVIDENCE_MANIFEST.json references a missing file
RECEIPT.json references a missing file
RECEIPT.json claims production action
VERIFY_RESULT.json removes the sample limitations
```

## Authority boundary

This repository stores the sample package. It does not execute the proof run, define canonical schemas, operate the verifier, or govern key registry authority.
