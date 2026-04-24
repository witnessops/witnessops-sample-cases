from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

SOURCE_TO_DESTINATION = {
    "privileged-access-approval-pass": "privileged-access-approval/pass/package",
    "privileged-access-approval-partial-missing-removal": "privileged-access-approval/partial-missing-removal/package",
    "privileged-access-approval-fail-scope-mismatch": "privileged-access-approval/fail-scope-mismatch/package",
}

REQUIRED_PACKAGE_FILES = [
    "README.md",
    "package_index.json",
    "receipt.json",
    "evidence_manifest.json",
    "verification_result.json",
    "report.md",
    "public_key.json",
    "results/comparison_result.json",
]

FORBIDDEN_SUFFIXES = [".hex"]
FORBIDDEN_MARKERS = [
    "private_key",
    "signing_seed",
    "secret_key",
    "kms_token",
    "hsm_credential",
    "client_secret",
]


def copy_package(source_dir: Path, destination_dir: Path) -> None:
    if not source_dir.exists():
        raise FileNotFoundError(f"missing source package: {source_dir}")

    if destination_dir.exists():
        shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)

    validate_imported_package(destination_dir)


def validate_imported_package(package_dir: Path) -> None:
    for relative in REQUIRED_PACKAGE_FILES:
        path = package_dir / relative
        if not path.exists():
            raise FileNotFoundError(f"missing required package file: {package_dir}/{relative}")

    if not (package_dir / "evidence").is_dir():
        raise FileNotFoundError(f"missing evidence directory: {package_dir}/evidence")
    if not (package_dir / "normalized").is_dir():
        raise FileNotFoundError(f"missing normalized directory: {package_dir}/normalized")

    verification_result = load_json(package_dir / "verification_result.json")
    package_index = load_json(package_dir / "package_index.json")
    receipt = load_json(package_dir / "receipt.json")

    if verification_result["status"] != "valid":
        raise ValueError(f"sample package verification status must be valid: {package_dir}")
    if package_index["verification_status"] != verification_result["status"]:
        raise ValueError("package_index.verification_status does not match verification_result.status")
    if package_index["verification_result_source"] != "witnessops_verifier":
        raise ValueError("package_index must identify witnessops_verifier as verification result source")
    if package_index["workflow_class"] != receipt["workflow_class"]:
        raise ValueError("package_index workflow_class does not match receipt")
    if package_index["proof_run_id"] != receipt["proof_run_id"]:
        raise ValueError("package_index proof_run_id does not match receipt")
    if package_index["outcome"] != receipt["result"]["outcome"]:
        raise ValueError("package_index outcome does not match receipt")

    assert_no_forbidden_material(package_dir)


def assert_no_forbidden_material(package_dir: Path) -> None:
    for path in package_dir.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(package_dir).as_posix().lower()
        if any(relative.endswith(suffix) for suffix in FORBIDDEN_SUFFIXES):
            raise ValueError(f"forbidden key-like file in package: {relative}")
        content = path.read_text(encoding="utf-8", errors="ignore").lower()
        for marker in FORBIDDEN_MARKERS:
            if marker in relative or marker in content:
                raise ValueError(f"forbidden marker {marker} found in {relative}")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def import_sample_packages(source_root: Path, repo_root: Path) -> list[Path]:
    imported = []
    for source_name, destination_relative in SOURCE_TO_DESTINATION.items():
        source_dir = source_root / source_name
        destination_dir = repo_root / destination_relative
        copy_package(source_dir, destination_dir)
        imported.append(destination_dir)
    return imported


def main() -> None:
    parser = argparse.ArgumentParser(description="Import exported WitnessOps sample packages into witnessops-sample-cases")
    parser.add_argument("--source-root", required=True, help="Directory containing exported sample package folders")
    parser.add_argument("--repo-root", default=".", help="Root of witnessops-sample-cases checkout")
    args = parser.parse_args()

    imported = import_sample_packages(Path(args.source_root), Path(args.repo_root))
    for path in imported:
        print(path)


if __name__ == "__main__":
    main()
