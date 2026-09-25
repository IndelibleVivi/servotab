# Behavior acceptance

A Field Lab `pass` records the declared deterministic assertions. It does not close
semantic requirements. Field Lab v0.2 (inspected baseline source `d9f717a`)
records pending
human review alongside that pass; its runner can then discard a passing workspace.
The diff, final response and verification artifacts remain the review evidence.

Servotab uses the existing v2 case `human_review_requirements` and separate,
receipt-bound review record. No model runner, installer, grading service or schema
fork is bundled. `scripts/check_behavior_acceptance.py` is a read-only subject
acceptance check, not a replacement for Field Lab's execution or permissions.

## Close a real attempt

Use the Servotab revision whose case and prompt produced the attempt. Inspect the
entire final response, diff and required artifacts, not just labels or the expected
answer. A compatible independent Field Lab review record must use each exact
requirement string as a `requirement_outcomes` key, with values `supported`,
`not-supported` or `inconclusive`. Give the material reasoning in `rationale`; a
correct label with contradictory reasoning must be rejected.

Field Lab baseline source `d9f717a` defines that review field and its internal writer
accepts a mapping, but its public CLI exposes no input for it. Feature commit
`57eb9ac`, merged into Field Lab main at `b87b14b`, adds the supported public input:

```bash
fieldlab review /path/to/study/fieldlab.json \
  --review-id independent-review \
  --receipt /path/to/attempt/receipt.json \
  --independence separate-agent \
  --judgment supported \
  --rationale "Bounded reasoning for the inspected attempt." \
  --requirement-outcomes /path/to/requirement-outcomes.json
```

Against that merged-source CLI, synthetic receipts for the then-current nine
human-required cases produced review records accepted by the Servotab checker,
with zero target-agent invocations. The current source candidate has twenty
human-required cases out of twenty-four; its four delegation canaries use the same
declared mechanics. One `delegate-bounded-investigation` attempt now has an independent
review supporting all three semantic requirements, but its deterministic receipt
was rejected. After the duplicate literal-label assertions were removed, a new
separately budgeted attempt passed deterministic verification and a new independent
review supported all three requirements; Servotab acceptance returned `accepted`.
The other three delegation canaries have no live review.
This proves producer-consumer contract compatibility only: the source is merged
but not released, installed or activated, and synthetic outcomes are not actual
independent human review. Do not hand-edit or manufacture a review to cross the
gate, and do not weaken the exact mapping requirement.

```bash
python3 scripts/check_behavior_acceptance.py /path/to/attempt/receipt.json
python3 scripts/check_behavior_acceptance.py /path/to/attempt/receipt.json \
  --review /path/to/separate-review.json
```

The command prints JSON and exits with:

| Code | Status | Meaning |
| --- | --- | --- |
| 0 | `accepted` | Encoded deterministic evidence passed; required independent review supports every requirement. |
| 1 | `rejected` | Attempt failed or a review requirement was rejected. |
| 2 | `needs-review` | Required independent review is missing, self-reviewed or inconclusive. |
| 3 | `invalid-evidence` | Stale/missing/tampered artifacts, mismatched case/prompt/review digest or malformed records. |

Purely deterministic cases do not acquire a mandatory review. Any negative review
outcome overrides a supported summary. The receipt stays immutable; the command
writes nothing and never invokes a target model. Keep private attempts and reviews
outside the public tree. Do not manufacture reviews to make CI green.

Checksums bind the supplied evidence; they do not authenticate its author or prove
its reasoning. Supply trusted Field Lab records and an actual independent review.
The command compares Field Lab's normalized attempt-case record with a deterministic
projection of the current raw case, so loader-added defaults do not become false
drift while substantive case changes still fail closed. It checks current case and
prompt identity, not the entire current plugin, fixture tree or host. Those
identities remain in Field Lab's pinned run inputs.
An accepted result supports that attempt only, not exclusive causation, deployment,
owner acceptance, superior performance or longitudinal reliability.

## Adversarial controls

`adversarial-controls.json` preserves twelve deliberately wrong output deltas from
the audit and later rehearsals. They are test material, never instructions or
genuine model outcomes. Apply each to its case's expected overlay in a disposable
fixture copy.

- `weak-check`: comment-only tests must fail the candidate regression check. The
  check runs the candidate's own suite with repaired and known-bad policy in fresh
  temporary directories; import errors, empty/skipped suites and unrelated failures
  are not red evidence. It does not edit the candidate workspace.
- `repeated-review-scope-accretion`: authority rewrites and unrelated new files must
  fail the exact write-scope assertion. The prompt declares this bounded fixture's
  two permitted outputs; existing restart tests already exercise its blocker.
- `spec-chain`, `review-evidence-boundaries`, `missing-host-test-seam`: the deliberately
  contradictory prose still passes structural checks. Without an independent
  review it must remain `needs-review`. A reviewer should reject it for the stored
  reason, not accept it for containing the required IDs or disposition labels.

The three worktree rehearsals add contradictory decision outputs that deliberately pass structural assertions. Review must reject unsafe deletion, duplicate creation, and refusal of already authorized safe parking; their file existence is not behavior proof. No rehearsal receipt may be promoted to real cleanup evidence.

The `discussion-intake` rehearsal adds four incorrect assessments: selecting only
the final theme, retaining a superseded mechanism, treating embedded proposals as
execution permission, and reporting permission honestly while losing other important
content. All four pass the structural file checks and must be rejected by review
for their stored reasons. Intake coverage, outcome/mechanism separation and the
permission boundary are semantic; a passing file-existence and write-scope gate
does not establish them. Alternate valid wording may explicitly say "not authorized"
or "out of scope"; structural checks must not reject those phrases. Separate tests
reject changes to the source discussion or an extra file.

Ordinary CI replays all twenty-four baseline/expected file-and-command oracles, the
twelve adversarial deltas, alternate valid regressions, malformed/empty test suites,
authority edits and incomplete CLI deliveries. Synthetic receipt tests exercise
acceptance gating without representing an actual attempt or human review.

One explicitly budgeted live attempt was run for `delegate-bounded-investigation`
on 2026-09-15. Its separate-agent review supported all three semantic requirements,
but three exact literal workspace assertions failed, so the immutable receipt and
Servotab acceptance remain `fail` and `rejected`. No retry occurred under that
first invocation budget. The current canary removes those three literal label checks:
deterministic assertions retain report existence, exact write scope, the focused
command, and trace ceilings, while the existing exact-key human review remains
the authority for report meaning and matching runtime evidence. A separately
authorized second attempt against that revised case passed those deterministic
checks; a new separate-agent review supported all three requirements, and the
checker returned `accepted`. This closes only the pinned case. Native plugin
activation, explicit leaf selection, method
overhead and comparative agent outcomes still require separately authorized
host/model observations. Reference reads and command ceilings are diagnostics;
correctness, complete requested behavior and permission compliance come first.
