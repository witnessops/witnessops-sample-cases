from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path


SAMPLE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SAMPLE_DIR / "tools"))

import sample_content_commitment as sample_tool  # noqa: E402


class SampleContentCommitmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.artifact = b"Example artifact bytes\n"
        self.nonce = bytes(range(32))
        self.receipt = sample_tool.build_receipt(
            self.artifact,
            "example.txt",
            self.nonce,
            "2026-08-19T05:30:00Z",
        )
        self.disclosure = sample_tool.build_disclosure(self.receipt, self.nonce)

    def test_known_vector(self) -> None:
        self.assertEqual(
            sample_tool.compute_commitment(self.artifact, self.nonce),
            "addde967ed41ab1af3de55ecbb49c9d6b2561515ae75b9f96bfd6ebbebcf2ca0",
        )

    def test_round_trip_matches(self) -> None:
        result = sample_tool.verify_opening(self.artifact, self.receipt, self.disclosure)
        self.assertEqual(result["verdict"], "SAMPLE_CONTENT_COMMITMENT_MATCH")
        self.assertEqual(result["time_evidence"], "NOT_PRESENT")

    def test_one_byte_artifact_mutation_fails(self) -> None:
        mutated = bytearray(self.artifact)
        mutated[-2] ^= 1
        result = sample_tool.verify_opening(bytes(mutated), self.receipt, self.disclosure)
        self.assertEqual(result["commitment_match"], "FAIL")
        self.assertEqual(result["verdict"], "NO_MATCH")

    def test_wrong_nonce_fails(self) -> None:
        wrong_disclosure = copy.deepcopy(self.disclosure)
        wrong_disclosure["nonce"] = (b"x" * 32).hex()
        result = sample_tool.verify_opening(self.artifact, self.receipt, wrong_disclosure)
        self.assertEqual(result["commitment_match"], "FAIL")

    def test_receipt_commitment_tampering_is_rejected(self) -> None:
        tampered = copy.deepcopy(self.receipt)
        tampered["commitment"]["value"] = "0" * 64
        with self.assertRaises(sample_tool.SampleReceiptError):
            sample_tool.verify_opening(self.artifact, tampered, self.disclosure)

    def test_cross_receipt_opening_is_rejected(self) -> None:
        wrong_disclosure = copy.deepcopy(self.disclosure)
        wrong_disclosure["receipt_id"] = "wo-sample-cc-000000000000000000000000"
        with self.assertRaises(sample_tool.SampleReceiptError):
            sample_tool.verify_opening(self.artifact, self.receipt, wrong_disclosure)

    def test_external_anchor_is_not_automatically_verified(self) -> None:
        anchored = copy.deepcopy(self.receipt)
        anchored["time_evidence"]["external_anchor"] = {
            "mechanism": "RFC3161",
            "evidence_file": "receipt.tsr",
        }
        result = sample_tool.verify_opening(self.artifact, anchored, self.disclosure)
        self.assertEqual(result["time_evidence"], "PRESENT_NOT_VERIFIED")

    def test_public_receipt_omits_nonce_and_raw_artifact_hash(self) -> None:
        serialized = json.dumps(self.receipt, sort_keys=True)
        self.assertNotIn(self.nonce.hex(), serialized)
        self.assertNotIn(hashlib.sha256(self.artifact).hexdigest(), serialized)

    def test_sample_manifest_is_complete_and_matches(self) -> None:
        manifest_path = SAMPLE_DIR / "MANIFEST.sha256"
        expected = {}
        for line in manifest_path.read_text(encoding="utf-8").splitlines():
            digest, relative = line.split("  ", 1)
            expected[relative] = digest

        actual_files = {
            path.relative_to(SAMPLE_DIR).as_posix()
            for path in SAMPLE_DIR.rglob("*")
            if path.is_file()
            and path.name != "MANIFEST.sha256"
            and "__pycache__" not in path.parts
            and path.suffix != ".pyc"
        }
        self.assertEqual(set(expected), actual_files)
        for relative, digest in expected.items():
            self.assertEqual(hashlib.sha256((SAMPLE_DIR / relative).read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
