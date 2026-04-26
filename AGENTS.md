# AGENTS.md

## Identity

This repo is the stable sample-case surface for WitnessOps proof packages. It is an inspectable sample and presentation repo — not a proof engine, not a verifier, not a schema authority, and not a deployment target.

## Ownership

This repo owns:

- sample-case READMEs and buyer/auditor walkthroughs
- stable sample package paths
- expected sample verifier outcomes
- redaction and sample-boundary notes
- public explanation of what each sample does and does not prove

This repo does not own:

- proof-engine source code
- offline verifier implementation
- contract schemas
- key registry authority
- production signing-key custody
- live customer evidence
- production workflow execution

## Non-Negotiable Rules

- Do not commit private keys, customer records, production evidence, secrets, credentials, tokens, or unrelated production data.
- Do not describe sample cases as production proof runs.
- Do not imply source-system honesty, production signing-key custody, client environment security, IAM certification, or real customer control effectiveness.
- Keep sample claims bounded to the included artifacts and stated verifier results.
- Do not mutate sample package artifacts, receipts, manifests, hashes, verifier results, or expected outcomes unless the lane explicitly authorizes a sample-case update.
- If a sample artifact changes, update the relevant manifest/hash artifact in the same lane and name the verification command used.
- Keep proof-engine package generation authority in `witnessops-proof-engine`.
- Keep offline verifier authority in `witnessops-verifier`.
- Keep contract schema authority in `witnessops-contracts`.
- Keep key-registry authority outside this repo.

## Codex Security review

Use [`docs/CODEX_SECURITY_THREAT_MODEL.md`](./docs/CODEX_SECURITY_THREAT_MODEL.md) as the seed context for Codex Security review.

Codex Security may identify findings and propose patches, but it does not authorize merge, release, sample artifact mutation, verifier-result mutation, manifest/hash changes, production proof claims, signing authority, deploy, or customer-impacting changes.

For security-sensitive changes, preserve these boundaries:

- sample artifacts are public and synthetic unless explicitly stated otherwise
- included receipts and verifier outputs are sample-scoped
- manifests and hashes must match local files when present
- redaction notes and not-proven language must not be removed to make the sample look stronger
- no real secret, customer, or production evidence may be introduced as a fixture

## Validation

This repo may not have a package-level health command. For sample-package lanes, validation should name the exact artifact checks performed, such as:

```bash
shasum -a 256 -c MANIFEST.sha256
```

Where verifier checks are used, record the exact verifier command, verifier repo/ref, contracts repo/ref, key registry source if any, and observed result.
