# Challenge Path

Sample ID: `SBOM_CISA_2026_MIN_ELEMENTS_SAMPLE_V1`

## What a third party can inspect

1. Confirm that the files named in `MANIFEST.sha256` exist locally.
2. Run `shasum -a 256 -c MANIFEST.sha256` from this directory.
3. Compare `RECEIPT.json` references with the named local files.
4. Compare `EVIDENCE_MANIFEST.json` items with the included synthetic artifacts.
5. Open `artifacts/min_elements_checklist.json` and confirm each `present` / `partial` / `missing` status has an evidence reference or named gap.
6. Confirm that `VERIFY_RESULT.json` is sample-scoped and does not claim production verification or CISA compliance certification.
7. Optionally open the public CISA 2026 resource and compare element names used in the checklist (paraphrased sample mapping, not a legal interpretation).

## What a third party can challenge

- Whether a real vendor SBOM export would map the same fields differently.
- Whether additional CISA 2026 practices beyond this sample checklist should be required for a live engagement.
- Whether component hash and license gaps in a live SBOM should block a buyer decision.
- Whether a client-facing statement exceeds the captured evidence.

## What this sample cannot prove

This sample cannot prove CISA or federal compliance certification, vulnerability-free software, KEV absence, exploitability conclusions, supplier honesty, production signer custody, live customer SBOM authenticity, or complete AI-SBOM / SaaS multi-tenant coverage.
