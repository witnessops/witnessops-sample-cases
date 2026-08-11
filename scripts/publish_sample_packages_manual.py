#!/usr/bin/env python3
"""Regenerate public sample packages from pinned local WitnessOps checkouts.

This command is intentionally local-only. It never commits, pushes, or reads a
GitHub credential. The operator reviews the resulting working-tree diff and
publishes it through an ordinary pull request.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Sequence


PINNED_COMPONENTS = {
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

PUBLISHED_PACKAGE_PATHS = [
    "privileged-access-approval/pass/package",
    "privileged-access-approval/partial-missing-removal/package",
    "privileged-access-approval/fail-scope-mismatch/package",
]

EXPORTS = [
    ("pass", "pass"),
    ("partial_missing_removal", "partial"),
    ("fail_scope_mismatch", "fail"),
]


def _output(command: Sequence[str], *, cwd: Path) -> str:
    return subprocess.check_output(command, cwd=cwd, text=True).strip()


def _run(command: Sequence[str], *, cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def _require_clean_checkout(path: Path, label: str) -> None:
    if not path.is_dir():
        raise SystemExit(f"{label} checkout does not exist: {path}")
    status = _output(["git", "status", "--porcelain"], cwd=path)
    if status:
        raise SystemExit(f"{label} checkout must be clean before publication: {path}")


def _require_publication_branch(repo_root: Path) -> str:
    branch = _output(["git", "branch", "--show-current"], cwd=repo_root)
    if not branch:
        raise SystemExit("sample-cases must be on a named publication branch")
    if branch in {"main", "master", "develop"}:
        raise SystemExit(
            f"refusing to generate on default branch {branch!r}; create a publication branch"
        )
    return branch


def _require_pinned_head(path: Path, component_key: str) -> str:
    expected = PINNED_COMPONENTS[component_key]["commit"]
    actual = _output(["git", "rev-parse", "HEAD"], cwd=path)
    if actual != expected:
        repository = PINNED_COMPONENTS[component_key]["repository"]
        raise SystemExit(f"{repository}: expected {expected}, got {actual}")
    return actual


def build_provenance(actual_commits: dict[str, str]) -> dict:
    return {
        "provenance_version": "witnessops.sample-publication-provenance.v1",
        "generated_by": "scripts/publish_sample_packages_manual.py",
        "publication_mode": "manual_local_reviewed_pull_request",
        "component_revisions": [
            {
                "repository": PINNED_COMPONENTS[key]["repository"],
                "commit": actual_commits[key],
            }
            for key in ("proof_engine", "verifier", "contracts")
        ],
        "published_package_paths": PUBLISHED_PACKAGE_PATHS,
        "limitations": [
            "Records component revisions used by this publication only.",
            "Does not establish production signing or key custody.",
            "Does not attribute packages committed before this record existed.",
            "The script does not commit or push; a reviewed pull request is required.",
        ],
    }


def _validate_contract_artifacts(repo_root: Path, contracts_dir: Path) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise SystemExit(
            "jsonschema is required; install the pinned component development dependencies"
        ) from exc

    packages = {
        "privileged-access-approval/pass/package": "pass",
        "privileged-access-approval/partial-missing-removal/package": "partial",
        "privileged-access-approval/fail-scope-mismatch/package": "fail",
    }
    schema_paths = {
        "package_index": contracts_dir / "schemas/package-index.schema.json",
        "verification_result": contracts_dir / "schemas/verifier-result.schema.json",
        "receipt": contracts_dir / "schemas/receipt.schema.json",
        "manifest": contracts_dir / "schemas/evidence-manifest.schema.json",
    }
    validators = {}
    for name, schema_path in schema_paths.items():
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validators[name] = Draft202012Validator(schema)

    for package_relative, expected_outcome in packages.items():
        package = repo_root / package_relative
        instances = {
            "package_index": package / "package_index.json",
            "verification_result": package / "verification_result.json",
            "receipt": package / "receipt.json",
            "manifest": package / "evidence_manifest.json",
        }
        loaded = {}
        for name, path in instances.items():
            instance = json.loads(path.read_text(encoding="utf-8"))
            errors = sorted(
                validators[name].iter_errors(instance), key=lambda error: list(error.path)
            )
            if errors:
                raise SystemExit(f"{package_relative}/{name} failed schema validation: {errors}")
            loaded[name] = instance

        verification_result = loaded["verification_result"]
        package_index = loaded["package_index"]
        receipt = loaded["receipt"]
        if verification_result["status"] != "valid":
            raise SystemExit(f"{package_relative}: verifier status is not valid")
        if verification_result["outcome"] != expected_outcome:
            raise SystemExit(f"{package_relative}: unexpected verifier outcome")
        if receipt["result"]["outcome"] != expected_outcome:
            raise SystemExit(f"{package_relative}: unexpected receipt outcome")
        if package_index["outcome"] != expected_outcome:
            raise SystemExit(f"{package_relative}: unexpected package-index outcome")
        if package_index["verification_status"] != "valid":
            raise SystemExit(f"{package_relative}: package index is not verified")
        if package_index["verification_result_source"] != "witnessops_verifier":
            raise SystemExit(f"{package_relative}: unexpected verifier source")


def publish(
    *,
    repo_root: Path,
    proof_engine_dir: Path,
    verifier_dir: Path,
    contracts_dir: Path,
) -> None:
    repo_root = repo_root.resolve()
    proof_engine_dir = proof_engine_dir.resolve()
    verifier_dir = verifier_dir.resolve()
    contracts_dir = contracts_dir.resolve()

    _require_clean_checkout(repo_root, "sample-cases")
    branch = _require_publication_branch(repo_root)
    checkouts = {
        "proof_engine": proof_engine_dir,
        "verifier": verifier_dir,
        "contracts": contracts_dir,
    }
    actual_commits = {}
    for key, path in checkouts.items():
        _require_clean_checkout(path, PINNED_COMPONENTS[key]["repository"])
        actual_commits[key] = _require_pinned_head(path, key)

    with tempfile.TemporaryDirectory(prefix="witnessops-sample-publication-") as tmp:
        export_root = Path(tmp)
        for fixture, _expected_outcome in EXPORTS:
            _run(
                [
                    sys.executable,
                    "scripts/export_sample_package.py",
                    "--fixture",
                    fixture,
                    "--output-dir",
                    str(export_root),
                    "--signed",
                    "--verifier-dir",
                    str(verifier_dir),
                    "--contracts-dir",
                    str(contracts_dir),
                ],
                cwd=proof_engine_dir,
            )

        _run(
            [
                sys.executable,
                "scripts/import_sample_packages.py",
                "--source-root",
                str(export_root),
                "--repo-root",
                str(repo_root),
            ],
            cwd=repo_root,
        )

    _validate_contract_artifacts(repo_root, contracts_dir)
    _run([sys.executable, "-m", "pytest", "-q"], cwd=repo_root)

    provenance = build_provenance(actual_commits)
    (repo_root / "PUBLICATION_PROVENANCE.json").write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"Generated and validated on branch {branch!r}.")
    print("No commit or push was performed. Review the working-tree diff and open a PR.")
    subprocess.run(["git", "status", "--short"], cwd=repo_root, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenerate pinned WitnessOps sample packages without GitHub write authority"
    )
    parser.add_argument("--repo-root", default=".", type=Path)
    parser.add_argument("--proof-engine-dir", required=True, type=Path)
    parser.add_argument("--verifier-dir", required=True, type=Path)
    parser.add_argument("--contracts-dir", required=True, type=Path)
    args = parser.parse_args()
    publish(
        repo_root=args.repo_root,
        proof_engine_dir=args.proof_engine_dir,
        verifier_dir=args.verifier_dir,
        contracts_dir=args.contracts_dir,
    )


if __name__ == "__main__":
    main()
