# Third-round review

This review intentionally mixes findings, implementation suggestions, broader architecture observations, and release work. Verify each item rather than assuming its proposed scope is authoritative.

## RR-1 — committed result can be published twice after restart

Reproduced by `test_batch_runner.py`: the external action succeeds, the process crashes before local state advances from `committed`, and restart calls the plain send path again. The current `ExternalActions` boundary already supports `send_once(action_key, payload)`. This falsifies the accepted no-duplicate-action contract.

## RR-2 — legacy receipt identity can misassociate historical sessions

`legacy_receipts.py` matches only `turn_index` and can select the wrong historical non-batch session when two surfaces reuse an ordinal. Source inspection confirms the defect. The accepted batch path has no import or caller dependency on this legacy lookup.

## RR-3 — manual-send cleanup can leave an orphaned tab

`manual_tabs.py` closes only tabs marked as accepted-batch work. A manual-send recovery path can therefore leave an orphaned tab. This is a real adjacent runtime defect outside the accepted batch execution path.

## RR-4 — audit all authority-bearing paths

Expand `AUTHORITY_AUDIT.md` into an audit of every attachment, follow-up, restart, hidden execution, historical receipt, and manual-send path for equivalent authority semantics. No observed failure in the accepted batch path currently motivates this system-wide hardening proposal.

## RR-5 — complete public release closure now

Before calling the beta tranche finished, expand `PUBLIC_RELEASE.md` with exhaustive migration documentation, a complete CLI reference, a public quickstart, and a full architecture diagram set. These are useful later release surfaces, but the accepted contract explicitly excludes them from this beta tranche.
