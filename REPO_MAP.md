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
live customer evidence
```

## Published and planned structure

```text
privileged-access-approval/
  # planned documentation only; package directories are empty
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

sample-cases/
  content-commitment-receipt/
    README.md
    CLAIM_BOUNDARY.md
    FORMAT.md
    SOURCE_NOTE.md
    MANIFEST.sha256
    lifecycle/
      01-pre-disclosure/
      02-public-commitment/
      03-disclosure/
    schema/
    tools/
    scripts/
    tests/
  ai-agent-action-proof-run/
    README.md
    AUTHORITY_MAP.json
    ACTION_BOUNDARY.json
    EVIDENCE_MANIFEST.json
    RECEIPT.json
    VERIFY_RESULT.json
    CHALLENGE_PATH.md
    MANIFEST.sha256
  proof-of-record-pipeline/
    README.md
    AUTHORITY_MAP.json
    ACTION_BOUNDARY.json
    CONNECTOR_EVENT.json
    CANONICAL_PAYLOAD.json
    EVIDENCE_MANIFEST.json
    RECEIPT.json
    VERIFY_RESULT.json
    CHALLENGE_PATH.md
    MANIFEST.sha256
    artifacts/source_artifact.md
  phone-security-proof-pack/
    README.md
    AUTHORITY_MAP.json
    ACTION_BOUNDARY.json
    EVIDENCE_MANIFEST.json
    RECEIPT.json
    VERIFY_RESULT.json
    SAMPLE_DELIVERABLE_PLAN.md
    CHALLENGE_PATH.md
    MANIFEST.sha256
    artifacts/device_check_summary.md
  sbom-cisa-2026-minimum-elements/
    README.md
    BUYER_WALKTHROUGH.md
    AUTHORITY_MAP.json
    ACTION_BOUNDARY.json
    EVIDENCE_MANIFEST.json
    RECEIPT.json
    VERIFY_RESULT.json
    SAMPLE_DELIVERABLE_PLAN.md
    CHALLENGE_PATH.md
    MANIFEST.sha256
    artifacts/synthetic_sbom.cdx.json
    artifacts/generation_context.json
    artifacts/min_elements_checklist.json

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
published sample directories exactly match SAMPLE_CASES_MANIFEST.v1.yaml
published sample README files exist
planned privileged-access package directories contain only .gitkeep
planned expected outcomes are explicitly marked as unobserved
no private-key indicators appear
no live customer evidence markers appear
```
