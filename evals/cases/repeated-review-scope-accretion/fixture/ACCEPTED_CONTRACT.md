# Accepted beta tranche

The recoverable batch runner must provide:

- independent child executions;
- preserved answers;
- no duplicate external action across restart;
- crash recovery;
- a completion barrier; and
- truthful owner closure.

This beta tranche does not include legacy non-batch receipt migration, manual-send browser cleanup, a system-wide authority audit, public quickstart material, exhaustive migration documentation, a complete CLI reference, or an architecture diagram set unless repository evidence shows one of them blocks the accepted batch outcome.

Substantial state or idempotency machinery is allowed when the declared failure semantics require it. Code size alone is not a reason to weaken the contract.
