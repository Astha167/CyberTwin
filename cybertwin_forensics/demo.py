"""Synthetic end-to-end demonstration for the CyberTwin forensic engine."""

from __future__ import annotations

import hashlib
import json
import random
import tempfile
from pathlib import Path

from .core import (
    CHUNK_SIZE,
    GENESIS,
    EvidenceVault,
    count_bits_changed,
    entry_digest,
    sha256_file,
    verify_chain,
    verify_integrity,
)

CHAT = [
    "[2026-09-27 14:15:02] Impersonator: Hey, my phone broke. Using a temporary number.",
    "[2026-09-27 14:15:30] Impersonator: Urgent: Can you send Rs 50,000 to account #987654321?",
    "[2026-09-27 14:16:10] Victim: Who is this? Your display photo looks like Rohan.",
    "[2026-09-27 14:16:45] Impersonator: Yes it is Rohan! Please hurry, it's an emergency!",
]
SMS = [
    "27-09-26 14:18 IST: A/c XX4321 debited by Rs 50,000.00 via IMPS to A/c 987654321.",
    "Not you? Report immediately on 1930 or cybercrime.gov.in",
]


def create_synthetic_evidence(evidence_dir: Path) -> tuple[Path, Path, Path, Path, bytes]:
    evidence_dir.mkdir(parents=True, exist_ok=True)
    original = ("\n".join(CHAT) + "\n").encode("utf-8")
    tampered = original.replace(b"#987654321", b"#987654329")
    e1 = evidence_dir / "E1_chat_log.txt"
    e1_tampered = evidence_dir / "E1_chat_log_TAMPERED.txt"
    e2 = evidence_dir / "E2_bank_sms.txt"
    e3 = evidence_dir / "E3_fake_profile.png"
    e1.write_bytes(original)
    e1_tampered.write_bytes(tampered)
    e2.write_bytes(("\n".join(SMS) + "\n").encode("utf-8"))

    try:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.axis("off")
        ax.text(0.5, 0.5, "FAKE PROFILE: 'Rohan K.'\n(cloned display photo)",
                ha="center", va="center", fontsize=11, weight="bold")
        fig.savefig(e3, dpi=100, bbox_inches="tight", format="png")
        plt.close(fig)
    except ImportError as exc:
        raise RuntimeError("matplotlib is required to generate the synthetic PNG demo evidence") from exc
    return e1, e1_tampered, e2, e3, original


def simulate_attack(vault_path: Path, level: int, tampered_hash: str) -> EvidenceVault:
    """Create an isolated malicious vault copy for L1/L2/L3 audit demonstrations."""
    if level not in (1, 2, 3):
        raise ValueError("Attack level must be 1, 2, or 3")
    attack_path = vault_path.parent / f"vault_attack_L{level}.json"
    data = json.loads(vault_path.read_text(encoding="utf-8"))

    data["records"][0]["sha256_digest"] = tampered_hash
    if level >= 2:
        data["custody_log"][0]["sha256"] = tampered_hash
    if level == 3:
        previous = GENESIS
        for entry in data["custody_log"]:
            entry["prev_hash"] = previous
            entry["entry_hash"] = entry_digest(entry)
            previous = entry["entry_hash"]

    attack_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return EvidenceVault(attack_path)


def run_avalanche(original: bytes, trials: int = 1000, seed: int = 42) -> tuple[float, float, list[int]]:
    baseline = hashlib.sha256(original).hexdigest()
    rng = random.Random(seed)
    values: list[int] = []
    for _ in range(trials):
        mutated = bytearray(original)
        bit_position = rng.randrange(len(mutated) * 8)
        mutated[bit_position // 8] ^= 1 << (bit_position % 8)
        values.append(count_bits_changed(baseline, hashlib.sha256(mutated).hexdigest()))
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return mean, variance ** 0.5, values


def run_demo(base: Path) -> dict[str, object]:
    base.mkdir(parents=True, exist_ok=True)
    evidence_dir = base / "evidence"
    vault_path = base / "evidence_vault.json"
    if vault_path.exists():
        vault_path.unlink()

    e1, e1_tampered, e2, e3, original = create_synthetic_evidence(evidence_dir)

    assert hashlib.sha256(b"abc").hexdigest() == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert hashlib.sha256(b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq").hexdigest() == "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"

    reference = sha256_file(e1)
    for size in (1, 7, 64, CHUNK_SIZE):
        assert sha256_file(e1, size) == reference

    vault = EvidenceVault(vault_path, handler="Investigator-01 (Group G<no>)")
    records = [
        vault.ingest(e1, "CASE-2026-001", "Synthetic WhatsApp chat export"),
        vault.ingest(e2, "CASE-2026-001", "Synthetic bank debit SMS"),
        vault.ingest(e3, "CASE-2026-001", "Synthetic cloned-profile screenshot"),
    ]
    anchor = (len(vault.log), vault.log[-1]["entry_hash"])

    assert verify_integrity(vault, e1, records[0]["evidence_id"])
    assert not verify_integrity(vault, e1_tampered, records[0]["evidence_id"])
    assert not verify_chain(vault, anchor)

    findings = {
        level: verify_chain(simulate_attack(vault_path, level, sha256_file(e1_tampered)), anchor)
        for level in (1, 2, 3)
    }
    assert all(findings.values())

    mean, std, avalanche_values = run_avalanche(original)
    assert 120 <= mean <= 136, f"Unexpected avalanche mean: {mean}"

    return {
        "vault": vault,
        "anchor": anchor,
        "records": records,
        "attack_findings": findings,
        "avalanche_mean": mean,
        "avalanche_std": std,
        "avalanche_values": avalanche_values,
        "evidence": (e1, e1_tampered, e2, e3),
    }


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="cybertwin-demo-") as temp_dir:
        result = run_demo(Path(temp_dir))
        print("CyberTwin synthetic forensic demo: PASS")
        print(f"Avalanche mean: {result['avalanche_mean']:.2f} bits")
        for level, findings in result["attack_findings"].items():
            print(f"Attack L{level}: DETECTED ({findings[0]})")
