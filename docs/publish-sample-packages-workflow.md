# Manual Sample Package Publication

## Purpose

`scripts/publish_sample_packages_manual.py` is the controlled local path for
regenerating public sample packages from private/internal WitnessOps source
repositories. It is not a GitHub Actions workflow and has no repository-write
or credential path.

The separation is deliberate:

```text
local pinned source checkouts
  generate and verify packages

witnessops-sample-cases publication branch
  receives validated package files and provenance

reviewed pull request
  is the only repository publication action
```

## Required local inputs

The operator must provide clean local checkouts at these exact commits:

```text
witnessops-proof-engine@24c13c96bc58ebfb51c159e466ba672f44b4d426
witnessops-verifier@c85fe398eaba915304f71d366e20fc8b144f4d33
witnessops-contracts@b344ed1610a07fbb8a03d5eff9480765610b89a0
```

The sample-cases checkout must also be clean and on a dedicated branch. The
command refuses `main`, `master`, and `develop`.

## Publication sequence

```text
assert clean checkouts
assert exact source commits
export packages into a temporary directory
import packages into stable sample paths
validate package schemas and expected outcomes
run the sample repository tests
write PUBLICATION_PROVENANCE.json
stop without committing or pushing
operator reviews the complete diff
operator opens a publication pull request
```

Run from the sample-cases checkout:

```bash
python scripts/publish_sample_packages_manual.py \
  --proof-engine-dir /path/to/witnessops-proof-engine \
  --verifier-dir /path/to/witnessops-verifier \
  --contracts-dir /path/to/witnessops-contracts
```

Dependency installation is an explicit operator precondition. The command does
not install packages or access GitHub credentials.

## Published package paths

```text
privileged-access-approval/pass/package
privileged-access-approval/partial-missing-removal/package
privileged-access-approval/fail-scope-mismatch/package
```

## Publication gate

A package is publishable only if:

```text
verification_result.status = valid
package_index.verification_status = valid
package_index.verification_result_source = witnessops_verifier
receipt validates against witnessops-contracts
manifest validates against witnessops-contracts
verification_result validates against witnessops-contracts
package_index validates against witnessops-contracts
no .hex key-like files are present
no forbidden secret markers are present
PUBLICATION_PROVENANCE.json records the exact source commits
the package and provenance diff is reviewed in one pull request
```

## Current key-registry boundary

The manual publisher does not pass a governed key registry into the sample
exporter. `key_registry` may therefore be `skipped` when the verifier result
records the reason. This is a sample limitation, not production key custody.

## Non-claims

Publishing sample packages does not claim:

```text
live customer evidence
production key custody
client environment security
compliance certification
```

It publishes reproducible fixture-derived packages for inspection.
