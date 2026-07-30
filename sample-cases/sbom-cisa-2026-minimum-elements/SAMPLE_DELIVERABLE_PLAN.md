# Sample Deliverable Plan — SBOM CISA 2026 Minimum Elements

Sample ID: `SBOM_CISA_2026_MIN_ELEMENTS_SAMPLE_V1`

## Offer shape (sample)

**Name:** SBOM minimum-elements package check (CISA 2026 baseline)

**Situation:** A buyer received or produced an SBOM and needs a bounded answer: which CISA 2026 minimum elements appear present, partial, missing, or unknown for a named software unit.

**Result:** A proof pack with:

1. The SBOM artifact(s) in scope (synthetic in this sample).
2. Generation context (tool name, author, scope notes).
3. A minimum-elements checklist with named gaps.
4. Evidence manifest, receipt, challenge path, and sample verifier-style result.

## Inputs (non-secret)

- Named software unit and version.
- SBOM file or agreed export path (format: CycloneDX or SPDX preferred).
- Who authored/generated the SBOM and with which tool, if known.
- Any known exclusions (containers, AI stack, SaaS multi-tenant surfaces).

## Explicit exclusions

- Not a vulnerability scan program.
- Not a VEX / exploitability opinion.
- Not a CISA or federal compliance certification.
- Not a claim of supplier honesty or full build-pipeline fidelity.
- Not a full AI-SBOM or SaaS multi-tenant assessment unless separately scoped.

## Safe client language examples

Allowed:

- "For the synthetic sample-app unit, document-level CISA 2026 fields in this pack are present; two component-level fields are partial with named gaps."
- "The package integrity checks for the included sample files passed under sample limitations."

Blocked:

- "This SBOM is CISA-compliant."
- "The software has no known exploited vulnerabilities."
- "This certifies supply-chain security."

## Public reference (not a claim of endorsement)

- CISA resource: [2026 Minimum Elements for a Software Bill of Materials (SBOM)](https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom)
- CISA news (2026-07-29): [Updated SBOM resource](https://www.cisa.gov/news-events/news/cisa-and-partners-unveil-updated-software-bill-materials-resource-improves-transparency-security-and)
