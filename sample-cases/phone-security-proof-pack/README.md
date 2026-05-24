# Phone Security Proof Pack Sample

Sample ID: `PHONE_SECURITY_PROOF_PACK_SAMPLE_V1`

Status: `sample_receipt_shape_ready`

## Purpose

This sample shows how WitnessOps can package one phone security check into a bounded client proof pack.

Sample workflow:

1. Client or device owner authorizes one scoped phone security check.
2. Phone security operator performs the device workflow and exports agreed outputs.
3. WitnessOps packages the outputs into an evidence manifest, gap register, receipt, verifier-style result, and challenge path.
4. The buyer receives a safe-claim summary that distinguishes observed outputs from unsupported conclusions.

## Boundary

This sample proves the package shape and local hash-reference mechanics only.

It does not claim spyware detection, absence of compromise, forensic admissibility, production deployment, legal compliance, source-system honesty, or whole-device assurance.

The receipt signature is simulated. The verifier result is sample-only and should not be represented as a production verification.

## Bundle

| File | Purpose |
|---|---|
| `AUTHORITY_MAP.json` | Names client authority, phone operator authority, proof-pack authority, and negative boundaries |
| `ACTION_BOUNDARY.json` | States what the proof-pack example is allowed and blocked from claiming |
| `artifacts/device_check_summary.md` | Synthetic device-check summary used as the sample input |
| `SAMPLE_DELIVERABLE_PLAN.md` | Buyer-facing proof-pack plan for a first pilot offer |
| `EVIDENCE_MANIFEST.json` | Evidence list, hashes, custody boundary, and failure states |
| `RECEIPT.json` | Portable receipt for the sample proof-pack event |
| `VERIFY_RESULT.json` | Sample verifier-style result and stated limitations |
| `CHALLENGE_PATH.md` | Third-party inspection and challenge path |
| `MANIFEST.sha256` | Local hash manifest for this sample bundle |

## Commercial Point

WitnessOps gives a phone security operator a client-readable proof pack: what was checked, what outputs were captured, what remains unproven, and what the client can safely repeat afterwards.
