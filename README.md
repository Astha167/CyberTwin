# CyberTwin — Forensic Integrity Engine

A synthetic academic implementation of the CyberTwin M3–M6 forensic-integrity work.

## Included

- Streaming SHA-256 evidence hashing with bounded memory
- NIST SHA-256 known-answer validation
- Evidence Vault with persistent JSON storage
- SHA-256 hash-chained custody ledger
- Integrity verification with MATCH/MISMATCH audit events
- External checkpoint verification
- L1/L2/L3 tamper and ledger-rewrite simulation
- 1,000-trial SHA-256 avalanche analysis
- Streaming-memory scalability profiling
- Automated Python tests
- Google Colab notebook and implementation guide

## Safety

All demonstration evidence is synthetic and harmless. Do not upload authentic personal, financial, legal, investigative, or other sensitive evidence to Colab or commit it to Git.

## Run locally

Python 3.10+ is sufficient for the core engine.

    python -m pip install -r requirements-forensics.txt
    python -m unittest discover -s tests -v
    python -m cybertwin_forensics.demo

## Repository layout

    cybertwin_forensics/
        __init__.py
        core.py
        demo.py
    tests/
        test_forensics.py
    notebooks/
        CyberTwin_G<no>.ipynb
    docs/
        CYBERTWIN_COLAB_IMPLEMENTATION.md
        FORENSIC_ENGINE.md

The notebook is designed for a Standard CPU Google Colab runtime and uses synthetic evidence only.
