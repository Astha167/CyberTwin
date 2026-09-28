"""Core forensic integrity and tamper-evident custody primitives for CyberTwin.

The implementation intentionally uses only Python's standard library. Matplotlib
is used by the demo layer for the avalanche-effect visualization.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CHUNK_SIZE = 64 * 1024
GENESIS = "0" * 64


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp with a trailing Z."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_file(path: str | os.PathLike[str], chunk_size: int = CHUNK_SIZE) -> str:
    """Return a file's SHA-256 digest using bounded streaming memory."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"Evidence file not found: {file_path}")

    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        for block in iter(lambda: handle.read(chunk_size), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_bytes(payload: dict[str, Any]) -> bytes:
    """Serialize a JSON object deterministically for cryptographic hashing."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def entry_digest(entry: dict[str, Any]) -> str:
    """Hash a custody entry after excluding its self-referential entry_hash."""
    payload = {key: value for key, value in entry.items() if key != "entry_hash"}
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def count_bits_changed(hex_digest_a: str, hex_digest_b: str) -> int:
    """Return the Hamming distance between two equal-length hexadecimal digests."""
    if len(hex_digest_a) != len(hex_digest_b):
        raise ValueError("Digest lengths must match")
    try:
        return (int(hex_digest_a, 16) ^ int(hex_digest_b, 16)).bit_count()
    except ValueError as exc:
        raise ValueError("Digests must contain only hexadecimal characters") from exc


class EvidenceVault:
    """Persistent evidence manifest plus an append-only hash-chained custody log."""

    def __init__(self, vault_path: str | os.PathLike[str], handler: str = "Investigator-01 (Group G<no>)") -> None:
        self.path = Path(vault_path)
        self.handler = handler
        self.records: list[dict[str, Any]] = []
        self.log: list[dict[str, Any]] = []
        if self.path.exists():
            self._load()

    def _load(self) -> None:
        with self.path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, dict):
            raise ValueError("Vault file must contain a JSON object")
        self.records = data.get("records", [])
        self.log = data.get("custody_log", [])
        if not isinstance(self.records, list) or not isinstance(self.log, list):
            raise ValueError("Vault records and custody_log must be JSON arrays")

    def _save(self) -> None:
        """Persist atomically to reduce the chance of a partially written vault."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"records": self.records, "custody_log": self.log}
        fd, temp_name = tempfile.mkstemp(prefix=self.path.name + ".", suffix=".tmp", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, ensure_ascii=False)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, self.path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)

    def log_event(self, evidence_id: str, action: str, digest: str, result: str) -> dict[str, Any]:
        """Append one cryptographically linked event to the custody ledger."""
        previous_hash = self.log[-1]["entry_hash"] if self.log else GENESIS
        entry: dict[str, Any] = {
            "seq": len(self.log) + 1,
            "timestamp_utc": utc_now(),
            "handler": self.handler,
            "evidence_id": evidence_id,
            "action": action,
            "sha256": digest,
            "result": result,
            "prev_hash": previous_hash,
        }
        entry["entry_hash"] = entry_digest(entry)
        self.log.append(entry)
        self._save()
        return entry

    def ingest(self, filepath: str | os.PathLike[str], case_label: str, description: str) -> dict[str, Any]:
        """Hash and register evidence, then record a baseline custody event."""
        path = Path(filepath)
        if not path.is_file():
            raise FileNotFoundError(f"Evidence file not found: {path}")

        digest = sha256_file(path)
        today = datetime.now(timezone.utc).strftime("%Y%m%d")
        evidence_id = f"EV-{today}-{len(self.records) + 1:04d}"
        record = {
            "evidence_id": evidence_id,
            "case_label": case_label,
            "description": description,
            "original_filename": path.name,
            "file_size_bytes": path.stat().st_size,
            "timestamp_recorded_utc": utc_now(),
            "hash_algorithm": "SHA-256 (FIPS 180-4)",
            "sha256_digest": digest,
        }
        self.records.append(record)
        self.log_event(evidence_id, "INGESTED", digest, "BASELINE")
        return record

    def get(self, evidence_id: str) -> dict[str, Any]:
        for record in self.records:
            if record.get("evidence_id") == evidence_id:
                return record
        raise KeyError(f"Evidence ID {evidence_id} not found in vault")


def verify_integrity(
    vault: EvidenceVault,
    filepath: str | os.PathLike[str],
    evidence_id: str,
) -> bool:
    """Compare presented evidence against the stored digest and log the audit event."""
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"Presented file not found: {path}")

    record = vault.get(evidence_id)
    stored_hash = record["sha256_digest"]
    current_hash = sha256_file(path)
    match = hmac.compare_digest(stored_hash, current_hash)
    result = "MATCH" if match else "MISMATCH"
    vault.log_event(evidence_id, "VERIFIED", current_hash, result)
    return match


def verify_chain(vault: EvidenceVault, anchor: tuple[int, str] | None = None) -> list[str]:
    """Return all detected custody-ledger anomalies."""
    issues: list[str] = []
    log = vault.log

    for index, entry in enumerate(log):
        expected_previous = GENESIS if index == 0 else log[index - 1]["entry_hash"]
        if entry.get("prev_hash") != expected_previous:
            issues.append(f"Seq {entry.get('seq')}: Broken link to previous entry")
        if entry_digest(entry) != entry.get("entry_hash"):
            issues.append(f"Seq {entry.get('seq')}: Log entry contents altered")

    for record in vault.records:
        evidence_id = record["evidence_id"]
        ingest_events = [
            entry for entry in log
            if entry.get("evidence_id") == evidence_id and entry.get("action") == "INGESTED"
        ]
        if not ingest_events:
            issues.append(f"{evidence_id}: No baseline INGESTED event recorded in custody log")
        elif record.get("sha256_digest") != ingest_events[0].get("sha256"):
            issues.append(f"{evidence_id}: Manifest digest differs from custody-log baseline")

    if anchor is not None:
        sequence, anchored_hash = anchor
        matching = [entry for entry in log if entry.get("seq") == sequence]
        if not matching:
            issues.append(f"Checkpoint seq {sequence} missing from custody log")
        elif matching[0].get("entry_hash") != anchored_hash:
            issues.append(f"Checkpoint seq {sequence} differs from externally anchored value")

    return issues
