from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "publish-sample-packages.yml"

PINNED_COMPONENTS = {
    "witnessops/witnessops-proof-engine": "6511d64590e877e2285cac92c9cf4610396ea3a5",
    "witnessops/witnessops-verifier": "a279a56226972fc3a15ea960f6e1150d2e16df85",
    "witnessops/witnessops-contracts": "b344ed1610a07fbb8a03d5eff9480765610b89a0",
}


def test_publication_workflow_pins_and_records_component_revisions():
    workflow = WORKFLOW.read_text(encoding="utf-8")

    for repository, commit in PINNED_COMPONENTS.items():
        assert f"repository: {repository}" in workflow
        assert f"ref: {commit}" in workflow
        assert commit in workflow

    assert "Assert pinned component revisions" in workflow
    assert 'git -C proof-engine rev-parse HEAD' in workflow
    assert 'git -C witnessops-verifier rev-parse HEAD' in workflow
    assert 'git -C witnessops-contracts rev-parse HEAD' in workflow
    assert "PUBLICATION_PROVENANCE.json" in workflow
    assert "published_package_paths" in workflow
    assert "Commit imported packages and provenance" in workflow
