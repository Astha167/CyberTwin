# Implementation plan and acceptance map

## Milestones

| Milestone | Phases | Gate |
|---|---|---|
| M1 Foundation | 0–1 | Approved plan plus tested authentication/ownership basis. |
| M2 Case workflow | 2–4 | Incidents, guidance/checklist, and timeline work only for their owner. |
| M3 Evidence/reporting | 5–8 | Protected evidence, integrity check, draft/export, legal info, dashboard. |
| M4 Quality | 9–11 | Security review, test results, integrated demonstration. |
| M5 Documentation | 12 | Accurate documentation, screenshots, mappings, limitations. |

## Ordered phases

1. Authentication and user management: registration, login/logout, session protection, ownership test.
2. Incident case management: create/view/update user-owned cases and stable IDs.
3. Recovery guidance and persisted checklist progress.
4. Timeline entry and chronological display.
5. Validated private evidence upload and SHA-256 capture.
6. Hash re-verification with `MATCH` and `MISMATCH` tests.
7. Complaint-draft template and print-to-PDF export.
8. Sourced, dated informational legal/cybercrime content and dashboard access.
9. Security and privacy review.
10. Full automated/manual test pass.
11. Demo-flow refinement with fictional data.
12. Final report evidence and documentation.

## Core acceptance conditions

| ID | Acceptance evidence |
|---|---|
| F-01 | Registration, login/logout, and cross-user access-denial tests. |
| F-02 | Saved incident and authorization test. |
| F-03 | Correct curated guidance and persisted checklist state. |
| F-04 | Out-of-order input displays chronologically. |
| F-05 | Upload stores hash; verification proves both match and mismatch paths. |
| F-06 | User-reviewed readable draft and successful PDF export. |
| F-07 | Correct informational guidance with visible source, date, and disclaimer. |
| F-08 | Dashboard limits summaries and reports to the current user. |

