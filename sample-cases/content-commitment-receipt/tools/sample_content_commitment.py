#!/usr/bin/env python3
"""Dependency-free demonstrator for the synthetic content-commitment sample."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
import secrets
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


TOOL_VERSION = "0.1.0-sample"
RECEIPT_VERSION = "1.0-sample"
DISCLOSURE_VERSION = "1.0-sample"
OPENING_RECORD_VERSION = "1.0-sample"
RECEIPT_TYPE = "sample_content_commitment"
SCHEME = "WITNESSOPS-SAMPLE-CONTENT-COMMITMENT-V1"
ALGORITHM = "SHA-256"
NONCE_BYTES = 32
DOMAIN_SEPARATOR = SCHEME.encode("ascii") + b"\x00"
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
RECEIPT_ID = re.compile(r"^wo-sample-cc-[0-9a-f]{24}$")


class SampleReceiptError(ValueError):
    """Raised for malformed sample inputs."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def validate_timestamp(value: str) -> str:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise SampleReceiptError("timestamp must be an ISO 8601 UTC value ending in Z")
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise SampleReceiptError("timestamp is not valid ISO 8601") from exc
    return value


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compute_commitment(artifact: bytes, nonce: bytes) -> str:
    if len(nonce) != NONCE_BYTES:
        raise SampleReceiptError(f"nonce must be exactly {NONCE_BYTES} bytes")
    if len(artifact) >= 1 << 64:
        raise SampleReceiptError("artifact is too large for the sample encoding")
    material = (
        DOMAIN_SEPARATOR
        + len(nonce).to_bytes(2, "big")
        + nonce
        + len(artifact).to_bytes(8, "big")
        + artifact
    )
    return sha256_hex(material)


def receipt_id_for(commitment: str) -> str:
    if not HEX_64.fullmatch(commitment):
        raise SampleReceiptError("commitment must be 64 lowercase hexadecimal characters")
    return f"wo-sample-cc-{commitment[:24]}"


def build_receipt(
    artifact: bytes,
    artifact_label: str,
    nonce: bytes,
    claimed_created_at: str,
) -> Dict[str, Any]:
    if not artifact_label or len(artifact_label) > 255:
        raise SampleReceiptError("artifact label must contain 1 to 255 characters")
    validate_timestamp(claimed_created_at)
    commitment = compute_commitment(artifact, nonce)
    return {
        "sample_status": "synthetic_noncanonical",
        "receipt_version": RECEIPT_VERSION,
        "receipt_type": RECEIPT_TYPE,
        "receipt_id": receipt_id_for(commitment),
        "commitment": {
            "scheme": SCHEME,
            "digest_algorithm": ALGORITHM,
            "value": commitment,
        },
        "artifact": {
            "label": artifact_label,
            "byte_length": len(artifact),
        },
        "opening_requirements": {
            "nonce_bytes": NONCE_BYTES,
            "nonce_encoding": "hex",
            "nonce_in_receipt": False,
        },
        "time_evidence": {
            "claimed_created_at": claimed_created_at,
            "external_anchor": None,
        },
        "claims": {
            "supported_after_successful_opening": [
                "The supplied artifact bytes and nonce reproduce this synthetic commitment under the declared sample scheme."
            ],
            "not_supported_by_this_sample": [
                "truth",
                "authorship",
                "authority",
                "confidentiality",
                "first_creation_time",
                "independent_timestamp",
                "artifact_safety",
                "canonical_verifier_acceptance",
            ],
        },
        "generator": {
            "name": "witnessops-sample-cases/content-commitment-receipt",
            "version": TOOL_VERSION,
        },
    }


def build_opening_record(receipt: Dict[str, Any], artifact: bytes, nonce: bytes) -> Dict[str, Any]:
    return {
        "opening_record_version": OPENING_RECORD_VERSION,
        "opening_record_type": "sample_commitment_opening_record",
        "receipt_id": receipt["receipt_id"],
        "nonce_encoding": "hex",
        "nonce": nonce.hex(),
        "artifact_sha256_operator_diagnostic": sha256_hex(artifact),
        "warning": "WITHHOLD UNTIL INTENTIONAL DISCLOSURE IN A REAL RUN; PUBLISHED HERE ONLY AS SYNTHETIC SAMPLE DATA",
    }


def build_disclosure(receipt: Dict[str, Any], nonce: bytes) -> Dict[str, Any]:
    return {
        "disclosure_version": DISCLOSURE_VERSION,
        "disclosure_type": "sample_commitment_opening",
        "receipt_id": receipt["receipt_id"],
        "nonce_encoding": "hex",
        "nonce": nonce.hex(),
    }


def load_json(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SampleReceiptError(f"file not found: {path}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SampleReceiptError(f"cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SampleReceiptError(f"JSON root must be an object: {path}")
    return value


def write_json(path: Path, value: Dict[str, Any], force: bool = False) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        raise SampleReceiptError(f"refusing to overwrite existing file without --force: {path}")
    payload = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    handle, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def require_object(parent: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise SampleReceiptError(f"receipt field {key!r} must be an object")
    return value


def require_exact_keys(value: Dict[str, Any], expected: set[str], context: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        raise SampleReceiptError(f"{context} is missing required fields: {', '.join(missing)}")
    if extra:
        raise SampleReceiptError(f"{context} contains unsupported fields: {', '.join(extra)}")


def validate_receipt(receipt: Dict[str, Any]) -> None:
    require_exact_keys(
        receipt,
        {
            "sample_status",
            "receipt_version",
            "receipt_type",
            "receipt_id",
            "commitment",
            "artifact",
            "opening_requirements",
            "time_evidence",
            "claims",
            "generator",
        },
        "receipt",
    )
    if receipt.get("sample_status") != "synthetic_noncanonical":
        raise SampleReceiptError("receipt is not marked synthetic_noncanonical")
    if receipt.get("receipt_version") != RECEIPT_VERSION:
        raise SampleReceiptError("unsupported receipt_version")
    if receipt.get("receipt_type") != RECEIPT_TYPE:
        raise SampleReceiptError("unsupported receipt_type")
    receipt_id = receipt.get("receipt_id")
    if not isinstance(receipt_id, str) or not RECEIPT_ID.fullmatch(receipt_id):
        raise SampleReceiptError("invalid receipt_id")

    commitment = require_object(receipt, "commitment")
    require_exact_keys(commitment, {"scheme", "digest_algorithm", "value"}, "commitment")
    if commitment.get("scheme") != SCHEME:
        raise SampleReceiptError("unsupported sample commitment scheme")
    if commitment.get("digest_algorithm") != ALGORITHM:
        raise SampleReceiptError("unsupported digest algorithm")
    commitment_value = commitment.get("value")
    if not isinstance(commitment_value, str) or not HEX_64.fullmatch(commitment_value):
        raise SampleReceiptError("invalid commitment value")
    if receipt_id != receipt_id_for(commitment_value):
        raise SampleReceiptError("receipt_id does not correspond to commitment")

    artifact = require_object(receipt, "artifact")
    require_exact_keys(artifact, {"label", "byte_length"}, "artifact")
    if not isinstance(artifact.get("label"), str) or not artifact["label"]:
        raise SampleReceiptError("artifact label must be a non-empty string")
    byte_length = artifact.get("byte_length")
    if not isinstance(byte_length, int) or isinstance(byte_length, bool) or byte_length < 0:
        raise SampleReceiptError("artifact byte_length must be a non-negative integer")

    opening_requirements = require_object(receipt, "opening_requirements")
    require_exact_keys(
        opening_requirements,
        {"nonce_bytes", "nonce_encoding", "nonce_in_receipt"},
        "opening_requirements",
    )
    if opening_requirements.get("nonce_bytes") != NONCE_BYTES:
        raise SampleReceiptError("unsupported nonce size")
    if opening_requirements.get("nonce_encoding") != "hex":
        raise SampleReceiptError("unsupported nonce encoding")
    if opening_requirements.get("nonce_in_receipt") is not False:
        raise SampleReceiptError("sample receipt must not contain the nonce")

    time_evidence = require_object(receipt, "time_evidence")
    require_exact_keys(time_evidence, {"claimed_created_at", "external_anchor"}, "time_evidence")
    validate_timestamp(time_evidence.get("claimed_created_at"))

    claims = require_object(receipt, "claims")
    require_exact_keys(
        claims,
        {"supported_after_successful_opening", "not_supported_by_this_sample"},
        "claims",
    )
    for key in ("supported_after_successful_opening", "not_supported_by_this_sample"):
        items = claims.get(key)
        if not isinstance(items, list) or not items or not all(isinstance(item, str) and item for item in items):
            raise SampleReceiptError(f"claims.{key} must be a non-empty array of non-empty strings")

    generator = require_object(receipt, "generator")
    require_exact_keys(generator, {"name", "version"}, "generator")
    if not all(isinstance(generator.get(key), str) and generator[key] for key in ("name", "version")):
        raise SampleReceiptError("generator name and version must be non-empty strings")


def extract_nonce(opening: Dict[str, Any], expected_receipt_id: str) -> bytes:
    disclosure_type = opening.get("disclosure_type")
    opening_record_type = opening.get("opening_record_type")
    if disclosure_type == "sample_commitment_opening":
        require_exact_keys(
            opening,
            {"disclosure_version", "disclosure_type", "receipt_id", "nonce_encoding", "nonce"},
            "disclosure",
        )
        if opening.get("disclosure_version") != DISCLOSURE_VERSION:
            raise SampleReceiptError("unsupported disclosure_version")
    elif opening_record_type == "sample_commitment_opening_record":
        require_exact_keys(
            opening,
            {
                "opening_record_version",
                "opening_record_type",
                "receipt_id",
                "nonce_encoding",
                "nonce",
                "artifact_sha256_operator_diagnostic",
                "warning",
            },
            "opening record",
        )
        if opening.get("opening_record_version") != OPENING_RECORD_VERSION:
            raise SampleReceiptError("unsupported opening_record_version")
        diagnostic = opening.get("artifact_sha256_operator_diagnostic")
        if not isinstance(diagnostic, str) or not HEX_64.fullmatch(diagnostic):
            raise SampleReceiptError("invalid operator diagnostic artifact digest")
    else:
        raise SampleReceiptError("opening must be a supported sample disclosure or opening record")

    if opening.get("receipt_id") != expected_receipt_id:
        raise SampleReceiptError("opening receipt_id does not match the receipt")
    if opening.get("nonce_encoding") != "hex":
        raise SampleReceiptError("opening nonce encoding must be hex")
    nonce_hex = opening.get("nonce")
    if not isinstance(nonce_hex, str) or not HEX_64.fullmatch(nonce_hex):
        raise SampleReceiptError("opening nonce must be 64 lowercase hexadecimal characters")
    return bytes.fromhex(nonce_hex)


def verify_opening(
    artifact: bytes,
    receipt: Dict[str, Any],
    opening: Dict[str, Any],
) -> Dict[str, str]:
    validate_receipt(receipt)
    nonce = extract_nonce(opening, receipt["receipt_id"])
    length_match = len(artifact) == receipt["artifact"]["byte_length"]
    calculated = compute_commitment(artifact, nonce)
    commitment_match = hmac.compare_digest(calculated, receipt["commitment"]["value"])
    anchor = receipt["time_evidence"]["external_anchor"]
    time_result = "NOT_PRESENT" if anchor is None else "PRESENT_NOT_VERIFIED"
    verdict = "SAMPLE_CONTENT_COMMITMENT_MATCH" if length_match and commitment_match else "NO_MATCH"
    return {
        "receipt_structure": "PASS",
        "artifact_byte_length_match": "PASS" if length_match else "FAIL",
        "commitment_match": "PASS" if commitment_match else "FAIL",
        "time_evidence": time_result,
        "verdict": verdict,
    }


def load_artifact(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError as exc:
        raise SampleReceiptError(f"artifact not found: {path}") from exc
    except OSError as exc:
        raise SampleReceiptError(f"cannot read artifact {path}: {exc}") from exc


def command_commit(args: argparse.Namespace) -> int:
    artifact_path = Path(args.artifact)
    receipt_path = Path(args.receipt).resolve()
    opening_path = Path(args.opening_record).resolve()
    if receipt_path == opening_path:
        raise SampleReceiptError("receipt and opening record must use different paths")
    if not args.force:
        for output_path in (receipt_path, opening_path):
            if output_path.exists():
                raise SampleReceiptError(f"refusing to overwrite existing file without --force: {output_path}")
    artifact = load_artifact(artifact_path)
    if args.nonce_hex is None:
        nonce = secrets.token_bytes(NONCE_BYTES)
    else:
        if not HEX_64.fullmatch(args.nonce_hex):
            raise SampleReceiptError("--nonce-hex must contain exactly 64 lowercase hexadecimal characters")
        nonce = bytes.fromhex(args.nonce_hex)
    claimed_created_at = validate_timestamp(args.claimed_created_at or utc_now())
    receipt = build_receipt(artifact, args.artifact_label or artifact_path.name, nonce, claimed_created_at)
    opening_record = build_opening_record(receipt, artifact, nonce)
    write_json(receipt_path, receipt, force=args.force)
    write_json(opening_path, opening_record, force=args.force)
    print(f"RECEIPT_ID={receipt['receipt_id']}")
    print(f"RECEIPT={receipt_path}")
    print(f"OPENING_RECORD={opening_path}")
    print("TIME_EVIDENCE=NOT_PRESENT")
    return 0


def command_disclose(args: argparse.Namespace) -> int:
    receipt = load_json(Path(args.receipt))
    validate_receipt(receipt)
    opening_record = load_json(Path(args.opening_record))
    nonce = extract_nonce(opening_record, receipt["receipt_id"])
    disclosure = build_disclosure(receipt, nonce)
    write_json(Path(args.disclosure), disclosure, force=args.force)
    print(f"RECEIPT_ID={receipt['receipt_id']}")
    print(f"DISCLOSURE={Path(args.disclosure).resolve()}")
    return 0


def command_verify(args: argparse.Namespace) -> int:
    artifact = load_artifact(Path(args.artifact))
    receipt = load_json(Path(args.receipt))
    opening = load_json(Path(args.disclosure or args.opening_record))
    result = verify_opening(artifact, receipt, opening)
    print(f"RECEIPT_STRUCTURE={result['receipt_structure']}")
    print(f"ARTIFACT_BYTE_LENGTH_MATCH={result['artifact_byte_length_match']}")
    print(f"COMMITMENT_MATCH={result['commitment_match']}")
    print(f"TIME_EVIDENCE={result['time_evidence']}")
    print(f"VERDICT={result['verdict']}")
    return 0 if result["verdict"] == "SAMPLE_CONTENT_COMMITMENT_MATCH" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Operate the synthetic content-commitment sample.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    commit_parser = subparsers.add_parser("commit", help="create a sample receipt and opening record")
    commit_parser.add_argument("--artifact", required=True)
    commit_parser.add_argument("--receipt", required=True)
    commit_parser.add_argument("--opening-record", required=True)
    commit_parser.add_argument("--artifact-label")
    commit_parser.add_argument("--claimed-created-at")
    commit_parser.add_argument(
        "--nonce-hex",
        help="fixed nonce for deterministic synthetic examples only; omit for an unscripted experiment",
    )
    commit_parser.add_argument("--force", action="store_true")
    commit_parser.set_defaults(handler=command_commit)

    disclose_parser = subparsers.add_parser("disclose", help="create a disclosure from an opening record")
    disclose_parser.add_argument("--receipt", required=True)
    disclose_parser.add_argument("--opening-record", required=True)
    disclose_parser.add_argument("--disclosure", required=True)
    disclose_parser.add_argument("--force", action="store_true")
    disclose_parser.set_defaults(handler=command_disclose)

    verify_parser = subparsers.add_parser("verify", help="compare an artifact and opening with a sample receipt")
    verify_parser.add_argument("--artifact", required=True)
    verify_parser.add_argument("--receipt", required=True)
    opening_group = verify_parser.add_mutually_exclusive_group(required=True)
    opening_group.add_argument("--disclosure")
    opening_group.add_argument("--opening-record")
    verify_parser.set_defaults(handler=command_verify)
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.handler(args)
    except SampleReceiptError as exc:
        print(f"ERROR={exc}", file=sys.stderr)
        print("VERDICT=INVALID_SAMPLE_INPUT", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR={exc}", file=sys.stderr)
        print("VERDICT=IO_ERROR", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
