from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_CASES = {
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

REQUIRED_DOCS = [
    "README.md",
    "REPO_MAP.md",
    "privileged-access-approval/README.md",
    "docs/how-to-verify-sample.md",
    "docs/sample-case-boundaries.md",
    "docs/evidence-redaction-policy.md",
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


def test_expected_sample_case_directories_exist():
    for relative, expectations in EXPECTED_CASES.items():
        case_dir = ROOT / relative
        readme = case_dir / "README.md"
        package_dir = case_dir / "package"
        assert case_dir.exists(), f"missing case directory: {relative}"
        assert readme.exists(), f"missing case README: {relative}"
        assert package_dir.exists(), f"missing package directory: {relative}/package"

        content = readme.read_text(encoding="utf-8")
        assert expectations["expected_outcome"] in content
        assert expectations["expected_failure"] in content
        assert "Package path" in content


def test_placeholder_packages_are_marked_until_import():
    for relative in EXPECTED_CASES:
        package_dir = ROOT / relative / "package"
        gitkeep = package_dir / ".gitkeep"
        if not (package_dir / "receipt.json").exists():
            assert gitkeep.exists(), f"empty package directory must include .gitkeep: {relative}/package"


def test_no_forbidden_private_or_customer_markers():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT).as_posix().lower()
        if ".git" in relative:
            continue
        content = path.read_text(encoding="utf-8", errors="ignore").lower()
        for marker in FORBIDDEN_MARKERS:
            if marker == "real customer evidence" and "not real customer evidence" in content:
                continue
            assert marker not in relative
            assert marker not in content, f"forbidden marker {marker} found in {relative}"
