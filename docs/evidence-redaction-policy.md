# Evidence Redaction Policy

## Purpose

This policy defines what evidence may appear in `witnessops-sample-cases`.

## Allowed evidence

```text
synthetic fixtures
redacted examples
non-customer demonstration artifacts
hashable package artifacts generated from fixtures
```

## Forbidden evidence

```text
real customer evidence
private keys
client secrets
access tokens
production credentials
personal data
unredacted emails
live system exports
```

## Required sample language

Every sample case must make clear that sample evidence is synthetic or redacted and is not a customer audit record.

## Import rule

Packages imported from `witnessops-proof-engine` must be generated from fixture data only unless a separate redaction review and publication approval exists.
