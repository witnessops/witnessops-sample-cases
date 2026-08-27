# witnessops-sample-cases

Public sample packages for WitnessOps reviews.

Use these when you want to **inspect an example** before requesting work: what
was checked, which files ship, and what the package does **not** prove.

## For buyers (start here)

1. Open a sample under `sample-cases/`.
2. Read that package's `README.md` (situation, inspect, does not prove).
3. Prefer `BUYER_WALKTHROUGH.md` when present.
4. Run `shasum -a 256 -c MANIFEST.sha256` from the package directory.
5. Treat every sample as **synthetic / labelled** — not live customer evidence.

Public web walkthroughs:

- https://witnessops.com/review/sample-cases
- Signed synthetic compromised-API-key rotation, SBOM minimum-elements check, and related examples

## Authority boundary

This repo presents and organizes sample cases. It does not define schemas,
execute production reviews, sign production receipts, or implement the
canonical internal verifier.

| Concern | Owned here? | Notes |
|---|---:|---|
| Sample READMEs and buyer walkthroughs | Yes | Situation, inspection, and does-not-prove language. |
| Stable sample package paths | Yes | Files exported or authored as public samples. |
| Expected sample verifier outcomes | Yes | Sample-scoped results only. |
| Redaction and sample boundaries | Yes | Explains why evidence is synthetic. |
| Proof-engine source | No | `witnessops-proof-engine`. |
| Canonical internal verifier | No | `witnessops-verifier`; supported public distribution remains unresolved. |
| Contract schemas | No | `witnessops-contracts`. |
| Key registry | No | `witnessops-key-registry`. |
| Private keys or live customer evidence | Never | Must not be committed here. |

## Current sample packages

```text
sample-cases/ai-agent-action-proof-run          # full package — signed synthetic API-key rotation
sample-cases/content-commitment-receipt         # synthetic byte-commitment lifecycle
sample-cases/sbom-cisa-2026-minimum-elements    # full package — SBOM min-elements check
sample-cases/phone-security-proof-pack          # full package — phone security shape
sample-cases/proof-of-record-pipeline           # full package — record pipeline shape
```

`sample-cases/SAMPLE_CASES_MANIFEST.v1.yaml` is the complete inventory of
published package directories under `sample-cases/`. Repository tests require
the manifest and directory inventory to match exactly.

## Planned sample packages

The following paths contain scenario documentation only. Their `package/`
directories are intentionally empty apart from `.gitkeep`, so they are not
published sample packages and are not included in the complete-package
manifest:

```text
privileged-access-approval/pass
privileged-access-approval/partial-missing-removal
privileged-access-approval/fail-scope-mismatch
```

They become current only after the documented manual publication process adds
complete artifacts and a reviewed change updates their status and inventory.

Web presentation is selective: not every GitHub package has a marketing page.
Prefer the site index for buyer entry; use this repo for file-level inspection.

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

Where a full offline verifier is used for imported packages, record the exact
command and refs in that package's docs. Sample signatures are often simulated.

## Controlled publication provenance

Publication is a local, manual operation. The
`scripts/publish_sample_packages_manual.py` command regenerates the three
`privileged-access-approval/*/package` directories from exact pinned Proof
Engine, Verifier, and Contracts commits.

The command:

- requires clean local checkouts at the recorded commits;
- refuses to run on `main`, `master`, or `develop`;
- exports into a temporary directory;
- imports and validates the generated packages;
- runs the sample repository tests;
- writes `PUBLICATION_PROVENANCE.json`; and
- never installs dependencies, reads a GitHub credential, commits, or pushes.

The operator must inspect the resulting diff and publish it through an ordinary
reviewed pull request. This keeps dependency execution separate from repository
write authority and avoids a persistent cross-repository Actions credential.

### Manual publication

1. Create a dedicated publication branch in this repository.
2. Prepare clean local checkouts at these exact commits:
   - `witnessops-proof-engine@24c13c96bc58ebfb51c159e466ba672f44b4d426`
   - `witnessops-verifier@c85fe398eaba915304f71d366e20fc8b144f4d33`
   - `witnessops-contracts@b344ed1610a07fbb8a03d5eff9480765610b89a0`
3. In a temporary Python environment, install the development dependencies
   declared by this repository, Proof Engine, and Verifier.
4. Run:

```bash
python scripts/publish_sample_packages_manual.py \
  --proof-engine-dir /path/to/witnessops-proof-engine \
  --verifier-dir /path/to/witnessops-verifier \
  --contracts-dir /path/to/witnessops-contracts
```

5. Review `git status`, the complete diff, package hashes, and
   `PUBLICATION_PROVENANCE.json`.
6. Commit the generated package paths and provenance together on the
   publication branch, then open a pull request.

The provenance record applies only to the package paths it names and only to
the publication commit that contains it. It does not retroactively attribute
component revisions to existing packages committed before the record existed.

## Publication rule

Do not commit secrets, customer data, production evidence, or private keys.
If package files change, update the relevant hash records and publication
provenance in the same reviewed change.
