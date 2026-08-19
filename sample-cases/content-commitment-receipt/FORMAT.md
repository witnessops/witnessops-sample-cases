# Sample Format and Construction

## Authority warning

This document defines only the synthetic format used by this directory. It is not a canonical `witnessops-contracts` schema and does not change verifier acceptance semantics elsewhere.

## Commitment scheme

Identifier:

```text
WITNESSOPS-SAMPLE-CONTENT-COMMITMENT-V1
```

Digest algorithm:

```text
SHA-256
```

Nonce requirement:

```text
32 cryptographically random bytes
```

The commitment input is the concatenation of:

1. ASCII domain separator `WITNESSOPS-SAMPLE-CONTENT-COMMITMENT-V1`;
2. one zero byte;
3. nonce length as an unsigned 2-byte big-endian integer;
4. nonce bytes;
5. artifact length as an unsigned 8-byte big-endian integer;
6. artifact bytes.

```text
SHA256(
  ASCII("WITNESSOPS-SAMPLE-CONTENT-COMMITMENT-V1") ||
  0x00 ||
  U16_BE(len(nonce)) ||
  nonce ||
  U64_BE(len(artifact)) ||
  artifact
)
```

## Receipt identifier

```text
wo-sample-cc-<first-24-commitment-hex-characters>
```

The identifier is for sample correlation only.

## Exact bytes

There is no canonicalization. Files that render identically but contain different bytes do not match. PDF metadata changes, text line-ending changes, and re-exporting can all change the commitment.

## Interoperability test vector

Artifact bytes, represented as UTF-8 text:

```text
Example artifact bytes\n
```

Nonce hexadecimal:

```text
000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
```

Expected commitment:

```text
addde967ed41ab1af3de55ecbb49c9d6b2561515ae75b9f96bfd6ebbebcf2ca0
```
