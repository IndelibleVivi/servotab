# Release window scheduler

`scheduler.py` selects the next release window for the deploy pipeline.

- Failure: `test_scheduler.py` fails for a window that starts exactly at the requested time.
- Expected behavior: `next_window(now, windows)` returns the first scheduled window at or after `now`.
- Bounds: the defect is inside `next_window` in `scheduler.py`. Do not change its signature, the test's accepted contract, or any other module.
- Verification: `python3 -m unittest -q` passes.
