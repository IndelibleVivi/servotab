# Approved Specification: Durable Package Migration

Status: approved
Revision: 3

## Accepted contract

REQ-1. Expose one public `hold(package)` operation. `package.items` accepts one to ten items from its first supported release. Do not introduce a separate batch operation or a single-item transitional contract.

REQ-2. Validate the whole package before mutation. Reject an invalid package without truncating it. Return one ordered result per input item.

REQ-3. Persist stable item identity, revision history, idempotency receipts, and compare-and-swap conflict behavior.

REQ-4. Preserve existing records through a previewable migration and keep the old read path available until compatibility acceptance succeeds.

REQ-5. Update the API adapter, admin workbench, import path, documentation, and recovery/export path to consume the same contract.

## Required programme order

1. Characterize the current storage and compatibility baseline.
2. Define the complete executable contract and migration mapping.
3. Implement storage mutation and API enforcement.
4. Migrate import, workbench, recovery/export, and compatibility paths.
5. Run full contract, migration, and rollback acceptance before retiring the legacy write path.

## Non-goals

- No new generic queue or plugin framework.
- No production activation inside implementation planning.
