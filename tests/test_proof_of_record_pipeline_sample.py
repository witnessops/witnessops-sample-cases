import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "sample-cases" / "proof-of-record-pipeline"

REQUIRED_FILES = [
    "README.md",
    "AUTHORITY_MAP.json",
    "ACTION_BOUNDARY.json",
    "CONNECTOR_EVENT.json",
    "CANONICAL_PAYLOAD.json",
    "EVIDENCE_MANIFEST.json",
    "RECEIPT.json",
    "VERIFY_RESULT.json",
    "CHALLENGE_PATH.md",
    "MANIFEST.sha256",
    "artifacts/source_artifact.md",
]


def test_proof_of_record_pipeline_sample_files_exist():
    for relative in REQUIRED_FILES:
        assert (SAMPLE / relative).exists(), f"missing Proof-Of-Record sample file: {relative}"


def test_proof_of_record_pipeline_receipt_is_sample_bounded():
    receipt = json.loads((SAMPLE / "RECEIPT.json").read_text(encoding="utf-8"))
    verify_result = json.loads((SAMPLE / "VERIFY_RESULT.json").read_text(encoding="utf-8"))
    authority_map = json.loads((SAMPLE / "AUTHORITY_MAP.json").read_text(encoding="utf-8"))

    assert receipt["signature"]["type"] == "simulated"
    assert receipt["action"]["production"] is False
    assert receipt["authority"]["decision"] == "recorded"
    assert "source-system honesty" in receipt["verification_boundaries"]["not_verified"]
    assert verify_result["result"] == "pass_with_sample_limitations"
    assert authority_map["authority_boundary"]["system_touched"]["production"] is False


def test_proof_of_record_pipeline_manifest_uses_relative_hashes_and_matches_files():
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


def test_proof_of_record_pipeline_receipt_references_existing_artifacts():
    receipt = json.loads((SAMPLE / "RECEIPT.json").read_text(encoding="utf-8"))
    evidence_manifest = json.loads((SAMPLE / "EVIDENCE_MANIFEST.json").read_text(encoding="utf-8"))

    for key in ["authority_map", "action_boundary"]:
        assert (SAMPLE / receipt["authority"][key]).exists()

    for key in ["canonical_payload", "manifest", "hash_manifest", "challenge_path"]:
        assert (SAMPLE / receipt["evidence"][key]).exists()

    for item in evidence_manifest["items"]:
        assert (SAMPLE / item["path"]).exists()


def test_proof_of_record_pipeline_payload_hash_references_match_local_file():
    receipt = json.loads((SAMPLE / "RECEIPT.json").read_text(encoding="utf-8"))
    evidence_manifest = json.loads((SAMPLE / "EVIDENCE_MANIFEST.json").read_text(encoding="utf-8"))
    verify_result = json.loads((SAMPLE / "VERIFY_RESULT.json").read_text(encoding="utf-8"))

    payload_path = SAMPLE / receipt["evidence"]["canonical_payload"]
    payload_hash = f"sha256:{hashlib.sha256(payload_path.read_bytes()).hexdigest()}"

    assert receipt["evidence"]["canonical_payload_hash"] == payload_hash
    assert evidence_manifest["canonical_payload_hash"] == payload_hash
    assert evidence_manifest["evidence_manifest_id"] == receipt["evidence"]["evidence_manifest_id"]

    checks = {check["name"]: check for check in verify_result["checks"]}
    assert checks["canonical_payload_hash_matches_receipt"]["observed"] == payload_hash
    assert checks["evidence_manifest_id_matches_receipt"]["observed"] == evidence_manifest["evidence_manifest_id"]
