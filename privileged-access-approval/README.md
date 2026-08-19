# Privileged Access Approval — Planned Sample Cases

> **Status: PLANNED / DOCUMENTATION ONLY**
>
> These scenarios do not yet contain published sample packages. Each
> `package/` directory is intentionally empty apart from `.gitkeep`.

This directory describes planned sample cases for the
`privileged_access_approval` workflow.

## Workflow question

> Can you prove that privileged access was approved, granted as approved, bounded by time, and removed when it should have been?

## Planned cases

| Case | Intended workflow outcome | Current package status | Purpose |
|---|---|---|---|
| `pass` | `pass` | Not published | Intended to show a complete approval-to-removal proof path. |
| `partial-missing-removal` | `partial` | Not published | Intended to show missing removal proof. |
| `fail-scope-mismatch` | `fail` | Not published | Intended to show a scope mismatch. |

## Important distinction

After packages are generated and published, a workflow result may be `fail`
while the package verification status is `valid`.

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

Until packages are imported through a reviewed publication change, each case is
documentation only and must not be described as verified, complete, or current.
