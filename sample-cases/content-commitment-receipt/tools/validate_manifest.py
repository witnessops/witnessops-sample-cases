#!/usr/bin/env python3
"""Validate this synthetic sample's MANIFEST.sha256 and reject unlisted files."""

from __future__ import annotations

import hashlib
from pathlib import Path


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    manifest_path = root / "MANIFEST.sha256"
    if not manifest_path.is_file():
        print("MANIFEST_RESULT=FAIL")
        print("ERROR=MANIFEST.sha256 is missing")
        return 1

    expected = {}
    for line_number, raw_line in enumerate(manifest_path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw_line.strip():
            continue
        try:
            expected_digest, relative_name = raw_line.split("  ", 1)
        except ValueError:
            print("MANIFEST_RESULT=FAIL")
            print(f"ERROR=invalid manifest line {line_number}")
            return 1
        relative = Path(relative_name)
        if relative.is_absolute() or ".." in relative.parts:
            print("MANIFEST_RESULT=FAIL")
            print(f"ERROR=unsafe manifest path on line {line_number}")
            return 1
        expected[relative.as_posix()] = expected_digest

    actual_files = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
        and path.name != "MANIFEST.sha256"
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    }
    expected_files = set(expected)
    missing = sorted(expected_files - actual_files)
    extra = sorted(actual_files - expected_files)
    mismatched = [
        name
        for name in sorted(expected_files & actual_files)
        if digest(root / name) != expected[name]
    ]

    if missing or extra or mismatched:
        print("MANIFEST_RESULT=FAIL")
        for name in missing:
            print(f"MISSING={name}")
        for name in extra:
            print(f"UNLISTED={name}")
        for name in mismatched:
            print(f"HASH_MISMATCH={name}")
        return 1

    print(f"MANIFEST_FILES={len(expected_files)}")
    print("MANIFEST_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
