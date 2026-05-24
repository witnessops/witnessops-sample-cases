import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "sample-cases" / "phone-security-proof-pack"

REQUIRED_FILES = [
    "README.md",
    "AUTHORITY_MAP.json",
    "ACTION_BOUNDARY.json",
    "EVIDENCE_MANIFEST.json",
    "RECEIPT.json",
    "VERIFY_RESULT.json",
    "SAMPLE_DELIVERABLE_PLAN.md",
    "CHALLENGE_PATH.md",
    "MANIFEST.sha256",
    "artifacts/device_check_summary.md",
]


def test_phone_security_proof_pack_sample_files_exist():
    for relative in REQUIRED_FILES:
        assert (SAMPLE / relative).exists(), f"missing phone security sample file: {relative}"


def test_phone_security_proof_pack_receipt_is_sample_bounded():
    receipt = json.loads((SAMPLE / "RECEIPT.json").read_text(encoding="utf-8"))
    verify_result = json.loads((SAMPLE / "VERIFY_RESULT.json").read_text(encoding="utf-8"))
    authority_map = json.loads((SAMPLE / "AUTHORITY_MAP.json").read_text(encoding="utf-8"))

    assert receipt["signature"]["type"] == "simulated"
    assert receipt["action"]["production"] is False
    assert receipt["authority"]["decision"] == "recorded"
    assert "spyware detection" in receipt["verification_boundaries"]["not_verified"]
    assert "absence of compromise" in receipt["verification_boundaries"]["not_verified"]
    assert verify_result["result"] == "pass_with_sample_limitations"
    assert authority_map["authority_boundary"]["system_touched"]["production"] is False


def test_phone_security_proof_pack_manifest_uses_relative_hashes_and_matches_files():
    manifest = SAMPLE / "MANIFEST.sha256"
    expected_files = set(REQUIRED_FILES) - {"MANIFEST.sha256"}
    seen_files = set()

    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split(maxsplit=1)
        assert not Path(relative).is_absolute(), f"manifest path must be relative: {relative}"
        path = SAMPLE / relative
        assert path.exists(), f"manifest references missing file: {relative}"
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == digest, f"hash mismatch for {relative}"
        seen_files.add(relative)

    assert seen_files == expected_files


def test_phone_security_proof_pack_receipt_references_existing_artifacts():
    receipt = json.loads((SAMPLE / "RECEIPT.json").read_text(encoding="utf-8"))
    evidence_manifest = json.loads((SAMPLE / "EVIDENCE_MANIFEST.json").read_text(encoding="utf-8"))

    for key in ["authority_map", "action_boundary"]:
        assert (SAMPLE / receipt["authority"][key]).exists()

    for key in [
        "device_check_summary",
        "manifest",
        "hash_manifest",
        "sample_deliverable_plan",
        "challenge_path",
    ]:
        assert (SAMPLE / receipt["evidence"][key]).exists()

    for item in evidence_manifest["items"]:
        assert (SAMPLE / item["path"]).exists()


def test_phone_security_proof_pack_summary_hash_references_match_local_file():
    receipt = json.loads((SAMPLE / "RECEIPT.json").read_text(encoding="utf-8"))
    evidence_manifest = json.loads((SAMPLE / "EVIDENCE_MANIFEST.json").read_text(encoding="utf-8"))
    verify_result = json.loads((SAMPLE / "VERIFY_RESULT.json").read_text(encoding="utf-8"))

    summary_path = SAMPLE / receipt["evidence"]["device_check_summary"]
    summary_hash = f"sha256:{hashlib.sha256(summary_path.read_bytes()).hexdigest()}"

    summary_item = next(
        item for item in evidence_manifest["items"] if item["path"] == "artifacts/device_check_summary.md"
    )
    assert summary_item["sha256"] == summary_hash
    assert evidence_manifest["evidence_manifest_id"] == receipt["evidence"]["evidence_manifest_id"]

    checks = {check["name"]: check for check in verify_result["checks"]}
    assert checks["device_check_summary_hash_matches_manifest"]["observed"] == summary_hash
    assert checks["evidence_manifest_id_matches_receipt"]["observed"] == evidence_manifest["evidence_manifest_id"]
