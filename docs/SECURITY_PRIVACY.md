# Security, privacy, and content policy

## Baseline controls

| Risk area | Planned control |
|---|---|
| Credentials | Django password hashers; no plaintext password persistence. |
| Sessions | Django sessions, CSRF protection, secure cookie settings in production, logout. |
| Ownership | Every protected action verifies the authenticated owner of the incident. |
| Input | Server-side validation; template auto-escaping; no execution of user input. |
| Uploads | MIME/type allow-list, 10 MiB maximum, server-generated storage key, executable rejection, private storage. |
| Integrity | SHA-256 generated after validated upload; later comparison reports `MATCH` or `MISMATCH`. |
| Errors/logging | User-safe errors; no stack traces, secrets, hashes' private paths, or evidence paths exposed. |
| Configuration | Environment variables only; `.env` ignored; rotate any accidentally exposed secret. |

## Threat-to-control review

| Scenario | Required control and test evidence |
|---|---|
| A user changes an incident identifier in a URL | Return denial/not-found without disclosing the other record; automated cross-user test. |
| Executable or oversized upload | Reject before it reaches evidence storage; upload validation test. |
| Script-like incident description | Render as text through auto-escaped templates; XSS regression test. |
| Secret committed | Remove from repository history where necessary, rotate it, and document the incident; prevention via ignore rules and review. |
| Guidance mistaken for legal advice | Display disclaimer and cautious language with source and review date. |
| Hash mistaken for forensic proof | State in UI/docs that SHA-256 is integrity-only, not admissibility or chain-of-custody proof. |

## Legal and cybercrime content policy

Content is informational, not legal advice. Each published item needs an authoritative source URL, a review date, and an assigned reviewer before release. It must use cautious language such as “may be relevant depending on the circumstances.” Legal sources are not selected in Phase 0; they require jurisdiction confirmation and source verification before implementation.

