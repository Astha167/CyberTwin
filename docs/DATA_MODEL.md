# Logical data model and ownership rules

## Relationships

```text
User 1 ──< Incident 1 ──< TimelineEvent
                    ├──< ChecklistProgress >── GuidanceTemplate
                    ├──< EvidenceRecord
                    └──< GeneratedReport

LegalGuidanceEntry ── selected by incident category ── Incident
```

## Planned records

| Record | Required fields | Ownership / validation |
|---|---|---|
| User | id, email (unique), password hash, created/updated timestamps | No plaintext credential fields. |
| Incident | stable ID, owner FK, category, affected-account descriptor, description, incident date, status, timestamps | `owner` is mandatory; controlled categories/statuses. |
| GuidanceTemplate | category/platform mapping, ordered items, version, review date | Curated application content, not user editable in MVP. |
| ChecklistProgress | incident FK, guidance-item reference, complete flag, completed timestamp | Unique per incident/item; incident ownership required. |
| TimelineEvent | incident FK, occurred-at, description, timestamps | Chronological presentation; incident ownership required. |
| EvidenceRecord | incident FK, opaque storage key, display filename, MIME type, byte size, uploaded-at, SHA-256 | Storage key is never a public path; allow-list and size checks precede storage. |
| GeneratedReport | incident FK, template version, created-at, snapshot/export metadata | Incident ownership required. |
| LegalGuidanceEntry | category mapping, content, authoritative source URL, review date, disclaimer version | Curated, dated, informational content. |

## Data minimisation and retention

Only collect data necessary to describe an incident and prepare the selected output. Affected-account descriptions must never request credentials or secrets. Retention and deletion periods are an operational deployment decision and must be documented before accepting real data. The local development database and evidence directory use fictional data only.

