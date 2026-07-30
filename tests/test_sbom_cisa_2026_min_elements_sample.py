import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "sample-cases" / "sbom-cisa-2026-minimum-elements"

REQUIRED_FILES = [
    "README.md",
    "BUYER_WALKTHROUGH.md",
    "AUTHORITY_MAP.json",
    "ACTION_BOUNDARY.json",
    "EVIDENCE_MANIFEST.json",
    "RECEIPT.json",
    "VERIFY_RESULT.json",
    "SAMPLE_DELIVERABLE_PLAN.md",
    "CHALLENGE_PATH.md",
    "MANIFEST.sha256",
    "artifacts/synthetic_sbom.cdx.json",
    "artifacts/generation_context.json",
    "artifacts/min_elements_checklist.json",
]

# Affirmative overclaim phrases only (negative "does not claim X" language is allowed).
FORBIDDEN_CLAIM_MARKERS = [
    "this sbom is cisa-compliant",
    "this sample is cisa-compliant",
    "certifies cisa compliance",
    "certified cisa compliant",
    "the software has no known exploited vulnerabilities",
    "proves the software is free of vulnerabilities",
]


def test_sbom_cisa_2026_sample_files_exist():
    for relative in REQUIRED_FILES:
        assert (SAMPLE / relative).exists(), f"missing SBOM sample file: {relative}"


def test_sbom_cisa_2026_receipt_is_sample_bounded():
    receipt = json.loads((SAMPLE / "RECEIPT.json").read_text(encoding="utf-8"))
    verify_result = json.loads((SAMPLE / "VERIFY_RESULT.json").read_text(encoding="utf-8"))
    authority_map = json.loads((SAMPLE / "AUTHORITY_MAP.json").read_text(encoding="utf-8"))
    action_boundary = json.loads((SAMPLE / "ACTION_BOUNDARY.json").read_text(encoding="utf-8"))

    assert receipt["signature"]["type"] == "simulated"
    assert receipt["action"]["production"] is False
    assert receipt["authority"]["decision"] == "recorded"
    assert "CISA or federal compliance certification" in receipt["verification_boundaries"]["not_verified"]
    assert "vulnerability-free software" in receipt["verification_boundaries"]["not_verified"]
    assert verify_result["result"] == "pass_with_sample_limitations"
    assert authority_map["authority_boundary"]["system_touched"]["production"] is False
    assert action_boundary["action"]["production"] is False


def test_sbom_cisa_2026_manifest_uses_relative_hashes_and_matches_files():
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


def test_sbom_cisa_2026_receipt_references_existing_artifacts():
    receipt = json.loads((SAMPLE / "RECEIPT.json").read_text(encoding="utf-8"))
    evidence_manifest = json.loads((SAMPLE / "EVIDENCE_MANIFEST.json").read_text(encoding="utf-8"))

    for key in ["authority_map", "action_boundary"]:
        assert (SAMPLE / receipt["authority"][key]).exists()

    for key in [
        "synthetic_sbom",
        "generation_context",
        "min_elements_checklist",
        "manifest",
        "hash_manifest",
        "sample_deliverable_plan",
        "challenge_path",
    ]:
        assert (SAMPLE / receipt["evidence"][key]).exists()

    for item in evidence_manifest["items"]:
        assert (SAMPLE / item["path"]).exists()


def test_sbom_cisa_2026_artifact_hash_references_match_local_files():
    receipt = json.loads((SAMPLE / "RECEIPT.json").read_text(encoding="utf-8"))
    evidence_manifest = json.loads((SAMPLE / "EVIDENCE_MANIFEST.json").read_text(encoding="utf-8"))
    verify_result = json.loads((SAMPLE / "VERIFY_RESULT.json").read_text(encoding="utf-8"))

    path_to_hash = {
        item["path"]: item["sha256"] for item in evidence_manifest["items"]
    }

    for relative in [
        "artifacts/synthetic_sbom.cdx.json",
        "artifacts/generation_context.json",
        "artifacts/min_elements_checklist.json",
    ]:
        local_hash = f"sha256:{hashlib.sha256((SAMPLE / relative).read_bytes()).hexdigest()}"
        assert path_to_hash[relative] == local_hash

    assert evidence_manifest["evidence_manifest_id"] == receipt["evidence"]["evidence_manifest_id"]

    checks = {check["name"]: check for check in verify_result["checks"]}
    assert (
        checks["synthetic_sbom_hash_matches_manifest"]["observed"]
        == path_to_hash["artifacts/synthetic_sbom.cdx.json"]
    )
    assert (
        checks["generation_context_hash_matches_manifest"]["observed"]
        == path_to_hash["artifacts/generation_context.json"]
    )
    assert (
        checks["min_elements_checklist_hash_matches_manifest"]["observed"]
        == path_to_hash["artifacts/min_elements_checklist.json"]
    )
    assert (
        checks["evidence_manifest_id_matches_receipt"]["observed"]
        == evidence_manifest["evidence_manifest_id"]
    )


def test_sbom_cisa_2026_checklist_names_intentional_gaps():
    checklist = json.loads(
        (SAMPLE / "artifacts" / "min_elements_checklist.json").read_text(encoding="utf-8")
    )
    sbom = json.loads(
        (SAMPLE / "artifacts" / "synthetic_sbom.cdx.json").read_text(encoding="utf-8")
    )
    verify_result = json.loads((SAMPLE / "VERIFY_RESULT.json").read_text(encoding="utf-8"))

    assert checklist["summary"]["overall"] == "partial_with_named_gaps"
    assert checklist["summary"]["intentional_sample_gaps"] == 2

    component_by_name = {c["name"]: c for c in sbom["components"]}
    assert "licenses" not in component_by_name["gap-demo-lib"]
    assert "hashes" not in component_by_name["license-only-lib"]

    partial = [
        row for row in checklist["component_level_elements"] if row["status"] == "partial"
    ]
    assert len(partial) == 2
    assert any(row["element"] == "Component Hash Algorithm" for row in partial)
    assert any(row["element"] == "Component License" for row in partial)

    checks = {check["name"]: check for check in verify_result["checks"]}
    assert checks["checklist_names_intentional_component_gaps"]["observed"] == 2


def test_sbom_cisa_2026_readme_and_generation_context_cite_cisa_2026():
    readme = (SAMPLE / "README.md").read_text(encoding="utf-8")
    generation = json.loads(
        (SAMPLE / "artifacts" / "generation_context.json").read_text(encoding="utf-8")
    )

    assert "CISA 2026" in readme
    assert "sample_receipt_shape_ready" in readme
    assert "does **not** claim CISA" in readme or "does not claim CISA" in readme.lower()
    assert (
        generation["cisa_reference"]["resource_url"]
        == "https://www.cisa.gov/resources-tools/resources/2026-minimum-elements-software-bill-materials-sbom"
    )


def test_sbom_cisa_2026_avoids_overclaim_markers_in_machine_json():
    # Markdown may quote blocked phrases as anti-patterns; JSON receipts must not claim them.
    for path in SAMPLE.rglob("*.json"):
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for marker in FORBIDDEN_CLAIM_MARKERS:
            assert marker.lower() not in text, f"{path}: forbidden claim marker {marker!r}"


def test_sbom_cisa_2026_deliverable_plan_lists_blocked_client_language():
    plan = (SAMPLE / "SAMPLE_DELIVERABLE_PLAN.md").read_text(encoding="utf-8")
    assert "## Explicit exclusions" in plan
    assert "Blocked:" in plan
    assert "CISA-compliant" in plan
    assert "compliance certification" in plan.lower()
