import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUAL_PUBLISHER = ROOT / "scripts" / "publish_sample_packages_manual.py"
SPEC = importlib.util.spec_from_file_location("publish_sample_packages_manual", MANUAL_PUBLISHER)
assert SPEC is not None and SPEC.loader is not None
publication = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publication)
ACTIONS_PUBLISHER = ROOT / ".github" / "workflows" / "publish-sample-packages.yml"

EXPECTED_COMPONENTS = {
    "proof_engine": {
        "repository": "witnessops/witnessops-proof-engine",
        "commit": "24c13c96bc58ebfb51c159e466ba672f44b4d426",
    },
    "verifier": {
        "repository": "witnessops/witnessops-verifier",
        "commit": "c85fe398eaba915304f71d366e20fc8b144f4d33",
    },
    "contracts": {
        "repository": "witnessops/witnessops-contracts",
        "commit": "b344ed1610a07fbb8a03d5eff9480765610b89a0",
    },
}


def test_manual_publication_pins_exact_component_revisions():
    assert publication.PINNED_COMPONENTS == EXPECTED_COMPONENTS


def test_publication_provenance_records_manual_review_boundary():
    actual = {key: value["commit"] for key, value in EXPECTED_COMPONENTS.items()}
    provenance = publication.build_provenance(actual)

    assert provenance["provenance_version"] == "witnessops.sample-publication-provenance.v1"
    assert provenance["generated_by"] == "scripts/publish_sample_packages_manual.py"
    assert provenance["publication_mode"] == "manual_local_reviewed_pull_request"
    assert provenance["published_package_paths"] == publication.PUBLISHED_PACKAGE_PATHS
    assert provenance["component_revisions"] == [
        {
            "repository": EXPECTED_COMPONENTS[key]["repository"],
            "commit": EXPECTED_COMPONENTS[key]["commit"],
        }
        for key in ("proof_engine", "verifier", "contracts")
    ]
    assert any("does not commit or push" in item for item in provenance["limitations"])


def test_automatic_actions_publisher_is_removed():
    assert not ACTIONS_PUBLISHER.exists()


def test_manual_publisher_has_no_repository_write_or_credential_path():
    source = MANUAL_PUBLISHER.read_text(encoding="utf-8")
    for forbidden in (
        "git push",
        "git commit",
        "contents: write",
        "GITHUB_TOKEN",
        "WITNESSOPS_CI_READ_TOKEN",
    ):
        assert forbidden not in source
