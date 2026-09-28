# CyberTwin — Forensic Integrity Engine

This implementation covers the M3–M6 portion of CyberTwin's synthetic digital-identity-theft scenario: synthetic evidence generation, streaming SHA-256 integrity checking, a persistent evidence vault, a hash-chained chain-of-custody ledger, external checkpoint verification, adversarial tamper simulation, avalanche analysis, and memory profiling.

> Safety boundary: all demonstration evidence is synthetic and harmless. Do not upload authentic personal, legal, financial, or investigative evidence to Google Colab or commit it to Git.

## Repository layout

    cybertwin_forensics/
    ├── core.py
    ├── demo.py
    tests/
    └── test_forensics.py
    notebooks/
    └── CyberTwin_G<no>.ipynb
    docs/
    └── FORENSIC_ENGINE.md

## Run locally

Python 3.10+ is sufficient for the core engine. The demo visualization requires matplotlib.

    python -m unittest discover -s tests -v
    python -m cybertwin_forensics.demo

For Google Colab, open the notebook in notebooks/, use a Standard CPU runtime, and run all cells sequentially.

## What is verified

- NIST SHA-256 known-answer vectors.
- SHA-256 invariance across multiple streaming chunk sizes.
- Authentic evidence returns MATCH; a one-bit mutation returns MISMATCH.
- Custody events form a SHA-256-linked ledger.
- Manifest, ledger-entry, and full-chain rewrite attacks are detected.
- A saved external checkpoint detects a full-history rewrite.
- Vault state can be rehydrated from JSON without losing records or ledger entries.
- A 1,000-trial single-bit-flip experiment demonstrates the expected SHA-256 avalanche behavior.

## Important reproducibility note

Timestamps, PNG bytes, benchmark timings, and some generated PNG SHA-256 values are runtime-dependent. The implementation asserts stable cryptographic properties and test outcomes rather than hard-coding environment-specific timestamps or performance numbers.
