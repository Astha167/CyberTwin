# Stack and architecture decision

**Status:** Approved baseline for Phase 1, subject to team sign-off recorded in `PROJECT_PLAN.md`.

## Decision

CyberTwin will be a Django 5.2 LTS monolith using server-rendered templates and Python 3.12. SQLite is the local-development database; PostgreSQL is the production target. Django authentication and server-side sessions provide the authentication basis. Evidence lives in an application-controlled directory outside any public web root. A server-side service computes SHA-256 after an upload passes validation. Complaint drafts render to a printable HTML page; browser print-to-PDF is the single reliable MVP export path.

## Why this fits

| Decision area | Selected option | Rationale |
|---|---|---|
| User interface | Django templates, progressively enhanced HTML | Fast to build, accessible without a separate frontend API, and easy to demonstrate. |
| Application/server | One Django application | One authorization boundary and less operational complexity than microservices. |
| Persistence | SQLite locally; PostgreSQL in production | Zero-setup local development with a relational production path. |
| Authentication/session | Django auth, password hashers, sessions, CSRF, logout | Mature built-in controls; no custom password or token implementation. |
| Evidence storage | Private filesystem path configured by environment | Keeps uploaded files out of public static/media paths. |
| Export | Printable HTML → PDF | A maintainable, readable single export path with no external integration. |
| Testing | Django `TestCase`/test client; later browser smoke tests | Direct coverage for authentication, ownership, validation, and integrity workflows. |
| Development/deployment | Python virtual environment; environment variables; WSGI/ASGI host | Reproducible local setup and simple deployment choices. |

## Architecture

```text
Browser (Django templates/forms)
          |
          v
Django views/services: authentication, validation, ownership authorization
          |                         |                         \
          v                         v                          v
Relational database          Guidance/templates          Private evidence directory
                                                           (hash calculated here)
```

Authorization is checked in every incident-scoped view/service before reading or changing an incident, timeline event, checklist item, evidence record, or report. Child records are resolved through their incident rather than trusted from a raw object identifier.

## Fixed Phase-0 constraints

- No external platform, government, email, or social-media integration.
- No microservices, mobile app, browser extension, OCR, AI guidance, or forensic-analysis service.
- One standard user role; access is based on ownership.
- SHA-256 is an integrity comparison only. It does not prove admissibility or chain of custody.
- Legal content is informational, sourced, dated, and never legal advice.

## Open operational decisions before deployment

Production host, PostgreSQL provider, backup schedule, retention period, and named owners are intentionally not invented. They require team approval before real user data is accepted.

