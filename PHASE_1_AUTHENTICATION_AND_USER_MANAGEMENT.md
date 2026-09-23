# CyberTwin — Phase 1: Authentication and User Management

**Project:** CyberTwin — Digital Identity Theft Recovery Assistant  
**Phase purpose:** Implement secure user registration, login, logout, and the ownership foundation that all later phases depend on.  
**Status:** Implementation phase — Phase 0 planning decisions must be approved before this phase begins.

---

## 1. Phase objective

Phase 1 establishes the authentication layer and user ownership mechanism that protects every personal record in CyberTwin. No core feature can be securely delivered without this foundation.

At the end of this phase, the team must have:

- a working registration flow that stores only hashed credentials;
- a working login and logout flow that correctly establishes and destroys authenticated state;
- a reusable, server-side ownership check that later phases will apply to incidents, evidence, timelines, and reports;
- documented security decisions that match the Phase 0 baseline;
- recorded test results for every acceptance test listed in this phase.

**This phase produces no useful visible feature for end users beyond login/logout. That is expected and correct.** The goal is a secure, reusable foundation — not a product demonstration.

---

## 2. Dependencies and prerequisites

Phase 1 cannot begin until Phase 0 is fully complete. The following Phase 0 outputs must be approved and available before any implementation work starts:

| Prerequisite | Required item |
|---|---|
| Scope approval | Core MVP and exclusions signed off (Phase 0, Section 10). |
| Stack decision | Every row in the stack-selection worksheet completed and approved (Phase 0, Section 4.2). |
| Architecture decision | Authorization boundary, session design, and secret-handling policy agreed (Phase 0, Sections 6.1–6.2). |
| Data model | User entity fields, credential storage requirements, and ownership relationships agreed (Phase 0, Section 7.1). |
| Repository setup | Repository is available to all team members and setup instructions are documented (Phase 0, Section 5). |
| Security baseline | Password-hashing approach, session policy, and secret/config rules confirmed (Phase 0, Section 8.1). |

Do not proceed if any item above is unresolved. Record the date and person who confirmed each prerequisite is complete.

---

## 3. Features and tasks

### 3.1 User registration

- Present a registration form collecting the minimum required identity and credential fields agreed in Phase 0.
- Validate all fields on the server/application boundary before processing.
- Hash the submitted password using the password-hashing mechanism selected in Phase 0. Never store or log a plaintext password at any point.
- Generate a unique user identifier and create the user record with required timestamps.
- Redirect the user to an appropriate next step after successful registration.
- Display clear, safe validation error messages for every invalid input without revealing whether an email address or username already exists (unless the team has a specific, documented reason for doing so).

### 3.2 User login

- Present a login form collecting the credential fields required by the selected stack.
- Validate inputs server-side before attempting credential verification.
- Compare the submitted credential against the stored hash using the selected hashing mechanism.
- On success: establish an authenticated session using the stack-approved session/token approach.
- On failure: return a uniform, non-specific error message that does not confirm whether a particular account exists.
- Apply rate-limiting or equivalent protection if available in the selected stack.

### 3.3 User logout

- Invalidate the authenticated session on logout.
- Redirect the user to an unauthenticated landing page after logout.
- Verify that accessing any protected route after logout returns an unauthenticated response, not previously loaded private content.

### 3.4 Authentication state and protected routing

- All routes that access personal case data must require an authenticated user.
- Unauthenticated requests to protected routes must be redirected or rejected, not served.
- The authenticated user identity must be available to every protected operation so that authorization checks in later phases can use it.

### 3.5 Ownership enforcement mechanism

- Implement a reusable server-side check that confirms the currently authenticated user matches the owner of the requested record.
- This mechanism will be used by every later phase. It must be designed to be applied consistently, not duplicated ad hoc.
- Document where the check lives in the codebase so later implementers know where to apply it.

### 3.6 Input validation and error handling

- Validate all required fields, minimum/maximum lengths, and acceptable formats.
- Reject malformed or unexpected input before it reaches persistence or credential logic.
- Return user-safe error messages. Do not expose stack traces, query details, internal field names, or database errors to the user interface.
- Log only the information needed for diagnosis; do not log raw passwords, session tokens, or sensitive personal details.

---

## 4. Deliverables

The following must exist and be verified by the end of Phase 1:

| Deliverable | Description |
|---|---|
| Registration flow | Working form, server-side validation, hashed storage, and redirect. |
| Login flow | Working form, credential verification, session creation, and redirect. |
| Logout flow | Session invalidation and redirect to unauthenticated state. |
| Protected route enforcement | All routes that will serve personal data return 401/403 or redirect for unauthenticated requests. |
| Ownership check mechanism | Reusable, server-side record-ownership check, documented in codebase. |
| Test results | Recorded actual outcomes for every test case in Section 7. |
| Report evidence | Screenshots, security notes, and test records for Chapters 4–8 (listed in Section 9). |

---

## 5. Database changes

### 5.1 User entity

Create the user identity and credential data structure using the technology selected in Phase 0. The structure must include:

| Field | Requirement |
|---|---|
| Unique user identifier | System-generated, stable, not reused. |
| Identity/contact field(s) | As agreed in Phase 0 (e.g., email or username). Required, validated format. |
| Password credential | Stored as a hash produced by the approved hashing mechanism. Plaintext must never be stored. |
| Account status | Active or equivalent; supports future deactivation without data loss if needed. |
| Created timestamp | Set at registration. Not user-modifiable. |
| Updated timestamp | Updated on any profile change. |

### 5.2 Constraints and rules

- The identity/contact field must be unique across all users.
- Password fields must not appear in any API response, log, or rendered view.
- The user identifier must be the foreign key used by all later entities (incidents, evidence, etc.).

### 5.3 Migration / schema creation

- Create the schema/migration file in the agreed location from the Phase 0 repository structure.
- Include all constraints in the schema definition, not only in application code.
- Record the migration version/timestamp so later phases can build on it.

---

## 6. Security requirements

These requirements are mandatory. No Phase 1 deliverable may be accepted if any item below is not implemented.

### 6.1 Credential security

| Requirement | Detail |
|---|---|
| Password hashing | Use the stack-approved password-hashing mechanism (e.g., bcrypt, Argon2, or equivalent). Never use general-purpose hash functions (MD5, SHA-1, SHA-256) for password storage. |
| No plaintext storage | Passwords must not appear in the database, logs, error messages, API responses, or configuration files at any time. |
| No plaintext transmission logging | Do not log submitted passwords even temporarily during debugging. |

### 6.2 Session and authentication security

| Requirement | Detail |
|---|---|
| Secure session design | Use the session/token approach approved in Phase 0 (e.g., signed server-side sessions, short-lived tokens, or stack-provided authentication). |
| Session invalidation on logout | Logout must invalidate the current session so replayed session tokens cannot restore access. |
| Secrets out of source control | Session secrets, signing keys, and any credential used by the authentication system must be supplied via environment configuration, not committed to the repository. |

### 6.3 Input and output safety

| Requirement | Detail |
|---|---|
| Server-side validation | All validation must occur server-side regardless of any client-side checks. |
| Safe error messages | Errors must not reveal existence of accounts, internal field names, database structure, or stack traces. |
| No unsafe output rendering | If any user-provided field is displayed back (e.g., a display name), it must be safely rendered to prevent script execution. |

### 6.4 Access control

| Requirement | Detail |
|---|---|
| All protected routes enforced | Every route that serves or mutates user-owned data must check authentication before processing. |
| Ownership check reusable | The mechanism that confirms record ownership must be centralised, not scattered across routes. |
| No privilege escalation | A standard registered user must not be able to access admin functions or another user's data through any URL manipulation or parameter change. |

---

## 7. Test cases

Record actual outcomes during testing. Do not pre-fill results or claim pass before executing the test.

### 7.1 Registration tests

| ID | Objective | Input | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| T1-R01 | Valid registration completes. | All required fields correctly filled. | User record created; password stored as hash; user redirected. | `[RECORD AFTER TEST]` | `[ ]` |
| T1-R02 | Missing required field rejected. | One required field left empty. | Validation error shown; no user record created. | `[RECORD AFTER TEST]` | `[ ]` |
| T1-R03 | Invalid email format rejected. | Malformed email address. | Validation error; no record created. | `[RECORD AFTER TEST]` | `[ ]` |
| T1-R04 | Duplicate identity field rejected. | Email/username already in use. | Safe error message; no second record created. | `[RECORD AFTER TEST]` | `[ ]` |
| T1-R05 | Password never stored in plaintext. | Valid registration submitted. | Database record contains only a hash; no plaintext in logs or response. | `[RECORD AFTER TEST]` | `[ ]` |
| T1-R06 | Short/weak password rejected (if policy applies). | Password below minimum length or policy. | Validation error; no record created. | `[RECORD AFTER TEST]` | `[ ]` |

### 7.2 Login tests

| ID | Objective | Input | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| T1-L01 | Valid login succeeds. | Correct email and password. | Session established; user redirected to authenticated area. | `[RECORD AFTER TEST]` | `[ ]` |
| T1-L02 | Wrong password rejected. | Correct email, incorrect password. | Uniform error message; no session created. | `[RECORD AFTER TEST]` | `[ ]` |
| T1-L03 | Non-existent account rejected. | Email not in system. | Same uniform error as T1-L02; no information disclosed. | `[RECORD AFTER TEST]` | `[ ]` |
| T1-L04 | Empty credentials rejected. | Both fields empty. | Validation error; no session created. | `[RECORD AFTER TEST]` | `[ ]` |
| T1-L05 | Protected route inaccessible without login. | Direct URL access without session. | Redirect or 401/403 response; no private content served. | `[RECORD AFTER TEST]` | `[ ]` |

### 7.3 Logout tests

| ID | Objective | Input | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| T1-O01 | Logout invalidates session. | Authenticated user clicks logout. | Session destroyed; user redirected to unauthenticated page. | `[RECORD AFTER TEST]` | `[ ]` |
| T1-O02 | Post-logout protected access denied. | Attempt to access a protected route after logout (e.g., browser back button or direct URL). | Redirect or 401/403; no private data served. | `[RECORD AFTER TEST]` | `[ ]` |

### 7.4 Authorization tests

| ID | Objective | Input | Expected result | Actual result | Status |
|---|---|---|---|---|---|
| T1-A01 | Cross-user access denied. | User A attempts to access a URL belonging to User B's future record. | 403/404 or redirect; User B's data not shown. *(Create a stub record if Phase 2 is not yet complete.)* | `[RECORD AFTER TEST]` | `[ ]` |
| T1-A02 | Ownership check is server-enforced. | Client-side manipulation of a user identifier parameter. | Server rejects or ignores the manipulation; ownership not bypassed. | `[RECORD AFTER TEST]` | `[ ]` |

---

## 8. Completion criteria

Phase 1 is complete when **all** conditions below are true:

- [ ] A user can register with valid data; the record is created with a hashed credential and correct timestamps.
- [ ] A registered user can log in with correct credentials and the session is established.
- [ ] Incorrect credentials produce a uniform error with no account-existence information.
- [ ] Logout destroys the session; subsequent protected-route access is denied.
- [ ] All protected routes reject unauthenticated requests before serving data.
- [ ] The reusable ownership check is implemented, documented, and confirmed to work with at least one test record.
- [ ] Passwords are stored only as hashes; no plaintext password appears in the database, logs, or responses.
- [ ] All session secrets and signing keys are supplied via environment configuration and are absent from the repository.
- [ ] All test cases in Section 7 have recorded actual results.
- [ ] No critical authentication, authorization, session, or credential-handling issue is open and unresolved.
- [ ] Phase 1 report evidence (Section 9) has been captured.

---

## 9. Report evidence to capture in Phase 1

Capture the following during or immediately after Phase 1. Replace planning notes with actual results as implementation proceeds.

| Future report area | Evidence required |
|---|---|
| Chapter 4 — System Design | Authentication flow diagram (registration → login → logout), use case for user authentication, session/token design note, password-hashing approach note. |
| Chapter 5 — Implementation | Stack-specific authentication implementation note, code location of ownership check, migration/schema summary, secret-handling approach. |
| Chapter 6 — Testing | Registration test results (T1-R01 to T1-R06), login test results (T1-L01 to T1-L05), logout test results (T1-O01 to T1-O02), authorization test results (T1-A01 to T1-A02). |
| Chapter 7 — Results | Registration form screenshot, login form screenshot, authenticated landing page screenshot, validation error screenshot, logout confirmation. |
| Chapter 8 — Security | Credential-hashing evidence (e.g., database record showing hash format), session-security design note, input-validation demonstration. |

> **Do not capture or include screenshots containing real credentials, real session tokens, or any personal data that belongs to a real person. Use only fictional test accounts.**

---

## 10. Phase 1 deliverables checklist

Before marking Phase 1 complete and moving to Phase 2:

- [ ] Registration, login, and logout are implemented and manually verified.
- [ ] All server-side validations are in place and tested.
- [ ] Passwords are stored as hashes using the approved mechanism.
- [ ] Sessions are established on login and invalidated on logout.
- [ ] All protected routes enforce authentication.
- [ ] Ownership check is implemented and reusable.
- [ ] Secrets are supplied via environment configuration.
- [ ] All Section 7 test cases have recorded actual results.
- [ ] No open critical security issue remains unresolved.
- [ ] All Section 9 report evidence has been captured with fictional test data only.

---

## 11. Handoff to Phase 2

Provide the following to the person/team beginning Phase 2 — Incident Registration and Case Management:

- Confirmed user entity structure and the user identifier field name used as the foreign key.
- Location of the reusable ownership check and instructions for applying it to new entities.
- Authentication state access pattern (how a protected route reads the current user's identity).
- Any restrictions on identity/profile fields that Phase 2 forms must respect.
- List of open non-critical issues deferred from Phase 1, with agreed handling.

**Previous phase:** [Phase 0 — Project Planning and Setup](PHASE_0_PROJECT_PLANNING_AND_SETUP.md)  
**Next phase:** Phase 2 — Incident Registration and Case Management
