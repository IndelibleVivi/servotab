A review reports that the chart groups events under the wrong date around
midnight. Verify the finding, then repair the shared behavior in `days.py`.
All user-facing date views must use the supplied fixed offset in minutes,
including chart, detail, and share output. Preserve the accepted UTC-only audit
date contract, existing function signatures, and rejection of naive timestamps.
Change only `days.py`, add no dependency, and run the focused tests.
