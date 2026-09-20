# CyberTwin

CyberTwin is a user-owned workspace for documenting a suspected digital identity-theft incident. It will help a person organise an incident, follow curated recovery and account-security guidance, record a timeline, preserve selected evidence with SHA-256 integrity checking, and prepare a **user-reviewed complaint draft**.

It is not an automated recovery service, complaint-submission portal, forensic tool, investigation platform, or legal-advice service. Never enter passwords, OTPs, recovery codes, or security-question answers.

## Project status

Phase 0 implementation is complete: scope, the architecture, the data plan, security boundaries, and the development conventions are recorded in [`docs/`](docs/). Team sign-off and named owners remain pending in the project plan. No application feature is implemented in this phase.

## Chosen stack

- Django 5.2 LTS (Python 3.12) rendered web application
- SQLite for local development; PostgreSQL for production deployment
- Django's built-in authentication, server-side sessions, CSRF protection, and password hashers
- Private filesystem evidence storage outside the web-served static/media roots
- Server-side SHA-256 via Python's standard library
- HTML complaint-draft view with print-to-PDF as the single MVP export path
- Django test runner, with later browser-level smoke tests

The rationale and constraints are in [`docs/STACK_DECISION.md`](docs/STACK_DECISION.md).

## Prerequisites

- Git
- Python 3.12+
- A virtual-environment tool (`python -m venv`)

## Planned local setup (Phase 1 onward)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Fill in a unique local SECRET_KEY in .env; do not commit it.
python manage.py migrate
python manage.py runserver
```

The `src/` Django project is deliberately not created until Phase 1, when authentication is implemented. The environment-variable contract and target layout are already defined.

## Team roles

Owners and reviewers must be assigned before implementation. See [`docs/PROJECT_PLAN.md`](docs/PROJECT_PLAN.md#ownership-and-approvals). Until then, `Unassigned` is intentional—not approval.

## Safety and test data

Use fictional incidents and harmless fixtures only. Local uploads belong under `var/evidence/` and are ignored by Git. Do not place private evidence, personal data, secrets, credentials, executables, or generated reports in this repository.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). The project uses short-lived `codex/` or `feature/` branches, focused commits, and review before merging.
