# CyberTwin Forensic Engine — Architecture

## 1. Evidence integrity

sha256_file() reads evidence in fixed-size binary chunks (64 KiB by default), so memory use is bounded independently of file size. hmac.compare_digest() is used when comparing a presented digest to the stored baseline.

## 2. Evidence vault

EvidenceVault stores an evidence manifest and custody log in evidence_vault.json. Evidence records contain a generated evidence ID, case label, description, filename, size, UTC timestamp, hash algorithm, and SHA-256 digest.

Vault writes are atomic: the JSON is written to a temporary file, flushed and synced, then atomically replaced. This is an implementation-quality improvement over a direct overwrite because an interrupted write is less likely to leave a truncated vault.

## 3. Hash-chained custody ledger

Each event contains the previous event's hash. Its own entry_hash is SHA-256 over canonical JSON excluding entry_hash itself:

h_i = SHA-256(canonical(e_i without entry_hash))

The first entry points to the 64-zero genesis value. Verification checks both the previous-hash linkage and each entry's self-digest.

## 4. External checkpoint

The demo stores (sequence, entry_hash) outside the vault in memory. A production deployment should store this checkpoint in an independently controlled system. The checkpoint is specifically intended to make a complete ledger rewrite detectable.

## 5. Attack model

- L1 — Manifest tampering: change the stored evidence digest.
- L2 — Log-entry forgery: change the manifest and the original INGESTED log digest.
- L3 — Full ledger rewrite: change the manifest, edit the log, and recompute the entire chain.

The internal chain catches L1/L2; the external checkpoint catches the L3 rewrite.

## 6. Scope

This is an academic integrity demonstration, not a court-certified forensic evidence-management system. It does not establish authenticity, provenance, legal admissibility, or secure external storage by itself.
