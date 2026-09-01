# CyberTwin — Phase 0: Project Planning and Setup

**Project:** CyberTwin — Digital Identity Theft Recovery Assistant  
**Phase purpose:** Make the project buildable before implementation starts.  
**Status:** Planning document — no application feature is implemented by this phase.

---

## 1. Phase objective

Phase 0 establishes the agreed MVP scope, delivery plan, data/security boundaries, and technology decisions that the team needs before writing application code. Its output is a set of approved decisions and checklists, not a working application.

At the end of this phase, the team must know:

- exactly what CyberTwin will and will not do;
- which features are required for the MVP;
- the chosen technology stack and why it fits the project;
- how users, incidents, timelines, evidence, guidance, and reports will relate;
- how sensitive data and uploaded files will be protected;
- the order in which work will be implemented and tested.

---

## 2. Scope confirmation

### 2.1 Product definition

CyberTwin is a user-owned incident workspace for people affected by suspected digital identity theft. It helps a user document an incident, receive curated recovery/safety guidance, create a timeline, preserve selected evidence with SHA-256 integrity checking, prepare a complaint **draft**, and view informational legal/cybercrime resources.

It is not an automated recovery service, professional forensic tool, legal-advice platform, government complaint portal, or investigator case-management system.

### 2.2 Core MVP scope

The following features must be planned for the MVP:

1. User registration, login, logout, and case ownership.
2. Incident creation, viewing, updating, and basic personal dashboard.
3. Recovery guidance and account-security checklist based on incident context.
4. Incident timeline creation and chronological display.
5. Validated evidence upload, metadata capture, SHA-256 generation, and later match/mismatch verification.
6. User-reviewed cybercrime complaint-draft generation and one reliable export path.
7. Informational legal/cybercrime guidance with authoritative sources, review date, and disclaimer.
8. Consolidated dashboard/report access.

### 2.3 Explicit exclusions and safety boundaries

The following are not part of the current implementation:

- Automatic account recovery.
- Automatic complaint submission.
- Direct integration with NCRP, social-media platforms, email providers, or other external recovery/reporting APIs.
- AI-based classification or recommendations.
- Mobile app and browser extension.
- OCR, advanced evidence analysis, professional forensics, or chain-of-custody management.
- Investigator/admin roles and multi-user case workflows.
- Legal advice or definitive claims that a law applies to a user's case.

The application must never collect, store, or ask users to share:

- passwords;
- OTPs;
- recovery codes;
- answers to security questions.

### 2.4 Scope approval checklist

- [ ] The team accepts the Core MVP list.
- [ ] Optional features are separated from required work.
- [ ] Future-scope features are excluded from the current delivery schedule.
- [ ] Product wording uses “recovery guidance,” not “automated recovery.”
- [ ] Complaint output is defined as a user-reviewed draft.
- [ ] Legal content is defined as informational guidance only.

---

## 3. Finalized feature list and acceptance boundaries

| ID | Planned feature | MVP boundary | Acceptance evidence later required |
|---|---|---|---|
| F-01 | Authentication and ownership | One standard user role; no advanced role model needed. | Registration/login/logout and cross-user access-denial tests. |
| F-02 | Incident case management | Create, view, update, status, stable incident ID. | Incident form, saved record, authorization test. |
| F-03 | Recovery guidance/checklist | Small curated set of incident/platform categories. | Correct guidance display and checklist-persistence test. |
| F-04 | Timeline | Dated events and chronological display. | Out-of-order input shown in correct order. |
| F-05 | Evidence and SHA-256 | Limited safe file types/sizes; integrity check only. | Upload result, stored hash, `MATCH` and `MISMATCH` tests. |
| F-06 | Complaint draft/export | One readable draft template and one export path. | Reviewed draft and successful export. |
| F-07 | Legal/cybercrime information | Small verified mapping, sources, review date, disclaimer. | Correct guidance, visible sources/disclaimer. |
| F-08 | Dashboard/report access | User's own incident summary and report links. | Personal dashboard and export authorization test. |

### Optional features — only after F-01 to F-08 pass

- Search, filtering, and richer dashboard summaries.
- More platform-specific recovery templates.
- Safe preview for a limited set of uploaded evidence types.
- Additional export formats or styling improvements.
- Checklist reminders/progress indicators.
- Basic user-visible case-change history.

---

## 4. Technology stack selection

### 4.1 Decision principle

Do not choose technologies because they are fashionable or because they add complexity. Select one coherent stack that the team can develop, test, explain, and demonstrate within the project timeline.

The chosen stack must support:

- authenticated web access or another agreed user interface;
- persistent user-owned records;
- secure password handling and session/authentication support;
- server-side validation and authorization;
- protected file storage and SHA-256 calculation;
- generation of one readable report export;
- testing and local demonstration/deployment.

### 4.2 Stack-selection worksheet

Complete this before Phase 1.

| Decision area | Selected option | Reason for choice | Owner | Approved? |
|---|---|---|---|---|
| User interface approach | `[TO BE SELECTED]` | `[TO BE COMPLETED]` | `[TO BE ASSIGNED]` | `[ ]` |
| Application/server approach | `[TO BE SELECTED]` | `[TO BE COMPLETED]` | `[TO BE ASSIGNED]` | `[ ]` |
| Database/persistence approach | `[TO BE SELECTED]` | `[TO BE COMPLETED]` | `[TO BE ASSIGNED]` | `[ ]` |
| Authentication/session approach | `[TO BE SELECTED]` | `[TO BE COMPLETED]` | `[TO BE ASSIGNED]` | `[ ]` |
| Evidence storage approach | `[TO BE SELECTED]` | `[TO BE COMPLETED]` | `[TO BE ASSIGNED]` | `[ ]` |
| Export/report approach | `[TO BE SELECTED]` | `[TO BE COMPLETED]` | `[TO BE ASSIGNED]` | `[ ]` |
| Testing approach | `[TO BE SELECTED]` | `[TO BE COMPLETED]` | `[TO BE ASSIGNED]` | `[ ]` |
| Development/deployment environment | `[TO BE SELECTED]` | `[TO BE COMPLETED]` | `[TO BE ASSIGNED]` | `[ ]` |

### 4.3 Selection criteria

Evaluate each candidate stack against these practical criteria:

1. Team familiarity and ability to explain it in a viva.
2. Time required to reach a secure MVP.
3. Support for secure authentication and authorization.
4. Support for database relationships and validation.
5. Ability to protect uploaded files from public access.
6. Ability to calculate SHA-256 server-side or within another controlled application component.
7. Ability to produce one reliable export format.
8. Ease of automated/manual testing and local demonstration.
9. Deployment cost and operational simplicity.
10. Availability of maintained, documented security support.

### 4.4 Stack decision gate

Do not start Phase 1 until the team has selected and documented a stack for every decision area in Section 4.2.

---

## 5. Development environment and repository setup

### 5.1 Tasks

- Create or confirm the project repository.
- Add a concise project README with project purpose, setup prerequisites, and team contacts/roles.
- Configure a shared, reproducible development environment based on the selected stack.
- Establish version-control conventions: branches, commits, reviews, and issue tracking.
- Define how environment-specific configuration and secrets will be handled without committing them.
- Define a safe local/test evidence directory that is not publicly served.
- Establish a test-data policy using fictional incidents and harmless sample files only.

### 5.2 Suggested logical repository areas

The exact folder names depend on the selected stack, but the repository should clearly separate:

- application/interface code;
- application/server logic;
- database schema/migrations or persistence definitions;
- tests and test fixtures;
- documentation;
- scripts/configuration templates where needed;
- non-public test evidence fixtures;
- generated output that should not be committed.

### 5.3 Repository rules

- Do not commit passwords, API keys, session secrets, production data, or private evidence.
- Use a configuration template/example to document required settings without exposing values.
- Keep generated dependencies, local caches, logs, and temporary uploaded files out of version control unless there is a deliberate, documented reason.
- Keep one source of truth for requirements and implementation status.

### 5.4 Setup completion checklist

- [ ] Repository is available to all team members.
- [ ] README states the project purpose and local setup prerequisites.
- [ ] Technology-specific setup steps are recorded after stack selection.
- [ ] Ignore rules protect secrets, generated files, logs, and local evidence uploads.
- [ ] Team development conventions are agreed.
- [ ] Test data uses no real credentials or victim data.

---

## 6. Basic architecture decision

### 6.1 Required architectural responsibilities

The selected architecture must separate these responsibilities, even if they are deployed together:

```text
User interface
    ↕
Application logic and authorization boundary
    ↕                 ↘
Persistent application data   Protected evidence-file storage
```

- **User interface:** collects user input, displays cases/guidance/results, and shows clear errors/disclaimers.
- **Application logic and authorization boundary:** validates input, authenticates users, authorizes case ownership, selects guidance, generates hashes/reports, and coordinates data access.
- **Persistent data:** stores users, incidents, guidance mappings, checklist state, timeline events, evidence metadata, legal references, and report metadata.
- **Protected evidence storage:** holds uploaded evidence outside public access, referenced by metadata rather than exposed direct paths.

### 6.2 Required design decisions

Record answers before implementation:

| Architecture question | Decision required |
|---|---|
| Where is authorization checked? | Every protected operation must check the authenticated user owns the incident or related record. |
| Where are files stored? | In a protected location not directly publicly accessible. |
| Where is SHA-256 calculated? | In a controlled component with access to the uploaded file, immediately after validated upload. |
| How are reports generated? | Through one selected, maintainable export path. |
| How is guidance maintained? | Predefined content/templates with review ownership and update dates. |
| What happens on error? | Show user-safe messages; retain only appropriate diagnostic information. |
| How are secrets supplied? | Through protected environment/configuration mechanisms, never source code. |

### 6.3 Architecture non-goals

- No microservices unless the team has a concrete educational or operational need.
- No external integrations in the MVP.
- No separate forensic-analysis service.
- No complex role-based workflow beyond user ownership.

---

## 7. Database and data planning

### 7.1 Planned entities

The final names/types depend on the selected technology, but the MVP needs the following logical records.

| Entity | Purpose | Essential fields/relationships |
|---|---|---|
| User | Identifies the account owner. | Unique ID, required identity/contact fields, password credential hash, timestamps. |
| Incident | Central user-owned case record. | Unique incident ID, owner ID, type/category, affected platform/account descriptor, description, dates, status, timestamps. |
| Guidance Template | Curated recovery/safety content. | Supported category/platform mapping, ordered steps, content version/review date. |
| Checklist Progress | Tracks user completion of guidance/checklist items. | Incident ID, item/template reference, completion state, timestamp. |
| Timeline Event | Records dated incident events. | Incident ID, event date/time, description, timestamps. |
| Evidence Record | Describes a protected uploaded file. | Incident ID, safe storage reference, display filename as appropriate, type, size, upload time, SHA-256 hash. |
| Generated Report | Tracks or retains a generated complaint draft/export if needed. | Incident ID, template version, generation time, export metadata/snapshot as needed. |
| Legal Guidance Entry | Maintains informational legal/cybercrime material. | Incident category mapping, content, source/reference, review/update date, disclaimer reference. |

### 7.2 Essential relationships

```text
User 1 ──< Incident 1 ──< Timeline Event
                    ├──< Checklist Progress
                    ├──< Evidence Record
                    └──< Generated Report

Guidance Template ── used by ──< Checklist Progress
Legal Guidance Entry ── selected by ── Incident category
```

### 7.3 Data minimisation rules

- Collect only information needed to document the incident and generate the selected outputs.
- Do not request passwords, OTPs, recovery codes, security-question answers, or unrelated identity data.
- Make descriptive fields clear but avoid requiring sensitive details that the MVP does not need.
- Set and document a retention/deletion approach before using real data.
- Use fictional data for demonstrations, tests, screenshots, and reports.

### 7.4 Database planning acceptance checklist

- [ ] Every user-owned record can be traced to an incident and user.
- [ ] No entity requires storing prohibited credential data.
- [ ] Evidence metadata is separate from protected file storage.
- [ ] Required fields, controlled values, uniqueness rules, and timestamps are identified.
- [ ] Retention/deletion decisions are recorded.

---

## 8. Security and privacy planning

### 8.1 Security baseline

| Area | Planned control |
|---|---|
| Credentials | Store only securely hashed passwords; never store plaintext passwords. |
| Authentication | Require authenticated access to personal case functions. |
| Authorization | Check ownership for incidents, timelines, checklists, evidence, drafts, and exports. |
| Input handling | Validate form input and safely render user-generated content. |
| File uploads | Allow-list types, set size limits, use safe names/storage, reject executables, and protect file access. |
| Evidence integrity | Calculate/store SHA-256; present it only as a file-integrity check. |
| Sessions | Use a stack-appropriate secure session/authentication design with logout support. |
| Errors/logging | Do not expose secrets, stack traces, storage paths, or other sensitive details to users. |
| Configuration | Keep secrets outside version control and document required configuration safely. |
| Privacy | Minimise personal data, limit access, use fictional data for testing, and define retention. |

### 8.2 Legal/content safety baseline

- Legal/cybercrime content must be verified using authoritative sources before it appears in the application.
- Every guidance item should record its source and review/update date.
- Use “may be relevant depending on the circumstances,” not definitive legal conclusions.
- Show a clear disclaimer that CyberTwin provides informational guidance, not legal advice.
- State clearly that SHA-256 does not by itself establish legal admissibility or a complete forensic chain of custody.

### 8.3 Threat-and-control review

Before Phase 1, discuss these scenarios and document the selected control:

| Scenario | Required response |
|---|---|
| User attempts to access another person's incident URL/identifier. | Server/application authorization denies access. |
| User uploads an executable or oversized file. | Upload is rejected before protected storage. |
| User enters script-like text in a description. | Input is safely handled and never executed in output. |
| A secret is accidentally added to the repository. | Prevent exposure through repository rules; rotate/remove it using the selected process. |
| User mistakes guidance for legal advice. | Visible disclaimer, cautious wording, sources, and review date. |
| User assumes a file hash proves forensic admissibility. | Clear integrity-only explanation in UI and documentation. |

---

## 9. Development milestones and team tracking

### 9.1 Milestone plan

| Milestone | Phases | Outcome required before proceeding |
|---|---|---|
| M1: Foundation | 0–1 | Approved scope/stack plus secure authentication and ownership basis. |
| M2: Case workflow | 2–4 | Incidents, contextual guidance/checklist, and timeline work for the right user/case. |
| M3: Evidence and reporting | 5–8 | Protected evidence integrity, draft generation, legal information, dashboard, and export work. |
| M4: Quality | 9–11 | Security review, actual test results, refined integrated demo workflow. |
| M5: Evidence/documentation | 12 | Accurate documentation, screenshots, report mappings, and limitations. |

### 9.2 Suggested work ownership matrix

Assign named people after team formation; do not assume roles are already filled.

| Work area | Primary owner | Reviewer | Status |
|---|---|---|---|
| Scope and requirements | `[TO BE ASSIGNED]` | `[TO BE ASSIGNED]` | Not started |
| Stack/environment | `[TO BE ASSIGNED]` | `[TO BE ASSIGNED]` | Not started |
| Data model/security design | `[TO BE ASSIGNED]` | `[TO BE ASSIGNED]` | Not started |
| Authentication/case workflow | `[TO BE ASSIGNED]` | `[TO BE ASSIGNED]` | Not started |
| Evidence/report workflow | `[TO BE ASSIGNED]` | `[TO BE ASSIGNED]` | Not started |
| Test/documentation evidence | `[TO BE ASSIGNED]` | `[TO BE ASSIGNED]` | Not started |

### 9.3 Definition of a completed task

A development task is complete only when it has:

1. an agreed requirement/acceptance condition;
2. implementation reviewed according to team practice;
3. relevant validation or test evidence;
4. updated documentation where user-facing behaviour or data/security design changed;
5. no unresolved critical security or ownership issue.

---

## 10. Phase 0 deliverables checklist

Before moving to Phase 1, complete and approve all of the following:

- [ ] Core MVP, optional features, and future-scope exclusions are signed off.
- [ ] User roles are limited and confirmed; the MVP uses user ownership.
- [ ] Technology stack is selected and recorded with rationale.
- [ ] Development environment and repository conventions are documented.
- [ ] Basic architecture decision is documented.
- [ ] Logical data model and ownership relationships are documented.
- [ ] File-storage and SHA-256 workflow are planned.
- [ ] Security/privacy baseline and threat/control review are complete.
- [ ] Legal-content sourcing/review process is defined.
- [ ] Milestones and work owners are assigned.
- [ ] Test-data and evidence-capture rules are agreed.
- [ ] The team can begin authentication implementation without a material open decision.

---

## 11. Report evidence to retain during Phase 0

Phase 0 creates planning evidence for the final report; it does not create application-result screenshots.

| Future report area | Evidence prepared in this phase |
|---|---|
| Chapter 3 — Requirements | Scope, functional/non-functional requirements, constraints, assumptions, feasibility notes. |
| Chapter 4 — System Design | Architecture decision, user flow, use cases, planned ER model, planned data flows, security design, SHA-256 workflow. |
| Chapter 5 — Implementation | Selected stack rationale and planned implementation order; replace planning statements with actual details after build. |
| Chapter 6 — Testing | Acceptance criteria and initial test-plan structure. |
| Chapter 8 — Security, Privacy and Legal | Security baseline, data-minimisation rules, legal disclaimer/content-review policy. |
| Chapter 9 — Limitations and Future Scope | Explicit exclusions, implementation risks, and future-scope list. |

---

## 12. Phase 0 completion criteria

Phase 0 is complete when all conditions below are true:

1. The team has approved a small, demonstrable Core MVP.
2. No excluded advanced feature has been added to the current scope.
3. The technology stack, environment, repository conventions, and basic architecture are selected.
4. The logical data model identifies user ownership for every sensitive record.
5. Evidence upload/storage, SHA-256 integrity limits, report-draft boundaries, and legal-information boundaries are understood.
6. Security, privacy, secret handling, and test-data rules are documented.
7. The phase checklist in Section 10 is complete.
8. Phase 1 can begin with no unresolved decision that changes the project scope or security model.

---

## 13. Handoff to Phase 1

Provide the following to the person/team beginning Phase 1:

- approved feature list and exclusions;
- selected stack and environment setup instructions;
- user entity/credential requirements;
- authentication/session decision;
- authorization and ownership rules;
- secret/configuration policy;
- initial authentication acceptance tests;
- list of decisions that must not be changed without review.

**Next phase:** [Phase 1 — Authentication and User Management](IMPLEMENTATION_PLAN.md#phase-1--authentication-and-user-management)
