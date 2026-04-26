# Security Policy

We take security issues in this repository seriously. This document describes what is in scope, how to report a suspected vulnerability, and what to expect from us in return.

## Scope

This repository contains public sample-case material for WitnessOps proof packages:

- buyer/auditor walkthroughs
- sample package paths
- sample receipts and related public artifacts
- expected sample verifier outcomes
- redaction and sample-boundary notes
- public explanation of what each sample does and does not prove

This repository does **not** contain proof-engine source code, offline verifier implementation, contract schemas, key registry authority, production signing-key custody, live customer evidence, production workflow execution, deployment authority, or private client evidence.

Reports against systems outside this repository are out of scope here and should be directed to the appropriate project or vendor.

## Supported surface

Only the current `main` branch of this repository is supported and receives security fixes. Older branches, tags, and historical releases are not patched.

## Reporting a vulnerability

Please report suspected vulnerabilities privately through one of the following channels:

- **Preferred:** GitHub Private Vulnerability Reporting —
  <https://github.com/witnessops/witnessops-sample-cases/security/advisories/new>
- **Alternative:** email <security@witnessops.com>

When reporting, please include:

- a description of the issue and its potential impact
- steps to reproduce, or a proof of concept
- the affected sample path, receipt, manifest, walkthrough, verifier output, report, or hash file if known
- any relevant commit SHA or environment details

> **Do not use public GitHub issues, discussions, or pull requests to report suspected vulnerabilities.** Public reports can put users at risk before a fix is available.

## Acknowledgment window

We will acknowledge receipt of your report within **5 business days**. That acknowledgment confirms the report reached us; a full triage and impact assessment will follow.

## Disclosure handling

We prefer coordinated disclosure:

- We will work with you to validate the issue, assess impact, and prepare a fix.
- We ask for a reasonable embargo period while a fix is being prepared and rolled out. The exact length depends on severity and complexity, and we will agree it with you.
- Once a fix is available, we will publish an advisory describing the issue and its resolution.
- Reporters will be credited in the advisory unless they ask to remain anonymous.

## Examples of in-scope issues

The following are examples of issues that may be security-relevant in this repository:

- committed secret, credential, token, private key, customer data, or private evidence
- sample copy presenting synthetic sample material as production proof
- mismatched or stale `MANIFEST.sha256` after sample artifact edits
- verifier result edited without a named verifier command or producer path
- sample receipt or evidence manifest claims more than included artifacts support
- buyer-facing walkthrough implying legal compliance, complete AI governance, source-system honesty, or real customer control effectiveness
- sample material copied from a private or production environment without redaction and boundary notes
- artifact path or package reference that points to private local custody paths or operator-only machines

## Generally out of scope

The following are generally not considered reportable vulnerabilities for this repository unless a concrete security impact is demonstrated:

- missing generic web-app security headers, because this repo is not a web app
- social-engineering attacks targeting maintainers or operators
- denial-of-service via volumetric traffic flooding
- third-party dependency advisories already tracked by an automated advisory feed
- marketing style preferences that do not affect claim boundaries, artifacts, or verifier semantics

If you believe one of the above has a concrete, demonstrable security impact in this repository, please still report it through the private channels above and explain the impact.
