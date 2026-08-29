# Test-systems boundary from private host-bridge dogfood

Status: `DECIDED`
Decision: `ADAPT`

## Source

- Experience: real private host-bridge debugging dogfood, abstracted to exclude private source, deployment identities, raw logs, personal paths, and owner-only acceptance material
- Pinned Softpowers baseline: `5aeb42151d441fce65267427bd70fe367112e66d`
- Primary-case pin: the exact private checkout ref and dirty-work snapshot were reviewed on `2026-08-29` and are retained outside the public tree under the private-continuity boundary
- License / rights note: owner-controlled private evidence; no private code or wording is copied into this record or its synthetic case
- Reviewed Softpowers files: `skills/softpowers/SKILL.md`, `methods/debug.md`, `methods/tdd.md`, `methods/execute.md`, `methods/plan.md`, `methods/verify.md`, `methods/finish.md`, their generated router references and leaves, `docs/pattern-intake.md`, `docs/external-patterns.md`, `BEHAVIORAL_PROBES.md`, `evals/README.md`, `evals/candidates/README.md`, representative `evals/cases/`, `fieldlab-pack.json`, `PACK_MANIFEST.json`, `README.md`, `CHANGELOG.md`, and build / sync / validation scripts
- Reviewed primary-case evidence classes: repository governance, package commands, CI topology, process-level protocol smoke, embedded host bridge, current-state record, owner acceptance contract, and the active local-host work in progress
- Review date: `2026-08-29`

## Distilled pattern

When a material behavior boundary has no cheap reliable reproducer, the missing evidence surface is itself a testability problem. Establish the smallest stable executable seam that reproduces the boundary's observable contract, localizes the first divergence, and remains cheaper than another remote hypothesis loop.

The seam may be a local surrogate, fake host or transport, deterministic fixture, browser or integration harness, focused command, or proportionate CI lane. It does not duplicate production. The exact remote host and owner remain the final acceptance surface whenever their behavior is part of the contract.

## Local signal

The primary case already had focused route-level unit coverage and process-level protocol/resource conformance. A manual local emulator was available, yet there was no repeatable browser-host test that mounted the embedded application, crossed the capability bridge, exercised the user action, and observed the resulting host disposition. A real host therefore revealed failures but also carried cache, transport, capability, policy, runtime identity, and owner-interaction variables into each debugging loop.

At review time, browser automation had only reached dependency-present work in progress. No committed host fixture, stable test command, CI lane, or execution receipt was observed. This proves the local problem and a candidate capability direction; it does not prove wiring, current exercise, or later effectiveness.

Evidence maturity is therefore:

- **Observed problem:** repeated remote feedback carried too many simultaneous hypotheses while an important host boundary lacked a cheap executable seam.
- **Capability:** existing manual local-host support and an in-progress browser dependency show that a local lane is feasible.
- **Wiring / current exercise:** not verified for an automated browser-host lane at the reviewed snapshot.
- **Later effectiveness:** not verified; no later comparable failure has yet shown fewer remote loops or faster localization.

## Existing coverage

| Surface | Current ownership | Candidate boundary |
|---|---|---|
| `debug` | Define and reproduce the failure, localize the first violated assumption, keep one active hypothesis, reset topology when patches cascade, and fix the causal source. | It is the escalation source. A missing cheap reproducer for a material boundary becomes a bounded testability slice; ordinary localized bugs stay in `debug`. |
| `tdd` | Create behavior-level red-green, characterization, or test-alongside evidence; use deterministic fakes at stable external interfaces. | It implements regression evidence inside an established seam; it does not need to own repository-wide test topology. |
| `execute` / `plan` | Implement a settled harness, fixture, command, or CI change in coherent slices, preserving the requested outcome. | They remain the implementation path once the structural evidence decision is settled. |
| `verify` | Map exact claims to fresh focused, adjacent, broad, artifact, runtime, named-host, and owner evidence. | It consumes the resulting proof surface and prevents a local surrogate from being described as remote acceptance. |
| `finish` | Inspect the final tree, documentation, Git state, and integration readiness. | Release readiness and publication remain outside the candidate territory. |
| Candidate territory | No current router reference or leaf. | Explicit design/audit/repair of a repository's executable evidence topology, or a handoff from `debug` after the absence of a cheap reproducer is established. |

The existing chain already covers phase transition, ordinary regression testing, mocks/fakes, risk-matched verification, and named-host acceptance. The only demonstrated runtime wording gap was that `debug` required a cheap reproducer without explicitly treating its absence as a bounded testability problem.

## Competing interpretations

### A — Existing methods are sufficient

This is strongest for the observed founding host-bridge failure. `execute` already transitions to evidence-driven debugging after unexplained verification failure; `debug` already resets topology after a patch cascade; `tdd` already supports stable-boundary fakes; `verify` and `finish` already separate local proof from named-host and owner acceptance. A narrow `debug` clarification may produce the complete needed behavior without a new method.

### B — A distinct episodic method exists

The independent caller is an explicit request to design, audit, repair, or operationalize repository testability, harnesses, test topology, or CI evidence lanes. Its decision object is an `ExecutableEvidenceTopology`: behavior boundary -> cheapest faithful reproducer -> first-failure localization -> focused/adjacent/broad command -> local automation versus remote/owner acceptance. Its durable outcome can be a small harness and command rather than a mandatory document.

### C — A new leaf costs more than it saves

`soft-test` can over-trigger on routine test execution, feature tests, coverage work, or release readiness. Softpowers also has a direct precedent: generic behavior-eval machinery once had an independent caller, runner, fixtures, schemas, and artifacts, yet was correctly moved out of the distributed pack into standalone Field Lab. Independent caller and durable output are necessary, not sufficient, for a runtime leaf.

## Decision hypothesis

- Component outcomes:
  - Existing `debug` missing-reproducer handoff: `ADAPT`
  - Maintainer candidate and deterministic positive canary: `ADAPT`
  - New distributed leaf, router reference, implicit activation, version, and installation surface: `DEFER`
- Accepted kernel: identify material behavior boundaries without a cheap reliable reproducer; build only the smallest faithful executable seam; prefer first-failure localization over another opaque full-E2E or remote loop; leave routine tests to TDD/execute and exact claims to verify; preserve named-host and owner acceptance.
- Excluded machinery: mandatory test plans, coverage targets, test pyramids, per-task ledgers, universal topology documents, default full E2E, retries or timeout inflation, production duplication, routine release ceremony, a new lifecycle stage, a new distributed leaf, and routing on the word `test`.
- Landing plane: one narrow clarification in the existing `debug` method plus Field Lab / maintainer evidence.
- Smallest useful delta: clarify the missing-reproducer escalation in canonical `methods/debug.md`, regenerate its existing projections, and add one portable positive canary while reusing existing parser and copy controls.

## Naming challenge

- **No new leaf now:** recommended. It avoids claiming an activation boundary that has not yet been exercised.
- **`soft-test`:** too broad; users can reasonably read it as run tests, write ordinary tests, raise coverage, or verify a release. A display title such as “Test Systems” does not repair the command's ambiguity.
- **`soft-test-system`:** clearer about structural scope but still sounds like a general platform and remains wider than the evidence.
- **`soft-test-design`:** under-specifies audit, repair, and operationalization, and can encourage an unnecessary design document.
- **`soft-testability`:** the narrowest eventual candidate if later evidence still supports a leaf. It names the proven seam/surrogate/localization problem without claiming all testing or release work. It is not reserved or distributed by this decision.

## Probe

### Applied positive case

- Fixture: `evals/cases/missing-host-test-seam/`
- Candidate behavior: existing green unit contract evidence does not conceal the absent host-envelope seam; create a bounded local surrogate, reproduce the capability disposition, fix the revealed route, add a focused command, and keep named-host acceptance separate.
- Deterministic assertions: the prompt-disclosed surrogate, regression, and topology artifacts exist; independent commands exercise available, denied, and missing envelopes through the source and surrogate; the focused suite passes; only the four disclosed files change. No assertion depends on a hidden code phrase, prose sentence, method name, or reference-loading sequence.
- Semantic judgment: the work reduces the hypothesis surface without cloning production or creating a general testing programme.
- Falsifier: the agent continues remote patching, adds unrelated unit tests or infrastructure, treats the local surrogate as production acceptance, or cannot distinguish the case from an ordinary regression with an adequate reproducer.

### Existing adjacent controls

- `stale-cursor`: an adequate deterministic reproducer exists; route through ordinary debug/TDD and change only the source invariant.
- `tiny-copy`: a one-file copy change stays direct with focused proof and no plan, harness, or test-system work.

### Future matched promotion matrix

Before any leaf proposal, matched positive/negative behavior evidence should cover:

| Scenario | Expected boundary |
|---|---|
| Remote host gap | `debug` establishes the missing reproducer, then a bounded local surrogate; production remains final acceptance. |
| Unlocalized full-E2E timeout | Add one or two stable integration seams and diagnostics; do not inflate timeout or rerun the opaque suite. |
| New external boundary | Establish the cheapest local contract counterpart and one representative real integration proof; do not duplicate production. |
| Focused parser bug with a failing test | Ordinary `debug` -> `tdd`; no structural test-system work. |
| Ordinary feature with unit/integration tests | `execute` / `tdd`; no topology document or new harness absent evidence. |
| CSS or copy change | Focused rendered/manual check; no candidate activation. |
| “Run the tests” | Execute the relevant existing commands; no strategy work. |
| Release readiness | `verify` / `finish`; no transfer of release authority. |
| Named-package coverage request | Follow the real risk and caller; do not activate from the word coverage alone. |

No live target-model run is authorized by this record. Deterministic fixture selftest can prove only that the case contract is internally credible, not that current or future routing selects it reliably.

## Verification if applied

- Fresh checks: generated source/projection sync passed; exact validation passed for 13 skills, 12 router references, and 1,523 `SKILL.md` lines; `PACK_MANIFEST.json` matched; the packaging selftest passed; the public-tree audit passed over 150 tracked/candidate files; Python compile and diff whitespace passed. No shell scripts exist in the current source tree, so shell syntax validation was not applicable.
- Deterministic Field Lab evidence: validate/list discovered 1 subject and 8 cases; selftest found the unresolved `missing-host-test-seam` fixture failing 6 assertions and its expected overlay passing all 7 assertions. All 8 cases were credible and target-agent invocations were `0`.
- Repeats: none; no live target-model invocation or budget was authorized.
- Adjacent controls: the existing `stale-cursor` and `tiny-copy` contracts remain in the same Field Lab pack; their unresolved fixtures failed the intended assertions and their expected overlays passed all deterministic assertions.
- Blocked or unavailable evidence: actual candidate activation, routing variance, automated browser-host exercise in the primary case, remote-loop reduction, independent real-topology transfer, and later effectiveness.

## Result

- Decision: `ADAPT` at the existing-method and maintainer/eval planes.
- Evidence: the primary case proves a serious missing executable seam; current Softpowers already owns most adjacent behavior; the narrow `debug` repair and portable canary capture the remaining demonstrated gap without expanding the distributed pack.
- Strongest argument for a future leaf: explicit testability/test-topology work has an independent caller, decision object, and durable executable outcome that are not identical to causal debugging, behavior-level TDD, or claim verification.
- Strongest argument against a future leaf: the observed failure may be completely solved by the narrow existing-method repair, and no prospective comparable task yet proves that a specialist method reduces token/time cost or routing variance.
- Remaining uncertainty: transfer beyond the founding private case is plausible but unproved; synthetic canaries and historical analogues are not later real-task effectiveness.
- Reopen condition: a later comparable host failure exercises the local seam and shows materially fewer remote loops or sharper localization; an independent real topology needs the same structural decision; or matched live canaries show that the current method chain still misses the boundary.

## Promotion conditions

A distributed leaf remains blocked until all of these are true:

1. The founding project's local host lane is complete and is actually used on a comparable failure.
2. Fresh evidence shows fewer remote deployment/debug loops or materially sharper first-failure localization.
3. At least one independent real topology supports the same method boundary, or matched canaries show stable distinction across equivalent environments.
4. Parser, ordinary feature, CSS/copy, run-tests, release-readiness, and coverage-only controls remain negative.
5. Router/leaf activation does not over-trigger on ordinary test language.
6. The method's expected token, time, files, and command cost is lower than ad hoc handling, while ordinary repository work stays dormant.
7. The owner explicitly accepts the public leaf name, runtime contract, and distribution surface.
