# Contributing to CyberTwin

## Workflow

1. Create a short-lived branch named `codex/<topic>` or `feature/<topic>`.
2. Keep one concern per pull request and write clear, imperative commit messages.
3. Add or update tests and documentation with behaviour, data, or security changes.
4. Request review before merging. The reviewer checks authorization, validation, and sensitive-data handling as relevant.
5. Link the work to the acceptance item in [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md).

## Non-negotiable repository rules

- Never commit secrets, `.env`, private evidence, production data, credentials, or generated reports.
- Never ask users for passwords, OTPs, recovery codes, or security-question answers.
- Treat every incident-related object as user-owned: protected operations must enforce ownership server-side.
- Use only fictional, harmless test data and fixtures.
- Do not add external recovery, reporting, platform, or AI integrations without a scope review.

## Definition of done

A change is done only when its acceptance condition is met, relevant tests pass, documentation is updated, and there is no unresolved critical authorization or security issue.

