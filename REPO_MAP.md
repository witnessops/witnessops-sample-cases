# Repo Map: witnessops-sample-cases

## Responsibility

Stable sample-case surface for WitnessOps proof packages.

## Owns

```text
sample-case README files
sample scenario explanations
expected verifier outcomes
stable package paths for demos
redaction and sample-boundary notes
sample-case structure validation
```

## Does not own

```text
proof execution
receipt signing
verifier implementation
contract schemas
key registry authority
private keys
real customer evidence
```

## Planned structure

```text
privileged-access-approval/
  README.md
  pass/
    README.md
    package/
  partial-missing-removal/
    README.md
    package/
  fail-scope-mismatch/
    README.md
    package/

docs/
  how-to-verify-sample.md
  sample-case-boundaries.md
  evidence-redaction-policy.md

tests/
  test_sample_case_structure.py

.github/workflows/
  validate-sample-cases.yml
```

## First gate

```text
sample case directories exist
sample README files exist
sample package directories are declared but may be empty until package import
expected outcomes are documented
no private-key indicators appear
no real customer evidence markers appear
```
