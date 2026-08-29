# Focused test topology

- Existing unit contract: `test_contract.py` preserves the legacy boolean capability behavior.
- Local host seam: `host_surrogate.py` and `test_host_surrogate.py` exercise the documented available, denied, and missing envelopes through the real route selector.
- Named-host acceptance remains separate: the local surrogate cannot prove the production host's policy, runtime identity, or user-interaction behavior.

This seam reproduces one observable contract. It is not a production-host clone, general test framework, coverage programme, or release gate.
