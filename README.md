# CyberTwin

CyberTwin is a user-owned workspace for documenting a suspected digital identity-theft incident. It will help a person organise an incident, follow curated recovery and account-security guidance, record a timeline, preserve selected evidence with SHA-256 integrity checking, and prepare a user-reviewed complaint draft.

It is not an automated recovery service, complaint-submission portal, or legal-advice service. Never enter passwords, OTPs, recovery codes, or security-question answers.

## Project status

**Phase 0 planning is complete, and the M3–M6 forensic integrity implementation is now implemented and tested.** The repository contains a reusable Python forensic engine, synthetic evidence demo, persistent Evidence Vault, hash-chained custody ledger, external checkpoint verification, adversarial tamper simulations, avalanche analysis, automated tests, and a Google Colab notebook matching the CA-2 implementation guide.

The broader Django application/authentication roadmap remains documented in the existing Phase 1 and project-planning files.

## Forensic implementation

- Streaming SHA-256 with a 64 KiB bounded buffer
- NIST known-answer validation and chunk-size invariance tests
- Synthetic TXT/SMS/PNG evidence generation
- Persistent EvidenceVault manifest
- SHA-256 hash-chained chain-of-custody ledger
- Constant-time integrity comparison
- External checkpoint verification
- L1/L2/L3 custody-ledger attack simulation
- 1,000-trial SHA-256 avalanche analysis
- Streaming-vs-read-all memory profiling
- Persistence/rehydration verification

### Run the forensic engine locally

Python 3.10+ is sufficient for the core engine.

    python -m pip install -r requirements-forensics.txt
    python -m unittest discover -s tests -v
    python -m cybertwin_forensics.demo

The Google Colab implementation is available at notebooks/CyberTwin_G<no>.ipynb, with the full source guide at docs/CYBERTWIN_COLAB_IMPLEMENTATION.md.

## Repository structure

    cybertwin_forensics/     Reusable forensic integrity engine
    tests/                   Automated forensic-engine tests
    notebooks/               Google Colab implementation
    docs/                    Architecture, planning and implementation guides
    var/                     Local evidence/report placeholders (ignored data)

## Chosen application stack

- Django 5.2 LTS (Python 3.12) rendered web application
- SQLite for local development; PostgreSQL for production deployment
- Django's built-in authentication, server-side sessions, CSRF protection, and password hashers
- Private filesystem evidence storage outside the web-served static/media roots
- Server-side SHA-256 via Python's standard library
- HTML complaint-draft view with print-to-PDF as the single MVP export path

The rationale and constraints are in docs/STACK_DECISION.md.

## Safety and test data

Use fictional incidents and harmless fixtures only. Local uploads belong under var/evidence/ and are ignored by Git. Do not place private evidence, personal data, secrets, credentials, executables, or generated reports in this repository.

## Team roles and contribution

See docs/PROJECT_PLAN.md and CONTRIBUTING.md. Existing planning and security documentation has been retained.
