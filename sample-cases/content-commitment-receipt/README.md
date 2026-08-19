# Synthetic Content Commitment Receipt

Sample ID: `CONTENT_COMMITMENT_RECEIPT_SAMPLE_V1`

Status: `SYNTHETIC / EDUCATIONAL / NONCANONICAL`

## Situation

An operator has an artifact that should remain undisclosed for a period of time. The operator publishes a salted SHA-256 commitment, then later discloses the artifact and nonce so another person can reproduce the commitment comparison.

This public sample includes every lifecycle stage so the complete mechanism can be inspected. In a real pre-disclosure run, the artifact and opening record would not be published until intentional disclosure.

## Inspect

| Path | Purpose |
|---|---|
| `lifecycle/01-pre-disclosure/example-agreement.txt` | Synthetic artifact bytes |
| `lifecycle/01-pre-disclosure/opening-record.json` | Synthetic nonce and operator diagnostic |
| `lifecycle/02-public-commitment/receipt.json` | Receipt that can be published before disclosure |
| `lifecycle/03-disclosure/disclosure.json` | Nonce disclosed later to open the commitment |
| `FORMAT.md` | Exact sample-local byte encoding and test vector |
| `CLAIM_BOUNDARY.md` | Supported and unsupported propositions |
| `schema/sample-receipt-v1.schema.json` | Sample-local structural fixture; not a canonical WitnessOps schema |
| `tools/sample_content_commitment.py` | Dependency-free sample demonstrator |
| `MANIFEST.sha256` | Hash inventory for this directory |

## Run

From this sample directory:

```bash
sh validate-sample.sh
```

Expected bounded result:

```text
COMMITMENT_MATCH=PASS
TIME_EVIDENCE=NOT_PRESENT
VERDICT=SAMPLE_CONTENT_COMMITMENT_MATCH
SAMPLE_VALIDATION=PASS
```

On Windows PowerShell:

```powershell
.\scripts\verify-example.ps1
```

## What the successful comparison shows

The supplied artifact bytes and disclosed nonce reproduce the commitment recorded in the supplied synthetic receipt under the declared sample-local scheme.

## What it does not prove

- truth of statements inside the artifact;
- authorship or operational authority;
- confidentiality before disclosure;
- first creation time;
- independent timestamping;
- safety of opening the artifact;
- production WitnessOps verifier acceptance;
- conformance with canonical `witnessops-contracts` schemas.

The fixed `claimed_created_at` value is reconstruction metadata, not timestamp evidence. `TIME_EVIDENCE=NOT_PRESENT` is therefore the expected result.

## Authority boundary

`WITNESSOPS-SAMPLE-CONTENT-COMMITMENT-V1` belongs only to this synthetic sample. It does not create an organization-wide protocol, contract, verifier, product, or supported public distribution.

Canonical schema authority remains in `witnessops-contracts`. Canonical internal verifier authority remains in `witnessops-verifier`.

## Regeneration

The included example uses a fixed nonce and timestamp so regeneration is deterministic:

```bash
sh scripts/create-example.sh
sh validate-sample.sh
```

For an unscripted experiment, omit `--nonce-hex`; the sample utility then obtains a fresh nonce from the operating system's cryptographically secure random generator.
