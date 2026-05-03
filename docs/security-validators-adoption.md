# Security Validators Adoption

```yaml
classification: INTERNAL_ONLY
publication_status: do_not_publish
execution_status: not_authorized
adoption_status: structure_only_guardrail
live_testing_allowed: false
security_posture_claim_allowed: false
sample_artifacts_mutated: false
```

## Purpose

This repo adopts the WitnessOps security validators package as a structure-only CI guardrail under:

```text
tools/witnessops-security-validators/
```

The package checks committed validator examples and boundary fixtures. It does not change sample cases, receipts, manifests, verifier results, package hashes, or expected sample outcomes.

## Repository Boundary

`witnessops-sample-cases` remains a sample and presentation surface. This adoption does not make the repo a proof engine, verifier implementation, contract schema authority, key-registry authority, deployment surface, or live security testing surface.

The schemas and fixtures inside `tools/witnessops-security-validators/` are validator package fixtures only. They are not promoted as WitnessOps contract schemas and do not replace `witnessops-contracts`.

## Included Checks

The CI workflow runs:

```bash
python3 scripts/validate-dfir-fixtures.py
python3 scripts/validate-api-authz-fixtures.py
python3 scripts/validate-sbom-supply-chain-fixtures.py
python3 scripts/validate-purple-detection-fixtures.py
python3 scripts/validate-source-refresh-records.py
```

from `tools/witnessops-security-validators/`.

## Allowed Claim

```text
The security validators passed structure-only checks against committed validator examples.
```

## Blocked Claims

Do not claim that this adoption proves:

- sample cases are production proof runs;
- source-system honesty;
- production signing-key custody;
- client environment security;
- IAM certification;
- real customer control effectiveness;
- live API, endpoint, cloud, telemetry, dependency, or package security posture.

## Closure

```yaml
security_validators_adoption:
  package_path: tools/witnessops-security-validators
  ci_workflow: .github/workflows/security-validators.yml
  sample_artifact_changes: false
  proof_execution_added: false
  verifier_authority_added: false
  contract_schema_authority_added: false
  live_testing_added: false
  public_security_posture_claim_added: false
```
