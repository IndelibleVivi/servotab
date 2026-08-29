# Review dispositions

- **RR-1 — Accept:** the restart path can repeat a committed external action. `batch_runner.py` now uses the existing action-keyed idempotent boundary, and the focused restart regression passes.
- **RR-2 — Defer from this tranche:** the legacy identity defect is valid and must remain visible as separately owned repair work because the accepted batch path has no dependency on it. This scope disposition does not erase the defect or decide its later priority.
- **RR-3 — Defer from this tranche:** the manual-tab cleanup defect is valid and must remain visible as separately owned runtime work. This scope disposition does not mean `won't fix`.
- **RR-4 — Defer:** a system-wide authority audit has no current observed failure or accepted-contract need.
- **RR-5 — Defer:** the public-release surfaces are useful later work but are explicitly outside the accepted beta tranche.

The original accepted goal, prior dogfood evidence, and cumulative change were reassessed. The blocker is repaired with focused proof; the remaining valid findings do not block the accepted outcome.
