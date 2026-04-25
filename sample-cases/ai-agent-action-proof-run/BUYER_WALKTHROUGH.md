# Buyer Walkthrough

This sample shows how a buyer can inspect a proof bundle after an AI agent acts.

## 1. What this sample is

This is a public, synthetic sample of an AI Agent Action Proof Run bundle. It shows the shape of a bounded receipt package: what the action was allowed to do, who or what acted, what evidence files are present, what the sample verifier result says, and how a third party can challenge the package.

This sample is not a production proof run. It does not claim production deployment, legal compliance, complete AI governance coverage, or real customer control effectiveness.

## 2. Who should read it

This walkthrough is for buyers and reviewers who need to understand the artifact set before requesting their own proof run:

- CISOs checking whether an AI-agent action can be reviewed after the fact.
- AI platform owners deciding whether a proof run fits their agent workflow.
- GRC leads mapping the package to internal review and audit questions.
- Auditors or challengers inspecting what is checkable and what remains outside the sample.

## 3. The buyer question it answers

The sample answers this buyer question:

Can a third party inspect a bounded AI-agent-assisted action and see the action boundary, authority map, evidence list, receipt, verifier result, and challenge path without guessing how the bundle works?

The answer shown here is limited: the bundle demonstrates receipt shape and verifier path using sample artifacts.

## 4. Artifact-by-artifact reading order

Read the files in this order:

| Order | Artifact | Buyer question it answers |
|---:|---|---|
| 1 | `ACTION_BOUNDARY.json` | What was the agent allowed to do, and what was blocked? |
| 2 | `AUTHORITY_MAP.json` | Who or what approved, acted, observed, and reviewed the action? |
| 3 | `EVIDENCE_MANIFEST.json` | Which artifacts are included as evidence for this sample? |
| 4 | `RECEIPT.json` | What does the portable action receipt declare about the run? |
| 5 | `VERIFY_RESULT.json` | What did the sample verifier result report, and with what limitations? |
| 6 | `CHALLENGE_PATH.md` | How should another party inspect, question, or dispute the package? |
| 7 | `MANIFEST.sha256` | Do the local sample files match the published hash manifest? |

## 5. What another party can check

Another party can check the sample by:

- Reading `ACTION_BOUNDARY.json` before any other file to understand the approved and blocked scope.
- Comparing `AUTHORITY_MAP.json` with `RECEIPT.json` to see whether authority, actor, observer, and reviewer roles are declared consistently.
- Reading `EVIDENCE_MANIFEST.json` to identify the evidence files that the receipt depends on.
- Reading `VERIFY_RESULT.json` to see the named result: `pass_with_sample_limitations`.
- Following `CHALLENGE_PATH.md` to see how a reviewer should question missing, inconsistent, or overstated evidence.
- Running `shasum -a 256 -c MANIFEST.sha256` from this directory to check that the sample files named in the manifest match their hashes.

## 6. What remains declared, inferred, or not proven

| Status | Meaning in this sample |
|---|---|
| Declared | The JSON artifacts declare the action boundary, authority roles, evidence list, receipt fields, and sample verifier result. |
| Checkable | The local hashes in `MANIFEST.sha256` can be checked against the sample files. The JSON files can be parsed and inspected. |
| Inferred | A reviewer can infer whether the artifacts tell a coherent story, but that coherence is not the same as source-system truth. |
| Not proven | The sample does not prove production deployment, production signing key custody, source-system honesty, legal compliance, complete AI governance coverage, client environment security, or real customer control effectiveness. |

Any statement that something is verified should point to the artifact that reports it, such as `VERIFY_RESULT.json`, or to the local hash check performed against `MANIFEST.sha256`.

## 7. How to challenge the proof

Use `CHALLENGE_PATH.md` as the challenge guide. A third party should challenge the package if:

- The action boundary is unclear or wider than the receipt suggests.
- The authority map does not identify the actor, approver, observer, or reviewer.
- The evidence manifest omits an artifact needed to understand the action.
- The receipt claims more than the verifier result supports.
- The verifier result does not name its limitations.
- The hash manifest does not match the local files.

For this sample, challenge language should stay bounded to the sample artifacts. It should not treat the sample as a production deployment, legal compliance artifact, or complete AI governance system.

## 8. What to submit for your own proof run

For a real proof run request, submit only non-secret scoping information:

- The AI-agent-assisted workflow to inspect.
- The system or repository touched.
- The intended action boundary.
- The human approval or review path.
- The evidence sources that can be safely captured.
- The verifier or review result you expect to rely on.
- Any known exclusions, redactions, or material that must not be submitted.

Do not submit secrets, credentials, private keys, customer records, or unrelated production data through a public sample path.
