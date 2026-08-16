# Approved Notes CLI Specification

Status: APPROVED

- `REQ-001` — Add `python3 notes.py add <text>` and persist one JSON object per line in `notes.jsonl`.
- `REQ-002` — Add `python3 notes.py list` and preserve insertion order.
- `REQ-003` — Reject blank notes without modifying stored data.
- `REQ-004` — Migrate an existing `notes.json` array on first write, preserving every note and creating a rollback copy.
- `REQ-005` — Add automated coverage for add, list, blank-input rejection, migration, rollback preservation, and malformed legacy data.

The implementation may be delivered in ordered tranches, but no tranche replaces this complete accepted scope.
