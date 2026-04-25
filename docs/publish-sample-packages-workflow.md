# Publish Sample Packages Workflow

## Purpose

The `Publish sample packages` workflow is the controlled publication path for committing generated sample packages into this repository.

This workflow is manual and depends on access to private/internal WitnessOps source repositories. It is not part of the default pull-request or push validation for this public buyer-facing sample repository.

It keeps package custody bounded:

```text
witnessops-proof-engine
  regenerates packages from fixtures

witnessops-verifier
  independently verifies package integrity

witnessops-contracts
  validates package artifact schemas

witnessops-sample-cases
  commits only validated package artifacts
```

## Trigger

The workflow is manual only:

```text
workflow_dispatch
```

Required input:

```text
target_branch
```

Default:

```text
main
```

## Access boundary

The workflow checks out these private/internal dependencies:

```text
witnessops-proof-engine
witnessops-verifier
witnessops-contracts
```

If GitHub Actions cannot access those repositories, publication must stop at checkout. That access failure is an authority or token configuration issue, not a sample-case validation failure.

Default PR/push CI must remain standalone and local-only for this repository.

## Publication sequence

```text
checkout sample-cases
checkout proof-engine
checkout verifier
checkout contracts
export signed sample packages from proof-engine
import packages into sample-cases
run sample-cases tests
validate package_index, verification_result, receipt, and manifest schemas
check no forbidden key or secret material was imported
commit imported packages to target branch
```

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
```

## Current key-registry boundary

The publication workflow does not currently pass a governed key registry into the sample exporter.

Therefore `key_registry` may be:

```text
skipped
```

This is acceptable for v0 sample publication when the verifier result records the reason.

## Non-claims

Publishing sample packages does not claim:

```text
live customer evidence
production key custody
client environment security
compliance certification
```

It publishes reproducible sample packages generated from fixtures.
