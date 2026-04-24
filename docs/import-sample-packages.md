# Import Sample Packages

## Purpose

This guide describes how to import exported sample packages from `witnessops-proof-engine` into `witnessops-sample-cases`.

The import process keeps responsibilities separate:

```text
witnessops-proof-engine
  exports package artifacts

witnessops-sample-cases
  publishes stable sample-case paths

witnessops-verifier
  verifies packages offline

witnessops-contracts
  validates package artifact schemas
```

## Source packages

Export packages from `witnessops-proof-engine`:

```bash
python scripts/export_sample_package.py \
  --fixture pass \
  --output-dir dist/sample-packages \
  --signed \
  --verifier-dir ../witnessops-verifier \
  --contracts-dir ../witnessops-contracts

python scripts/export_sample_package.py \
  --fixture partial_missing_removal \
  --output-dir dist/sample-packages \
  --signed \
  --verifier-dir ../witnessops-verifier \
  --contracts-dir ../witnessops-contracts

python scripts/export_sample_package.py \
  --fixture fail_scope_mismatch \
  --output-dir dist/sample-packages \
  --signed \
  --verifier-dir ../witnessops-verifier \
  --contracts-dir ../witnessops-contracts
```

Expected exported directories:

```text
dist/sample-packages/privileged-access-approval-pass
dist/sample-packages/privileged-access-approval-partial-missing-removal
dist/sample-packages/privileged-access-approval-fail-scope-mismatch
```

## Import command

From the `witnessops-sample-cases` repository:

```bash
python scripts/import_sample_packages.py \
  --source-root ../witnessops-proof-engine/dist/sample-packages \
  --repo-root .
```

This copies packages into:

```text
privileged-access-approval/pass/package
privileged-access-approval/partial-missing-removal/package
privileged-access-approval/fail-scope-mismatch/package
```

## Import validation

The import script requires:

```text
README.md
package_index.json
receipt.json
evidence_manifest.json
verification_result.json
report.md
public_key.json
results/comparison_result.json
evidence/
normalized/
```

It also checks:

```text
verification_result.status = valid
package_index.verification_status matches verification_result.status
package_index.verification_result_source = witnessops_verifier
package_index workflow_class, proof_run_id, and outcome match receipt.json
no *.hex files
no private-key or secret markers
```

## Boundary

Imported sample packages must come from fixture or redacted evidence. Do not import real customer evidence unless a separate publication approval exists.
