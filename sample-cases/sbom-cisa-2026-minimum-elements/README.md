# SBOM — CISA 2026 Minimum Elements Sample

Sample ID: `SBOM_CISA_2026_MIN_ELEMENTS_SAMPLE_V1`

Status: `sample_receipt_shape_ready`

## Purpose

This sample shows how WitnessOps can package one **SBOM minimum-elements package check** into a bounded proof pack, mapped against the public **CISA 2026 Minimum Elements for a Software Bill of Materials (SBOM)** baseline.

Sample workflow:

1. Buyer authorizes one scoped SBOM package check for a named software unit (synthetic here).
2. An SBOM producer supplies a machine-readable SBOM fragment and generation context (synthetic here).
3. WitnessOps packages the SBOM, generation context, and a minimum-elements checklist with named gaps.
4. The buyer receives a safe-claim summary that distinguishes checklist observation from compliance or vulnerability conclusions.

## Boundary

This sample proves the package shape, local hash-reference mechanics, and a sample checklist mapping only.

It does **not** claim CISA or federal compliance certification, vulnerability-free software, KEV absence, exploitability conclusions, production deployment, production signer custody, live customer SBOM authenticity, supplier honesty, or complete AI-SBOM / SaaS multi-tenant coverage.

The receipt signature is simulated. The verifier result is sample-only and should not be represented as a production verification.

## Why now

On **29 July 2026**, CISA and partners published updated minimum elements for SBOMs, replacing the 2021 NTIA baseline. Public summaries highlight refined fields such as **Component Hash Algorithm**, **Component License**, **SBOM Tool Name**, and **SBOM Generation Context**, plus naming updates (for example **SBOM Author**, **Component Producer**, **Component Version**).

This sample references that public baseline; it is **not** an official CISA artifact and is **not** a compliance certification.

Public references:

- [2026 Minimum Elements resource](https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom)
- [CISA news release (2026-07-29)](https://www.cisa.gov/news-events/news/cisa-and-partners-unveil-updated-software-bill-materials-resource-improves-transparency-security-and)

## Bundle

| File | Purpose |
|---|---|
| `AUTHORITY_MAP.json` | Names buyer, SBOM producer, packager authority, and negative boundaries |
| `ACTION_BOUNDARY.json` | States what the sample review is allowed and blocked from claiming |
| `artifacts/synthetic_sbom.cdx.json` | Tiny synthetic CycloneDX-shaped SBOM with intentional gaps |
| `artifacts/generation_context.json` | Tool name, author, generation context, CISA reference links |
| `artifacts/min_elements_checklist.json` | Document- and component-level present / partial statuses |
| `SAMPLE_DELIVERABLE_PLAN.md` | Buyer-facing offer shape and safe-language examples |
| `BUYER_WALKTHROUGH.md` | Short inspection order for buyers and partners |
| `EVIDENCE_MANIFEST.json` | Evidence list, hashes, custody boundary, and failure states |
| `RECEIPT.json` | Portable receipt for the sample package-check event |
| `VERIFY_RESULT.json` | Sample verifier-style result and stated limitations |
| `CHALLENGE_PATH.md` | Third-party inspection and challenge path |
| `MANIFEST.sha256` | Local hash manifest for this sample bundle |

## Intentional sample gaps

The synthetic SBOM deliberately omits:

| Component | Gap |
|---|---|
| `gap-demo-lib@0.9.0` | Component License missing |
| `license-only-lib@2.0.1` | Component Hash Algorithm / hash missing |

Checklist overall: `partial_with_named_gaps`.

## Local verification

```bash
cd sample-cases/sbom-cisa-2026-minimum-elements
shasum -a 256 -c MANIFEST.sha256
```

## Commercial point

WitnessOps can deliver a client-readable SBOM package check: which CISA 2026 minimum elements appear present or partial for a named software unit, which gaps remain, and what the client can safely claim afterwards — without turning the pack into a compliance certificate.
