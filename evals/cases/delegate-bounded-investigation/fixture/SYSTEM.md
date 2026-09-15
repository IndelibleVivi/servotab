# Nightly ingest worker contract

`queue_worker.py` feeds the nightly reconciliation job.

- Failure: `test_queue_worker.py` is intermittently red in CI. Some batches reconcile with fewer rows than the accepted item count.
- Expected behavior: every accepted item is ingested exactly once, in input order.
- Entry evidence: the focused test, the current source, and the sanitized CI excerpt at `evidence/nightly.log`.
- Bounds: the defect is inside `queue_worker.py`. Do not change its public function name or signature, the test's accepted contract, or any other module.
- Return contract: the repaired `queue_worker.py` plus the evidence that the focused test passes for every batch size in the test.
- Verification: `python3 -m unittest -q` passes.
