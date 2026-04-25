# Import Publication Policy

## Purpose

This policy defines when generated WitnessOps sample packages may be committed into `witnessops-sample-cases`.

The manual publication workflow proves that packages can be regenerated, imported, and validated when private/internal WitnessOps source repositories are accessible. Committing generated packages into this repository is a separate publication act and requires an explicit publication gate.

Default PR/push CI for this public buyer-facing repository is local-only. It must not silently depend on private proof-engine, verifier, or contracts repository access.

## Publication boundary

Publishing a sample package means copying exported package files into one of these paths:

```text
privileged-access-approval/pass/package/
privileged-access-approval/partial-missing-removal/package/
privileged-access-approval/fail-scope-mismatch/package/
```

## Required source

Published packages must be generated from `witnessops-proof-engine` fixtures using:

```text
scripts/export_sample_package.py
```

Manual package assembly is not allowed for publication unless a separate exception is documented.

## Required verification before publication

Before committing package files, the package must have:

```text
verification_result.status = valid
package_index.verification_status = valid
package_index.verification_result_source = witnessops_verifier
receipt validates against witnessops-contracts
manifest validates against witnessops-contracts
verification_result validates against witnessops-contracts
package_index validates against witnessops-contracts
artifact hashes verify
manifest hash verifies against receipt
receipt signature verifies
```

If a key registry is supplied, `key_registry` must be `passed`.

If no key registry is supplied, `key_registry` may be `skipped`, but the reason must be visible in `verification_result.json`.

## Expected workflow outcomes

| Sample case | Expected workflow outcome | Required failure state |
|---|---|---|
| `pass` | `pass` | none |
| `partial-missing-removal` | `partial` | `missing_removal_proof` |
| `fail-scope-mismatch` | `fail` | `scope_mismatch` |

A workflow `fail` result is publishable when the package itself verifies and the failure state is intentional for the sample case.

## Forbidden material

Published packages must not contain:

```text
raw signing key files
signing seeds
operator credentials
cloud signing credentials
access tokens
customer secrets
real customer logs
unredacted personal data
live system exports
```

## Required review before publication

A publication PR must state:

```text
source proof-engine commit or branch
sample packages imported
expected workflow outcomes
verifier command used
contract schemas used
whether key registry was supplied
confirmation that no forbidden material is present
```

## Package update rule

If `witnessops-contracts`, `witnessops-verifier`, or `witnessops-proof-engine` changes the package format, existing published packages should be regenerated or explicitly marked historical.

## Non-claims

Publishing a sample package does not claim:

```text
customer control effectiveness
production signing custody
client environment security
compliance certification
```

It only publishes a reproducible sample package for inspection and verification.
