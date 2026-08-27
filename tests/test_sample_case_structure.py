import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AI_AGENT_ACTION_SAMPLE = ROOT / "sample-cases" / "ai-agent-action-proof-run"

PLANNED_CASES = {
    "privileged-access-approval/pass": {
        "expected_outcome": "outcome = pass",
        "expected_failure": "failure_states = []",
    },
    "privileged-access-approval/partial-missing-removal": {
        "expected_outcome": "outcome = partial",
        "expected_failure": "missing_removal_proof",
    },
    "privileged-access-approval/fail-scope-mismatch": {
        "expected_outcome": "outcome = fail",
        "expected_failure": "scope_mismatch",
    },
}

PUBLISHED_SAMPLE_ROOT = ROOT / "sample-cases"
PUBLISHED_SAMPLE_MANIFEST = PUBLISHED_SAMPLE_ROOT / "SAMPLE_CASES_MANIFEST.v1.yaml"

REQUIRED_DOCS = [
    "README.md",
    "REPO_MAP.md",
    "privileged-access-approval/README.md",
    "docs/how-to-verify-sample.md",
    "docs/sample-case-boundaries.md",
    "docs/evidence-redaction-policy.md",
    "docs/import-sample-packages.md",
    "docs/import-publication-policy.md",
    "docs/publish-sample-packages-workflow.md",
]

REQUIRED_AI_AGENT_ACTION_FILES = [
    "README.md",
    "AUTHORITY_MAP.json",
    "ACTION_BOUNDARY.json",
    "BUNDLE.wops.json",
    "BUYER_WALKTHROUGH.md",
    "CHALLENGE_PATH.md",
    "DEMO_KEY_REGISTRY.json",
    "DEMO_PUBLIC_KEY.pem",
    "EVIDENCE_MANIFEST.json",
    "RECEIPT.json",
    "VERIFY_RESULT.json",
    "evidence/AFTER.json",
    "evidence/ALERT.json",
    "evidence/BEFORE.json",
    "evidence/CHECKS.json",
    "evidence/EVENTS.ndjson",
    "MANIFEST.sha256",
]

FORBIDDEN_MARKERS = [
    "private_key",
    "signing_seed",
    "secret_key",
    "api_token",
    "access_token",
    "client_secret",
    "real customer evidence",
]


def test_required_docs_exist():
    for relative in REQUIRED_DOCS:
        assert (ROOT / relative).exists(), f"missing required doc: {relative}"


def test_publication_policy_contains_required_gate_language():
    policy = (ROOT / "docs" / "import-publication-policy.md").read_text(encoding="utf-8")
    for marker in [
        "Required verification before publication",
        "Forbidden material",
        "Required review before publication",
        "Package update rule",
        "verification_result.status = valid",
        "package_index.verification_result_source = witnessops_verifier",
    ]:
        assert marker in policy, f"publication policy missing marker: {marker}"


def test_manual_publication_doc_contains_required_gate_language():
    doc = (ROOT / "docs" / "publish-sample-packages-workflow.md").read_text(encoding="utf-8")
    for marker in [
        "Manual Sample Package Publication",
        "scripts/publish_sample_packages_manual.py",
        "Publication sequence",
        "Publication gate",
        "stop without committing or pushing",
        "verification_result.status = valid",
        "package_index.verification_result_source = witnessops_verifier",
    ]:
        assert marker in doc, f"manual publication doc missing marker: {marker}"


def _manifest_sample_paths():
    paths = []
    for line in PUBLISHED_SAMPLE_MANIFEST.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("path: "):
            paths.append(stripped.removeprefix("path: "))
    return paths


def test_published_sample_manifest_matches_directories_exactly():
    manifest_paths = _manifest_sample_paths()
    directory_paths = sorted(
        f"sample-cases/{path.name}"
        for path in PUBLISHED_SAMPLE_ROOT.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )

    assert len(manifest_paths) == len(set(manifest_paths)), "manifest contains duplicate sample paths"
    assert sorted(manifest_paths) == directory_paths


def test_manifest_entries_are_complete_synthetic_samples():
    manifest = PUBLISHED_SAMPLE_MANIFEST.read_text(encoding="utf-8")
    assert manifest.count("evidence_class: synthetic_sample") == len(_manifest_sample_paths())
    assert manifest.count("publication_state: complete") == len(_manifest_sample_paths())


def test_planned_sample_case_directories_exist():
    for relative, expectations in PLANNED_CASES.items():
        case_dir = ROOT / relative
        readme = case_dir / "README.md"
        package_dir = case_dir / "package"
        assert case_dir.exists(), f"missing case directory: {relative}"
        assert readme.exists(), f"missing case README: {relative}"
        assert package_dir.exists(), f"missing package directory: {relative}/package"

        content = readme.read_text(encoding="utf-8")
        assert expectations["expected_outcome"] in content
        assert expectations["expected_failure"] in content
        assert "Status: PLANNED / DOCUMENTATION ONLY" in content
        assert "Package path" in content


def test_planned_packages_are_empty_and_excluded_from_manifest():
    manifest_paths = set(_manifest_sample_paths())
    for relative in PLANNED_CASES:
        package_dir = ROOT / relative / "package"
        contents = {path.name for path in package_dir.iterdir()}
        assert contents == {".gitkeep"}, f"planned package must remain empty: {relative}/package"
        assert relative not in manifest_paths


def test_ai_agent_action_sample_bundle_exists_and_is_bounded():
    for relative in REQUIRED_AI_AGENT_ACTION_FILES:
        assert (AI_AGENT_ACTION_SAMPLE / relative).exists(), f"missing AI action sample file: {relative}"

    receipt = json.loads((AI_AGENT_ACTION_SAMPLE / "RECEIPT.json").read_text(encoding="utf-8"))
    verify_result = json.loads((AI_AGENT_ACTION_SAMPLE / "VERIFY_RESULT.json").read_text(encoding="utf-8"))
    authority_map = json.loads((AI_AGENT_ACTION_SAMPLE / "AUTHORITY_MAP.json").read_text(encoding="utf-8"))

    key_registry = json.loads(
        (AI_AGENT_ACTION_SAMPLE / "DEMO_KEY_REGISTRY.json").read_text(encoding="utf-8")
    )
    evidence_manifest = json.loads(
        (AI_AGENT_ACTION_SAMPLE / "EVIDENCE_MANIFEST.json").read_text(encoding="utf-8")
    )

    assert receipt["receipt_version"] == "witnessops.receipt.v0"
    assert receipt["receipt_profile"] == "witnessops.verification_context.v1"
    assert receipt["workflow_class"] == "compromised_api_key_rotation"
    assert receipt["signature"]["algorithm"] == "ed25519"
    assert receipt["signature"]["encoding"] == "hex"
    assert len(receipt["signature"]["signature"]) == 128
    assert receipt["signature"]["public_key_id"] == key_registry["keys"][0]["id"]
    assert key_registry["keys"][0]["purpose"] == "synthetic_demo_receipts_only"
    assert key_registry["keys"][0]["status"] == "retired"
    assert verify_result["verdict"] == "VALID_SYNTHETIC_SPECIMEN"
    assert authority_map["approval"]["approved"] is True
    assert authority_map["synthetic"] is True

    artifact_ids = {artifact["artifact_id"] for artifact in evidence_manifest["artifacts"]}
    assert len(artifact_ids) == len(evidence_manifest["artifacts"])
    for claim in receipt["claims"]:
        assert set(claim["evidence_refs"]).issubset(artifact_ids)

    limitations = " ".join(receipt["verification_context"]["limitations"]).lower()
    assert "no real provider" in limitations
    assert "synthetic" in limitations


def test_ai_agent_action_sample_contains_no_credential_material():
    forbidden_fields = {
        "api_key",
        "api_key_value",
        "credential_value",
        "secret",
        "secret_value",
        "token",
        "token_value",
    }

    for relative in REQUIRED_AI_AGENT_ACTION_FILES:
        path = AI_AGENT_ACTION_SAMPLE / relative
        if path.suffix not in {".json", ".ndjson"}:
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            parsed = json.loads(line) if path.suffix == ".ndjson" else None
            if parsed is not None:
                assert forbidden_fields.isdisjoint(parsed)

    for path in [
        AI_AGENT_ACTION_SAMPLE / "ACTION_BOUNDARY.json",
        AI_AGENT_ACTION_SAMPLE / "AUTHORITY_MAP.json",
        AI_AGENT_ACTION_SAMPLE / "EVIDENCE_MANIFEST.json",
        AI_AGENT_ACTION_SAMPLE / "RECEIPT.json",
        AI_AGENT_ACTION_SAMPLE / "VERIFY_RESULT.json",
        AI_AGENT_ACTION_SAMPLE / "evidence" / "ALERT.json",
        AI_AGENT_ACTION_SAMPLE / "evidence" / "BEFORE.json",
        AI_AGENT_ACTION_SAMPLE / "evidence" / "AFTER.json",
        AI_AGENT_ACTION_SAMPLE / "evidence" / "CHECKS.json",
    ]:
        value = json.loads(path.read_text(encoding="utf-8"))
        stack = [value]
        while stack:
            current = stack.pop()
            if isinstance(current, dict):
                assert forbidden_fields.isdisjoint(current)
                stack.extend(current.values())
            elif isinstance(current, list):
                stack.extend(current)


def test_ai_agent_action_manifest_uses_relative_hashes_and_matches_files():
    manifest = AI_AGENT_ACTION_SAMPLE / "MANIFEST.sha256"
    expected_files = set(REQUIRED_AI_AGENT_ACTION_FILES) - {"MANIFEST.sha256"}
    seen_files = set()

    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split(maxsplit=1)
        assert not Path(relative).is_absolute(), f"manifest path must be relative: {relative}"
        path = AI_AGENT_ACTION_SAMPLE / relative
        assert path.exists(), f"manifest references missing file: {relative}"
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == digest, f"hash mismatch for {relative}"
        seen_files.add(relative)

    assert seen_files == expected_files


def test_no_forbidden_private_or_customer_markers():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix().lower()
        if ".git" in relative:
            continue
        if relative.startswith(".github/"):
            continue
        if relative.startswith("scripts/"):
            continue
        if relative.startswith("tests/"):
            continue
        content = path.read_text(encoding="utf-8", errors="ignore").lower()
        for marker in FORBIDDEN_MARKERS:
            if marker == "real customer evidence" and "not real customer evidence" in content:
                continue
            assert marker not in relative
            assert marker not in content, f"forbidden marker {marker} found in {relative}"
