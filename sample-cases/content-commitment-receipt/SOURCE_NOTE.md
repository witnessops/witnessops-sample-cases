# Source and Adaptation Note

## Source

The initial local seed was packaged as:

```text
witnessops-commitment-receipt-seed-v0.1.0.zip
```

Source ZIP SHA-256:

```text
0f7cd0a20febf7a0425f11e3d6cc57d6b42b0dd5e43c8dd87540f969ebe2b75c
```

The source ZIP was checked through clean extraction, an 18-file manifest comparison, eight positive and negative unit tests, and an end-to-end commitment comparison before adaptation.

## Repository adaptations

- Classified the package as synthetic, educational, and noncanonical.
- Changed the scheme from `WITNESSOPS-CONTENT-COMMITMENT-V1` to `WITNESSOPS-SAMPLE-CONTENT-COMMITMENT-V1`.
- Changed the receipt identifier prefix to `wo-sample-cc-`.
- Renamed the schema as a sample-local fixture.
- Renamed the utility as a sample demonstrator rather than a WitnessOps verifier.
- Reorganized files into explicit pre-disclosure, public-commitment, and disclosure lifecycle stages.
- Removed the nested licence so the repository licence governs this contribution.
- Regenerated commitments, test vectors, disclosure files, and manifest hashes after adaptation.

These adaptations prevent this public example from implying canonical contract or verifier authority.
