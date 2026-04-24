# Sample Case: Privileged Access Approval — Fail Scope Mismatch

## Scenario

A privileged access event has evidence, but the granted access does not match the approved scope.

Example mismatch:

```text
approved role = reader
granted role = owner
```

## Expected workflow result

```text
outcome = fail
failure_states includes scope_mismatch
```

## Expected package verification result

```text
status = valid
receipt_signature = passed
manifest_hash = passed
artifact_hashes = passed
schema_validation = passed
key_registry = passed | skipped depending on registry input
```

## What this demonstrates

This case demonstrates that package verification and workflow success are separate.

The package can verify while the workflow result is fail because the evidence proves a scope mismatch.

## Package path

```text
package/
```

The package should be imported from:

```text
witnessops-proof-engine/dist/sample-packages/privileged-access-approval-fail-scope-mismatch/
```
