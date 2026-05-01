# Proof-Of-Record Pipeline Sample

Sample ID: `PROOF_OF_RECORD_PIPELINE_SAMPLE_V1`

Status: `sample_receipt_shape_ready`

## Purpose

This sample shows how WitnessOps can package one connector-observed artifact into a bounded Proof-Of-Record bundle.

Sample workflow:

1. A connector emits a bounded event for one observed artifact.
2. The artifact is normalized into a canonical payload.
3. The payload hash is recorded in an evidence manifest.
4. The receipt references the manifest, authority boundary, and challenge path.
5. The verifier result reports sample checks and explicit limitations.

## Boundary

This sample proves the package shape and local hash-reference mechanics only.

It does not claim source-system honesty, production deployment, legal compliance, or full governance approval.

The receipt signature is simulated. The verifier result is sample-only and should not be represented as a production verification.

## Bundle

| File | Purpose |
|---|---|
| `AUTHORITY_MAP.json` | Names the record-only authority boundary and operator scope |
| `ACTION_BOUNDARY.json` | States what the pipeline is allowed and blocked from doing |
| `CONNECTOR_EVENT.json` | Sample connector event used as the observed input |
| `CANONICAL_PAYLOAD.json` | Normalized record payload with artifact hash and subject metadata |
| `EVIDENCE_MANIFEST.json` | Evidence list, hashes, custody boundary, and failure states |
| `RECEIPT.json` | Portable receipt for the Proof-Of-Record event |
| `VERIFY_RESULT.json` | Sample verifier result and stated limitations |
| `CHALLENGE_PATH.md` | Third-party inspection and challenge path |
| `MANIFEST.sha256` | Local hash manifest for this sample bundle |
| `artifacts/source_artifact.md` | Synthetic source artifact captured by the connector event |

## Commercial Point

WitnessOps gives enterprises a portable receipt for a record that can be inspected, challenged, and replayed against the included evidence boundary.
