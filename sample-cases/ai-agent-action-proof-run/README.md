# AI Agent Action Proof Run Sample

Sample ID: `AI_AGENT_ACTION_PROOF_RUN_SAMPLE_V1`

Status: `sample_receipt_shape_ready`

## Purpose

This sample shows how WitnessOps packages one consequential AI-agent-assisted workflow into a portable proof bundle.

Sample workflow:

1. AI agent proposes a bounded code/config change.
2. Human approver grants a scoped approval.
3. Agent/tool performs the bounded action.
4. Evidence is captured.
5. Receipt is signed or simulated.
6. Verifier reports pass/fail.
7. Challenge path explains what a third party can inspect.

## Boundary

This sample proves the receipt shape and verifier path only.

It does not claim production deployment, legal compliance, or complete AI governance coverage.

The receipt signature is simulated. The verifier result is sample-only and should not be represented as a production verification.

## Bundle

| File | Purpose |
|---|---|
| `AUTHORITY_MAP.json` | Who approved, who/what acted, and which boundary controlled the action |
| `ACTION_BOUNDARY.json` | What the agent/tool was allowed and blocked from doing |
| `EVIDENCE_MANIFEST.json` | Which proof artifacts are included |
| `RECEIPT.json` | Portable receipt for the action |
| `VERIFY_RESULT.json` | Sample verifier result and limitations |
| `CHALLENGE_PATH.md` | Third-party inspection and challenge path |
| `MANIFEST.sha256` | Local hash manifest for this sample bundle |

## Commercial Point

WitnessOps gives enterprises a receipt they can verify after an AI agent acts.

