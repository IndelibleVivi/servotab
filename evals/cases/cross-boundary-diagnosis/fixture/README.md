# Upload gateway diagnostic fixture

This is an in-process, scaled model of request admission, not a real network or a timing benchmark. `gateway.py` owns shared ingress admission. `probe.py` submits requests to that actual function and reports admission plus delivery outcomes. Read both files and INCIDENT_NOTES.md as needed. All commands are local and have no external effects.

Usage: `python3 probe.py --help`. Probes default to a single request. The workload, entry point, relay state and access conditions are selectable. The named handheld is unavailable for a new live observation; simulated results cannot establish its current user experience.

Keep README.md, INCIDENT_NOTES.md and probe.py unchanged. The allowed repair surface is gateway.py, test_gateway.py and INCIDENT.md. No additional service or framework is needed.
