# Notes CLI implementation plan

## Full-spec coverage

- `REQ-001`: implement JSONL append in `notes.py` and test the stored record.
- `REQ-002`: implement ordered listing in `notes.py` and test insertion order.
- `REQ-003`: validate blank input before writes and prove the file is unchanged.
- `REQ-004`: migrate `notes.json`, create a rollback copy, preserve every note, and test recovery.
- `REQ-005`: cover add, list, blank rejection, migration, rollback preservation, and malformed legacy data in `test_notes.py`.

## Dependency order and tranches

1. Establish storage and validation helpers in `notes.py`, then run focused unit tests.
2. Add the CLI commands and end-to-end tests.
3. Add migration and rollback behavior after the JSONL contract is stable.

Each tranche is an execution view. Full completion requires every requirement above and the complete focused suite.
