# witnessops-sample-cases

Public sample packages for WitnessOps reviews.

Use these when you want to **inspect an example** before requesting work: what was checked, which files ship, and what the package does **not** prove.

## For buyers (start here)

1. Open a sample under `sample-cases/`.
2. Read that package’s `README.md` (situation, inspect, does not prove).
3. Prefer `BUYER_WALKTHROUGH.md` when present.
4. Run `shasum -a 256 -c MANIFEST.sha256` from the package directory.
5. Treat every sample as **synthetic / labelled** — not live customer evidence.

Public web walkthroughs (buyer chrome):

- https://witnessops.com/review/sample-cases
- AI agent change package, SBOM minimum-elements check, and related examples

## Authority boundary

This repo presents and organizes sample cases. It does not define schemas, execute production reviews, sign production receipts, or implement the offline verifier.

| Concern | Owned here? | Notes |
|---|---:|---|
| Sample READMEs and buyer walkthroughs | Yes | Situation, inspect, does-not-prove language |
| Stable sample package paths | Yes | Files exported or authored as public samples |
| Expected sample verifier outcomes | Yes | Sample-scoped results only |
| Redaction / sample-boundary notes | Yes | Why evidence is synthetic |
| Proof-engine source | No | `witnessops-proof-engine` |
| Offline verifier | No | `witnessops-verifier` |
| Contract schemas | No | `witnessops-contracts` |
| Key registry | No | `witnessops-key-registry` |
| Private keys or live customer evidence | Never | Must not be committed here |

## Current sample packages

```text
sample-cases/ai-agent-action-proof-run          # full package — AI agent change
sample-cases/sbom-cisa-2026-minimum-elements    # full package — SBOM min-elements check
sample-cases/phone-security-proof-pack          # full package — phone security shape
sample-cases/proof-of-record-pipeline           # full package — record pipeline shape
privileged-access-approval/pass                 # outcome demo (pass)
privileged-access-approval/partial-missing-removal
privileged-access-approval/fail-scope-mismatch
```

Web presentation is selective: not every GitHub package has a marketing page. Prefer the site index for buyer entry; use this repo for file-level inspection.

## What samples can show

```text
package file layout
authority and action boundary language
evidence manifest shape
receipt and sample verifier-result shape
named gaps and challenge path
local hash (MANIFEST.sha256) checks
```

## What samples cannot show

```text
live customer evidence
production signing-key custody
source-system honesty
compliance or audit certification
client environment security as a whole
```

## Local verification

```bash
cd sample-cases/<package>
shasum -a 256 -c MANIFEST.sha256
```

Where a full offline verifier is used for imported packages, record the exact command and refs in that package’s docs. Sample signatures are often **simulated**.

## Publication rule

Do not commit secrets, customer data, production evidence, or private keys.  
If package files change, update `MANIFEST.sha256` and any hash references in the same change.
