# Sample Case: Privileged Access Approval — Pass

## Scenario

A privileged access event has complete evidence for:

```text
request
approval
authority
execution
removal or expiry
```

## Expected workflow result

```text
outcome = pass
failure_states = []
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

This case demonstrates a complete approval-to-removal proof path for one bounded privileged access event.

## Package path

```text
package/
```

The package should be imported from:

```text
witnessops-proof-engine/dist/sample-packages/privileged-access-approval-pass/
```
