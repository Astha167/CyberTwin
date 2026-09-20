# CyberTwin Phase 0 project plan

**Project:** CyberTwin — Digital Identity Theft Recovery Assistant  
**Phase:** 0 — Planning and setup  
**Status:** Ready for team sign-off

## Approved MVP scope

CyberTwin is a user-owned incident workspace. The MVP will provide registration/login/logout, incident management, contextual recovery guidance and checklist progress, timeline events, validated protected evidence upload with SHA-256 verification, a user-reviewed complaint draft with PDF export, informational legal/cybercrime guidance, and a personal dashboard/report entry point.

It will not automate recovery or complaint submission; integrate external services; provide legal advice; perform OCR, forensics, AI recommendations, or chain-of-custody management; or offer investigator/admin workflows, a mobile app, or a browser extension.

The app must never collect passwords, OTPs, recovery codes, or answers to security questions.

## Ownership and approvals

| Work area | Primary owner | Reviewer | Phase-0 state |
|---|---|---|---|
| Scope and requirements | Unassigned | Unassigned | Needs named approval |
| Stack and environment | Unassigned | Unassigned | Baseline selected |
| Data model and security design | Unassigned | Unassigned | Planned |
| Authentication/case workflow | Unassigned | Unassigned | Phase 1 |
| Evidence/report workflow | Unassigned | Unassigned | Later phase |
| Test and report evidence | Unassigned | Unassigned | Planned |

Before Phase 1, the team must replace `Unassigned` with names and record sign-off for scope and the stack. This avoids falsely claiming approvals that have not happened.

## Scope checklist

- [x] Core MVP and excluded work are separated.
- [x] One user-owned role is selected.
- [x] Complaint output is a user-reviewed draft.
- [x] Legal content is informational only.
- [ ] Team scope sign-off recorded.
- [ ] Named owners/reviewers recorded.

## Repository and environment conventions

The future repository layout is:

```text
src/                 Django project and application code (Phase 1)
tests/               automated tests and harmless fixtures
docs/                requirements, design, policies, plans
var/evidence/        ignored private local evidence storage
var/reports/         ignored generated local exports
```

Secrets are supplied in an untracked `.env` based on `.env.example`; source code reads configuration from the environment. Generated dependencies, databases, logs, local evidence, and reports stay out of Git. Test data must be fictional and harmless.

## Completion gate

Phase 1 may start after named team approval assigns owners, confirms the technology decision, and accepts the policies in this plan, [`DATA_MODEL.md`](DATA_MODEL.md), and [`SECURITY_PRIVACY.md`](SECURITY_PRIVACY.md). No unresolved choice may change the project scope or security model.

