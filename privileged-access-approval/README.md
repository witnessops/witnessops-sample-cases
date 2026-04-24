# Privileged Access Approval Sample Cases

This directory contains stable sample cases for the `privileged_access_approval` workflow.

## Workflow question

> Can you prove that privileged access was approved, granted as approved, bounded by time, and removed when it should have been?

## Sample cases

| Case | Workflow outcome | Package verification status | Purpose |
|---|---|---|---|
| `pass` | `pass` | `valid` after verifier run | Shows a complete approval-to-removal proof path. |
| `partial-missing-removal` | `partial` | `valid` after verifier run | Shows a package that verifies, while the workflow result declares missing removal proof. |
| `fail-scope-mismatch` | `fail` | `valid` after verifier run | Shows a package that verifies, while the workflow result declares a scope mismatch. |

## Important distinction

A workflow result can be `fail` while the package verification status is `valid`.

```text
workflow outcome
  says what the bounded workflow evidence proves

package verification status
  says whether the receipt, manifest, artifacts, schemas, and signatures verify
```

## Package source

Packages should be exported from `witnessops-proof-engine` and copied into each sample case directory under:

```text
package/
```

Until packages are imported, each case includes README documentation and expected result boundaries.
