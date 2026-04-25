# Challenge Path

Sample ID: `AI_AGENT_ACTION_PROOF_RUN_SAMPLE_V1`

## What A Third Party Can Inspect

1. Open `AUTHORITY_MAP.json` and confirm the approval boundary exists.
2. Open `ACTION_BOUNDARY.json` and confirm the allowed and blocked scope are explicit.
3. Open `EVIDENCE_MANIFEST.json` and confirm the receipt names the artifacts it relies on.
4. Open `RECEIPT.json` and confirm it does not claim production deployment, legal compliance, or complete AI governance coverage.
5. Open `VERIFY_RESULT.json` and confirm the verifier result is `pass_with_sample_limitations`.
6. Check `MANIFEST.sha256` to verify local file hashes for the sample bundle.

## Challenge Questions

- Who approved the action?
- What exact action was approved?
- What tool or agent acted?
- What system was touched?
- What evidence was captured?
- What result was produced?
- What could not be independently verified?
- Is the signature real or simulated?
- Does the receipt overclaim beyond the evidence?

## Expected Challenge Outcomes

| Challenge | Expected answer |
|---|---|
| Is this production evidence? | No. Sample only. |
| Is the signature cryptographic? | No. Simulated. |
| Is the approval boundary explicit? | Yes. See `AUTHORITY_MAP.json`. |
| Is the action scope explicit? | Yes. See `ACTION_BOUNDARY.json`. |
| Is there a verifier result? | Yes. See `VERIFY_RESULT.json`. |
| Does the bundle claim complete AI governance coverage? | No. That claim is explicitly out of scope. |

## Failure Path

The proof should be rejected if any of these are true:

- the receipt is represented as production evidence
- the simulated signature is represented as cryptographic proof
- the approval boundary is missing
- the action boundary is missing
- the evidence manifest is missing
- the verifier result is missing
- the receipt claims legal compliance or complete AI governance coverage

