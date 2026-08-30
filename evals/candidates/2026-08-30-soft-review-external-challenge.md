# Soft Review external challenge

Status: `DECIDED`
Decision: `ADAPT`
Landing recommendation: `EVAL_GAP_ONLY`

## Source

- Internal baseline: `IndelibleVivi/softpowers@0b10ff8bbcb64cac0cb189aa6c38d7dd9e9af2d7`
- Host baseline: `openai/codex@63d213884daea50e4f74efc192cdc44f549b67d5`
  (Apache-2.0), reviewed:
  - `codex-rs/exec/src/cli.rs`
  - `codex-rs/prompts/src/review_request.rs`
  - `codex-rs/prompts/templates/review/rubric.md`
- Evaluation candidate:
  `SathiaAI/adversarial-review@343861548fbf58fb1d69c521d33ea38d2ea6f00b`
  (MIT), reviewed:
  - `SKILL.md`
  - `evals/README.md`
  - `evals/corpus/clean-refactor-total/*`
  - `evals/corpus/test-weak-assert-charge/*`
  - `evals/report/live-20260823-211755.summary.md`
- Contrast source:
  `shakacode/agent-workflows@1614b6758735cb3d5a02c3a4313af4e0eb2db4a8`
  (MIT), reviewed:
  - `skills/autoreview/SKILL.md`
  - `skills/adversarial-pr-review/SKILL.md`
  - `skills/structural-review/SKILL.md`
  - `skills/type-design-review/SKILL.md`
- Historical control:
  `obra/superpowers@b36e0829c6d0140e93cfef2ca599b1b07d4a7797`
  (MIT); no new run or absorption cycle
- Review date: `2026-08-30`

No external source code or substantial wording was copied. Case shapes were independently
reduced to repository-local synthetic fixtures.

## Baseline attribution

Operational relevance: Codex native `/review` is included only as the lane's requested
host-attribution control. It is not Softpowers' ordinary review workflow or a replacement
target for Soft Review. The runtime landing turns on current Soft Review behavior against
the accepted case contracts; the native arm only prevents host behavior from being
miscredited as Softpowers value.

| Behavior | Host native review | Current Soft Review | Decision |
|---|---|---|---|
| Explicit uncommitted / base / commit targets | Yes | Accepts the same bounded target plus files or completed implementation | Host baseline; do not credit to Soft Review |
| Custom prompt combined with an explicit target flag | No at the pinned/current CLI seam; Clap flags conflict | Ordinary repo-grounded review prompt remains available outside native target mode | Preserve as a host limitation; no wrapper without a caller |
| Actionable, discrete findings; trigger scenario; severity; clean result | Yes | Yes | `ALREADY_COVERED` by host for generic review calibration |
| Final finding location overlaps the diff | Required by host schema | Soft Review can cite contract or nearest owning surface | Candidate difference, but SR-03 showed the host could still report the omission against a changed test line |
| Intended behavior, acceptance criteria, tests, schemas, contracts | Repository rules can override the host rubric | Explicit review target authority | Current Soft Review emphasis; no unmatched case benefit observed |
| Surrounding callers and provably affected code | Host rubric requires a concrete affected part | Explicitly says not to review a diff in isolation | Shared behavior |
| Tests that cannot catch the bug / false-green evidence | Available through repository rules and general correctness | Explicit review priority | Shared behavior in SR-04 |
| Goal-integrity verdicts | Not a native rubric concept | Soft Review only when product meaning, programme order, trust boundaries, or generalized infrastructure are implicated | Distinct Soft Review behavior; not needed for routine cases |

## Case manifest

| Case | Expected outcome | Falsifier |
|---|---|---|
| SR-01 clean permitted cleanup | No material finding or style padding | Either arm invents a finding after the contract explicitly permits the docstring and local rename |
| SR-03 specification omission | Report missing `export-data` without fabricating an absent implementation line | Reviewer returns clean or ignores the accepted fifth operation because no implementation line exists |
| SR-04 weak test / false green | Explain that `gateway.called` cannot prove exact amount, return value, or false-result failure path | Reviewer accepts green execution as contract proof |
| SR-06 conditional external trigger | Preserve the real leaking branch and impact while naming production-header uncertainty | Reviewer suppresses the defect as speculative, or states that the unobserved header definitely occurs |

## Matched run

Local ignored evidence:
`.fieldlab/lane1-runs/run-20260830-b/`.

- Host: `codex-cli 0.147.0`
- Requested model / effort: `gpt-5.6-sol` / `high`
- Native arm: `codex exec review --uncommitted` with only the ambient `softpowers`
  skill disabled through session config
- Soft Review arm: ordinary report-only review with the installed `softpowers` router;
  `diff -qr` confirmed the installed router and `soft-review` leaf matched this pinned
  canonical checkout
- Both arms used the same case state, read-only sandbox, no approvals, no network search,
  and fresh ephemeral sessions
- `codex debug prompt-input` confirmed the isolated native catalog omitted
  `softpowers`
- An earlier `run-20260830-a` was rejected from attribution because native review read
  the ambient Softpowers skill and the clean contract left docstring metadata ambiguous

| Case | Native review | Current Soft Review | Adjudication |
|---|---|---|---|
| SR-01 | Clean | Clean | True clean control; zero material findings |
| SR-03 | Found missing `export-data`, cited changed test as owning surface | Found the same omission, cited specification and test | Same true positive; no demonstrated negative-space advantage |
| SR-04 | One deduplicated finding covered exact amount, return value, and false-result path | Two true findings split success and failure coverage; also ran a mutation-style probe | Same material catch; Soft Review used more commands and findings |
| SR-06 | Found raw-header redaction bypass and noted the header was not established as token-free | Found the same conditional leak and explicitly kept production occurrence unproven | Same true positive; uncertainty did not erase impact |

## Finding adjudication

- Confirmed true positives: SR-03, SR-04, SR-06 in both arms.
- Confirmed clean: SR-01 in both arms.
- False negatives: none in this matched set.
- False positives: none in the accepted matched run.
- Conditional handling: both arms kept SR-06 as a real defect and did not claim the
  production trigger had been observed.
- Scope drift: no repository-wide audit or repair in either arm.
- Overhead: current Soft Review used more inspection / verification commands, split SR-04
  into two findings, and added goal-integrity verdicts to SR-03 and SR-06. These differences
  did not produce an additional material catch.

## External pattern decisions

### OpenAI native review

- Component outcome: `ALREADY_COVERED`
- Accepted kernel: explicit target resolution, introduced-change discipline, concrete
  trigger scenarios, clean-result permission, and short actionable findings.
- Boundary: this is host behavior, not Soft Review value. The target/custom-prompt conflict
  and diff-overlap schema remain actual host seams.

### Adversarial Review

- Component outcome: `ADAPT`
- Accepted kernel: labeled defect cases, explicit clean controls, false-positive pressure,
  and separate true-positive / false-negative / false-positive adjudication.
- Excluded machinery: mandatory multi-provider panel, provider-family independence,
  deterministic release verdict, rebuttal, immutable per-change ledger, scoring framework,
  API spend, and release governance for ordinary review.
- Landing plane: one repository-owned Field Lab canary, not runtime method prose.

### ShakaCode review workflows

- Component outcome: `ALREADY_COVERED`
- Accepted kernel: resolve the exact target, verify findings against current code, reject
  speculation, and stop after a clean result.
- Excluded machinery: mandatory pre-ship review, fix/re-review loops, independent validation
  for every consequential finding, PR labels, large receipts, and leaf/lens proliferation.

### Superpowers ancestry

- Component outcome: `REJECT`
- Keep the existing rejection of mandatory task-by-task reviewer dispatch and duplicate
  review ceremony. No new run was justified.

## Result

- Overall landing: `EVAL_GAP_ONLY`.
- Runtime method: no change to `methods/review.md`, router metadata, generated leaves, or
  installed payload. The Soft Review arm itself handled all four accepted semantic
  boundaries. Native parity is only attribution evidence and is not the reason to retain
  the current runtime.
- Smallest applied delta:
  - one combined executable canary at
    `evals/cases/review-evidence-boundaries/`;
  - this decision record;
  - the corresponding probe, eval inventory, and external-source registry entries.
- The combined canary protects the useful behavior while making clean false-positive and
  review-overhead pressure visible. Its exact disposition labels are eval-only and do not
  impose a response schema on ordinary reviews.

## Applied canary verification

- Saved-plan live run: `review-evidence-boundaries-20260830`, mode `canary`, one target-agent
  invocation against `softpowers-source`.
- Result: `1/1 PASS` on `codex-cli 0.147.0`, requested `gpt-5.6-sol` / `high`, approvals
  disabled and network access false.
- The report returned the exact clean / finding / finding / conditional dispositions,
  named `export-data`, rejected `gateway.called` as sufficient outcome proof, and kept the
  `X-Payload-Mode` production trigger explicitly `unobserved` while tracing the concrete
  redaction-bypass impact.
- Verification observed only `REVIEW.md` changed, four command executions, zero plan updates,
  zero subagent events, and a read of canonical `review.md`.
- This one current-source canary proves the landed case is executable; it does not replace
  the matched comparison above or establish longitudinal model variance.

## Uncertainty and reopen conditions

- One accepted run per case is sufficient to reject an automatic method change, not to
  estimate model variance or prove longitudinal superiority.
- The CLI command records requested model and effort; it does not independently prove
  provider-side model identity.
- Same-session self-review, external-provider comparison, and provider-family independence
  were not run. They remain non-default research arms, not missing completion gates.
- Reopen runtime wording only if a comparable real review or repeated matched runs:
  - miss a material specification omission;
  - accept a false-green test as proof;
  - suppress a real conditional defect because the external trigger is unobserved;
  - invent findings on adjacent clean controls; or
  - repeatedly expand routine review through unnecessary goal-integrity ceremony.
- Recheck host attribution when Codex changes target/custom-instruction composition or the
  diff-location output contract.
