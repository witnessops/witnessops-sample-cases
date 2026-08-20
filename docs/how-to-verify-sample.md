# How to Verify a WitnessOps Sample Package

## Purpose

This guide explains how to verify a sample package in this repository using `witnessops-verifier` and `witnessops-contracts`.

## Inputs

The command below applies only after the privileged-access package has been
generated and published. The checked-in `privileged-access-approval/*/package`
directories are currently planned placeholders and are not verifiable packages.

```text
witnessops-sample-cases/<sample>/package/
witnessops-verifier/
witnessops-contracts/
witnessops-key-registry/ optional
```

## Command

```bash
PYTHONPATH=../witnessops-verifier \
python ../witnessops-verifier/verifier/witnessops_verify.py ./privileged-access-approval/pass/package \
  --contracts-dir ../witnessops-contracts \
  --key-registry-dir ../witnessops-key-registry
```

## Expected checks

```text
receipt_signature
key_registry
manifest_hash
artifact_hashes
schema_validation
```

## Important distinction

A sample package can verify as structurally and cryptographically valid while the workflow outcome is `partial` or `fail`.

```text
package verification status
  tells whether the package is internally checkable

workflow outcome
  tells what the evidence proves about the bounded event
```
