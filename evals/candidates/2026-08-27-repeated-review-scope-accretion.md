# Repeated review scope accretion

Status: `DECIDED`
Decision: `ALREADY COVERED`

## Source

- Experience: real Batch Oracle review / repair dogfood, abstracted to exclude private implementation details and paths
- Pinned Softpowers ref: `31740deee5670ae4564b8f52b279d73476843708`
- Reviewed files: `methods/receive-review.md`, `methods/execute.md`, `methods/review.md`, `methods/finish.md`, `docs/pattern-intake.md`, `BEHAVIORAL_PROBES.md`, `evals/README.md`, representative `evals/cases/`, `scripts/build_skills.py`, `scripts/selftest.py`, `scripts/validate.py`, `scripts/validate_sync.py`
- Review date: `2026-08-27`

## Distilled pattern

Repeated expert review and repair handoffs can produce globally excessive work even when each finding is valid and each local implementation decision is reasonable. Broad discovery remains useful, but implementation commitment stays anchored to the accepted current outcome. Across rounds, the runtime agent must sometimes reassess the original acceptance boundary, cumulative diff, and existing proof before accepting more work into the tranche.

## Local signal

The Batch Oracle cycle showed that most durability, recovery, idempotency, barrier, and owner-closure machinery followed directly from the accepted failure semantics. Scope pressure instead accumulated through shared-substrate repairs, recursive authority auditing, PR / tranche drift, and early public closure.

Current `receive-review` wording can classify one review item as `Accept`, `Adjust`, `Verify`, `Reject`, or `Defer`, while `execute` already gives every mechanism a present-job test and stops after the settled request has risk-matched proof. The narrower possible gap is longitudinal: neither method explicitly tells the runtime agent to reconsider the original accepted goal and cumulative diff across repeated valid review rounds.

## Existing coverage

- `receive-review` treats feedback as evidence rather than authority and supports `Defer` for valid out-of-scope findings.
- `execute` rejects abstractions, fallbacks, retries, compatibility paths, dependencies, and checks without a present job.
- `execute` and `finish` already stop after the settled request and risk-matched proof are complete.
- `review` should remain free to discover adjacent, shared-runtime, security, architecture, and future-work concerns.

## Decision hypothesis

- Accepted kernel: broad review discovery; bounded implementation commitment; visible disposition of all validated findings; concrete separate-work ownership for real adjacent defects; cumulative scope reassessment across repeated rounds; stopping after the accepted outcome and sufficient proof. `Defer` answers whether a finding enters the current tranche, not whether a validated defect deserves later repair.
- Excluded machinery: upstream review templates; user-side normalization; mandatory owner approval; handoff envelopes; fixed response schemas; new skills or router logic; mandatory multi-agent review; per-round paperwork; blanket rejection of shared-infrastructure fixes; complexity limits that weaken required durability, recovery, idempotency, security, or concurrency semantics.
- Landing plane: eval first; runtime method only after demonstrated need.
- Smallest useful delta: one manual behavioral probe and one ordinary executable shadow case. If three comparable baseline runs show stable scope accretion, add at most two concise boundaries to canonical `methods/receive-review.md` and regenerate existing projections.

## Probe

- Fixture or task: a third-round heterogeneous review of a recoverable batch runner after two dogfood runs and green focused / adjacent tests.
- Candidate behavior: verify every item, fix the duplicate external action that falsifies the accepted contract, retain all findings in a disposition report, route real shared and adjacent defects to separately owned work, defer unsupported broad auditing and public-release closure, then stop. Current-tranche deferral must not erase the defect or silently decide its later repair priority.
- Baseline/control: the same case against the unmodified generated Softpowers skill tree; `tiny-copy` remains a lightweight direct negative control and `adopted-foundation-review` remains an adjacent authority control.
- Deterministic assertions: the duplicate-action regression passes; all five findings remain visible; adjacent source and proposal files remain untouched. A directly related test-helper cleanup is allowed because it does not accrete review scope.
- Semantic judgment: the runtime agent uses the original accepted goal, cumulative history, and existing proof to bound the tranche without hiding true discoveries or weakening declared failure semantics.
- Falsifier: current Softpowers consistently produces the bounded outcome, or results are unavailable / mixed rather than showing stable scope accretion.

## Verification if applied

- Fresh checks: `fieldlab validate fieldlab-pack.json` passed with 7 cases; `fieldlab selftest-pack fieldlab-pack.json` proved all 7 fixtures fail their intended assertions and all 7 expected overlays pass, with 0 target-agent invocations.
- Repeats: baseline run `baseline-repeated-review-20260827` executed the unmodified generated Softpowers payload three times with `gpt-5.6-sol`, `xhigh`, network disabled, and one pinned plan. The raw deterministic result was 2/3 pass; direct diff and disposition inspection found the bounded semantic outcome in 3/3.
- Adjacent controls: run `repeated-review-controls-20260827` used the same requested model / effort for the refined shadow case, `adopted-foundation-review`, and `tiny-copy`. `tiny-copy` passed. The refined shadow case satisfied every file and behavior assertion but exceeded the 20-command trace cap with 23 commands after an optional Oracle consultation and transport diagnosis. The authority control produced the correct sole `advances` verdict and changed only `REVIEW.md`, but its raw assertion rejected the semantically equivalent phrase `explicitly adopts` because the existing canary requires the exact substring `explicitly adopted`. Neither raw failure is scope accretion; neither limit was relaxed to manufacture a green result.
- Repository gates: canonical / generated sync passed; YAML validation passed for 13 skills and 12 router references; `PACK_MANIFEST.json` matched; the packaging self-test passed; the public-tree audit passed for 140 tracked / candidate files; diff and trailing-whitespace checks passed.
- Blocked or unavailable evidence: no LLM grader was configured or added. The target-agent receipt did not independently claim its actual model identity, so the evidence records the explicitly requested model rather than treating it as an observed model claim.

## Result

- Decision: `ALREADY COVERED`.
- Runtime method decision: no canonical method wording changed. Existing `receive-review` classification and completion reporting, combined with `execute` / `finish` scope and stopping boundaries, already produced the intended longitudinal outcome in this case. Generated runtime projections therefore remain unchanged and synchronized.
- Evidence: all three baseline attempts fixed RR-1, retained RR-2 through RR-5 in a disposition report, kept adjacent implementation and release surfaces outside the tranche, used the original contract and cumulative history, and stopped after focused proof. Attempts 1 and 2 matched the original exact changed-file assertion. Attempt 3 also removed an unused plain-send method from the directly affected test double; that caused the sole raw assertion failure but did not implement any adjacent review finding. The canary now checks the named adjacent source and proposal files directly instead of treating this bounded cleanup as scope accretion. A later refined run again preserved RR-2 and RR-3 as real separately owned defects rather than dismissing them, while leaving their source files untouched in the current tranche.
- Remaining uncertainty: this synthetic same-task evidence does not prove broader longitudinal improvement across future real tasks.
- Reopen condition: another comparable real task shows cumulative scope accretion, or later matched runs repeatedly modify adjacent findings despite the accepted boundary.
