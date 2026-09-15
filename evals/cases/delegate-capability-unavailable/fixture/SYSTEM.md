# Collector reconciliation contract

`reconciler.py` computes the entries the collector still has to deliver.

- Failure: `test_reconciler.py` fails when every accepted entry was already delivered; the job retries an entry that is not missing.
- Expected behavior: `reconcile(accepted, delivered)` returns exactly the accepted entries that are not in `delivered`, preserving accepted order.
- Entry evidence: the focused test, the current source, and the sanitized collector excerpt at `evidence/collector.log`.
- Bounds: the defect is inside `reconciler.py`. Do not change its signature, the test's accepted contract, or any other module.
- Verification: `python3 -m unittest -q` passes.
