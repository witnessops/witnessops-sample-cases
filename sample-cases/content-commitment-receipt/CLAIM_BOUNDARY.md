# Sample Claim Boundary

## Purpose

This directory demonstrates a salted content-commitment lifecycle. It is a synthetic sample, not a hosted service, canonical contract, supported verifier distribution, identity system, digital-signature system, or trusted timestamp authority.

## Inputs required for the sample comparison

1. Exact artifact bytes.
2. The structurally valid sample receipt.
3. The 32-byte nonce from the disclosure or opening record.

## Successful result

The sample utility returns `VERDICT=SAMPLE_CONTENT_COMMITMENT_MATCH` only when:

- the receipt uses the expected sample version, type, scheme, algorithm, and field formats;
- the disclosed nonce is exactly 32 bytes;
- the receipt identifier corresponds to its commitment;
- the artifact byte length matches the receipt;
- recomputing the commitment produces exactly the recorded value.

The successful result supports this bounded proposition:

> The supplied artifact bytes and nonce reproduce the supplied commitment under `WITNESSOPS-SAMPLE-CONTENT-COMMITMENT-V1` using SHA-256.

## Timing proposition

If the unchanged receipt were independently anchored and that anchor were separately verified under an accepted trust chain, a verifier could additionally assess whether the commitment existed no later than the evidenced anchor time.

This sample has no external anchor. The self-declared creation time is not evidence of time.

## Unsupported propositions

This sample does not establish:

- truth;
- authorship;
- identity of the operator;
- operational authority;
- confidentiality;
- first creation time;
- independent timestamping;
- absence of alternate versions;
- artifact safety;
- production execution;
- customer control effectiveness;
- compliance or certification;
- canonical WitnessOps verifier acceptance.

## Privacy boundary

The public receipt omits the raw artifact hash and nonce. The sample commitment includes a 32-byte nonce so a public commitment does not ordinarily enable straightforward guessing of predictable artifact content.

Publishing the nonce enables candidate artifacts to be tested against the commitment. This repository publishes it intentionally because the lifecycle is synthetic and fully disclosed.

Labels and byte lengths may still reveal information. A real operator must account for those disclosures separately.

## Cryptographic assumptions

The sample relies on SHA-256 preimage and collision resistance, correct generation and preservation of the nonce, exact preservation of the artifact bytes, and correct implementation of the declared sample scheme.
