# Buyer Walkthrough — SBOM CISA 2026 Minimum Elements Sample

Sample ID: `SBOM_CISA_2026_MIN_ELEMENTS_SAMPLE_V1`

## Start here

1. Read `README.md` for purpose and boundaries.
2. Open `artifacts/synthetic_sbom.cdx.json` — tiny synthetic application + three libraries.
3. Open `artifacts/generation_context.json` — tool name, author, generation context, CISA reference links.
4. Open `artifacts/min_elements_checklist.json` — document-level present; two intentional component-level gaps.
5. Run `shasum -a 256 -c MANIFEST.sha256`.
6. Read `RECEIPT.json` and `VERIFY_RESULT.json` for sample-scoped results.

## What you should conclude

- WitnessOps can package an SBOM check as a bounded proof pack: authority, artifacts, checklist, gaps, receipt, challenge path.
- Checklist observation is not the same as compliance certification.
- Named gaps (missing license on one component; missing hash on another) are deliberate demo material.

## What you should not conclude

- That this sample SBOM is a real product bill of materials.
- That the software is safe, free of vulnerabilities, or free of known exploited vulnerabilities.
- That CISA endorses WitnessOps or that this sample certifies any organization.

## Public CISA pointers

- [2026 Minimum Elements resource](https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom)
- [29 Jul 2026 news release](https://www.cisa.gov/news-events/news/cisa-and-partners-unveil-updated-software-bill-materials-resource-improves-transparency-security-and)
