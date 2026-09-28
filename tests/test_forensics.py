from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from cybertwin_forensics import EvidenceVault, count_bits_changed, sha256_file, verify_chain, verify_integrity
from cybertwin_forensics.demo import create_synthetic_evidence, run_avalanche, simulate_attack


class ForensicEngineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.evidence = self.base / "evidence"
        self.e1, self.tampered, self.e2, self.e3, self.original = create_synthetic_evidence(self.evidence)
        self.vault_path = self.base / "evidence_vault.json"
        self.vault = EvidenceVault(self.vault_path, handler="Test Investigator")

    def tearDown(self):
        self.temp.cleanup()

    def test_nist_sha256_vectors(self):
        self.assertEqual(hashlib.sha256(b"abc").hexdigest(), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
        self.assertEqual(hashlib.sha256(b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq").hexdigest(), "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1")

    def test_chunk_size_invariance(self):
        expected = sha256_file(self.e1)
        for size in (1, 7, 64, 65536):
            self.assertEqual(sha256_file(self.e1, size), expected)

    def test_ingest_and_integrity_audit(self):
        record = self.vault.ingest(self.e1, "CASE-TEST", "Synthetic chat")
        self.assertTrue(verify_integrity(self.vault, self.e1, record["evidence_id"]))
        self.assertFalse(verify_integrity(self.vault, self.tampered, record["evidence_id"]))
        self.assertEqual(len(self.vault.log), 3)

    def test_chain_and_external_anchor(self):
        self.vault.ingest(self.e1, "CASE-TEST", "Synthetic chat")
        self.vault.ingest(self.e2, "CASE-TEST", "Synthetic SMS")
        self.vault.ingest(self.e3, "CASE-TEST", "Synthetic screenshot")
        anchor = (len(self.vault.log), self.vault.log[-1]["entry_hash"])
        self.assertEqual(verify_chain(self.vault, anchor), [])
        self.vault.records[0]["sha256_digest"] = sha256_file(self.tampered)
        self.assertTrue(verify_chain(self.vault, anchor))

    def test_attack_levels_are_detected(self):
        self.vault.ingest(self.e1, "CASE-TEST", "Synthetic chat")
        self.vault.ingest(self.e2, "CASE-TEST", "Synthetic SMS")
        self.vault.ingest(self.e3, "CASE-TEST", "Synthetic screenshot")
        anchor = (len(self.vault.log), self.vault.log[-1]["entry_hash"])
        tampered_hash = sha256_file(self.tampered)
        for level in (1, 2, 3):
            attacked = simulate_attack(self.vault_path, level, tampered_hash)
            self.assertTrue(verify_chain(attacked, anchor), f"L{level} should be detected")

    def test_persistence(self):
        self.vault.ingest(self.e1, "CASE-TEST", "Synthetic chat")
        reloaded = EvidenceVault(self.vault_path)
        self.assertEqual(reloaded.records, self.vault.records)
        self.assertEqual(reloaded.log, self.vault.log)

    def test_avalanche_distribution_is_near_50_percent(self):
        mean, std, values = run_avalanche(self.original, trials=1000, seed=42)
        self.assertEqual(len(values), 1000)
        self.assertGreaterEqual(mean, 120)
        self.assertLessEqual(mean, 136)
        self.assertGreater(std, 0)

    def test_bit_distance(self):
        self.assertEqual(count_bits_changed("00", "ff"), 8)
        self.assertEqual(count_bits_changed("0f", "f0"), 8)


if __name__ == "__main__":
    unittest.main()
