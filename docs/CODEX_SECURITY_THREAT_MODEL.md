# Codex Security Threat Model — witnessops-sample-cases

Status: `repo_prep_seed_for_codex_security`

This document is a repository-specific seed for Codex Security review and GitHub PR review. It is not a vulnerability report, not a scan result, and not proof that any production workflow occurred.

## Scope

This repository is the stable sample-case surface for WitnessOps proof packages.

It owns:

- buyer/auditor walkthroughs
- stable sample package paths
- expected sample verifier outcomes
- redaction and sample-boundary notes
- public explanation of what each sample does and does not prove
- sample package material copied from authorized generation flows

Current sample paths include:

- `privileged-access-approval/pass`
- `privileged-access-approval/partial-missing-removal`
- `privileged-access-approval/fail-scope-mismatch`
- `sample-cases/ai-agent-action-proof-run`

## Out of scope

This repository does not own:

- proof-engine source code
- offline verifier implementation
- contract schemas
- key registry authority
- production signing-key custody
- live customer evidence
- production workflow execution
- production deploys
- private client evidence

Do not infer that a passing Codex Security review verifies any out-of-scope system.

## Authority boundaries

- `main` in `witnessops/witnessops-sample-cases` is the code/content authority for public sample-case presentation and sample paths.
- Proof-engine generation authority belongs in `witnessops-proof-engine`.
- Offline verifier implementation authority belongs in `witnessops-verifier`.
- Contract schema authority belongs in `witnessops-contracts`.
- Key-registry authority belongs outside this repo.
- Codex Security may identify findings and suggest patches.
- Codex Security findings do not authorize merge, release, sample artifact mutation, verifier-result mutation, manifest/hash changes, production proof claims, signing authority, deploy, or customer-impacting changes.

## Primary review surfaces

Treat the following as first-class review surfaces:

1. Sample package directories
   - receipts
   - evidence manifests
   - package indexes
   - verifier results
   - reports
   - hash manifests
   - challenge paths and walkthroughs

2. Buyer/auditor walkthroughs
   - claim boundaries
   - reading order
   - not-proven language
   - challenge guidance
   - no-secrets intake language

3. Redaction and sample-boundary notes
   - synthetic/sample status
   - excluded evidence
   - non-production limitations
   - simulated signatures or sample-only verifier results

4. Manifest and hash material
   - `MANIFEST.sha256` where present
   - local file/hash consistency
   - no silent manifest drift

5. Expected verifier outcomes
   - expected package verification status
   - workflow result semantics
   - failure/partial/pass language

## Untrusted inputs

Review all handling of:

- sample receipts
- evidence manifests
- package indexes
- verifier outputs
- walkthrough text
- challenge-path text
- artifact paths
- hash manifests
- copied package outputs from other repos
- any fixture value that resembles a real secret, credential, customer record, private key, token, production target, or private evidence path

## Security invariants

The following must remain true unless an explicit design change is reviewed and approved:

- No private keys, customer records, production evidence, secrets, credentials, tokens, or unrelated production data may be committed.
- Sample cases must not be described as production proof runs.
- Sample cases must not imply source-system honesty, production signing-key custody, client environment security, IAM certification, or real customer control effectiveness.
- Sample claims must stay bounded to included artifacts and stated verifier results.
- Redaction notes and not-proven language must not be removed to make a sample look stronger.
- If sample package artifacts change, related manifests/hashes must be updated in the same lane and the verification command must be named.
- A verifier result must not be edited manually to fit copy; regenerate or re-run through the named verifier path when the lane authorizes it.
- Sample package generation should remain traceable to `witnessops-proof-engine` or another named approved producer.
- Public presentation must not overstate what the sample artifacts prove.

## High-priority finding classes

Treat the following as P1 for review purposes:

- committed secret, credential, token, private key, customer data, or private evidence
- sample copy presenting synthetic sample material as production proof
- mismatched or stale `MANIFEST.sha256` after sample artifact edits
- verifier result edited without a named verifier command or producer path
- sample receipt or evidence manifest claims more than included artifacts support
- buyer-facing walkthrough implying legal compliance, complete AI governance, source-system honesty, or real customer control effectiveness
- sample material copied from a private or production environment without redaction and boundary notes
- artifact path or package reference that points to private local custody paths or operator-only machines

## Lower-priority but relevant finding classes

Review but do not automatically treat as P1 without demonstrated impact:

- cosmetic wording changes that preserve proof boundaries
- missing application security headers, because this repo is not a web app
- dependency advisories, because this repo may not have runtime code
- general style preferences that do not change claim boundaries, artifacts, or verifier semantics

## Review instructions for Codex

When reviewing this repository:

- prefer small, surgical findings over broad refactors
- name the affected sample path, receipt, manifest, walkthrough, verifier output, report, or hash file
- include a concrete leak path, overclaim path, or sample-drift path where possible
- do not propose production customer data, private evidence, signing keys, credentials, or cloud secrets as fixtures
- do not mutate sample artifacts, verifier results, manifests, or hashes unless the lane explicitly authorizes sample-package updates
- do not weaken not-proven language to improve marketing tone
- preserve the distinction between sample presentation, proof-engine generation, verifier implementation, contract schemas, key registry authority, and production workflow reality

## Suggested Codex Security scan configuration

Initial scan seed:

- repository: `witnessops/witnessops-sample-cases`
- branch: `main`
- history window: `180 days`
- environment family: `sample artifacts / markdown / JSON`
- setup command: none unless a future package manager file is introduced
- validation command for docs-only proposed patches: inspect changed files and confirm no sample artifact/hash mutation unless authorized
- artifact hash validation where present: `shasum -a 256 -c MANIFEST.sha256` from the sample package directory
- agent secrets: none
- production credentials: prohibited
- customer data fixtures: prohibited
- private proof bundles: prohibited
- sample artifact mutation without explicit lane authority: prohibited

## Closure condition for this prep artifact

This prep artifact is sufficient when:

- Codex Security scan context can be seeded from this file.
- `AGENTS.md` points reviewers to this file.
- A private-reporting `SECURITY.md` exists for the repo.
- No sample artifacts, receipts, manifests, hashes, verifier results, package indexes, production settings, secrets, customer evidence, or proof claims were changed by this prep pass.
