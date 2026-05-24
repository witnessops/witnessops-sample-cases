# Challenge Path

Sample ID: `PHONE_SECURITY_PROOF_PACK_SAMPLE_V1`

## What a third party can inspect

1. Confirm that the files named in `MANIFEST.sha256` exist locally.
2. Run `shasum -a 256 -c MANIFEST.sha256` from this directory.
3. Compare `RECEIPT.json` references with the named local files.
4. Compare `EVIDENCE_MANIFEST.json` items with the included synthetic artifacts.
5. Confirm that `VERIFY_RESULT.json` is sample-scoped and does not claim production verification.

## What a third party can challenge

- Whether the phone security operator's real-world tool output supports a stronger claim.
- Whether device handling continuity was preserved in a live workflow.
- Whether app provenance, boot integrity, or signer authority was separately verified.
- Whether a client-facing statement exceeds the captured evidence.

## What this sample cannot prove

This sample cannot prove spyware detection, absence of compromise, forensic admissibility, legal compliance, production signer custody, source-system honesty, or whole-device assurance.
