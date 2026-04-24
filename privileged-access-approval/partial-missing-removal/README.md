# Sample Case: Privileged Access Approval — Partial Missing Removal

## Scenario

A privileged access event has request, approval, authority, and execution evidence, but lacks portable proof that access was removed or expired.

## Expected workflow result

```text
outcome = partial
failure_states includes missing_removal_proof
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

This case demonstrates the distinction between a valid package and an incomplete workflow proof path.

The package can verify while the workflow result remains partial.

## Package path

```text
package/
```

The package should be imported from:

```text
witnessops-proof-engine/dist/sample-packages/privileged-access-approval-partial-missing-removal/
```
