# Plan strategy evidence

Status: unreleased source candidate; the first bounded live comparison is complete.
Candidate: six accepted attempts. Baseline: five accepted and one rejected attempt.
Full REQ-12 acceptance remains open.
Contract: [Plan specification, REQ-12](../docs/specs/plan-strategy.md).
Current work: [single implementation entry](../docs/plans/plan-strategy.md).

## Scenario coverage and limits

| Spec case | Available source scenario | Observed behavior and remaining limits |
|---|---|---|
| C01 | `tiny-copy`, `delegate-trivial-direct` | Four `tiny-copy` attempts accepted; each changed only the requested line, with no new plan or user questions |
| C02 | `plan-shared-assumption` | Four attempts accepted: inspected provider and pre-edit CLI failure, then repaired the shared collector |
| C03 | `plan-domain-handoff`; mature-path activation seed | Handoff rehearsal covers reuse; mature multi-step execution still needs a real attempt |
| C04 | `plan-shared-assumption` | Four attempts accepted with pre-edit provider/CLI evidence and all three outputs |
| C05 | `plan-domain-handoff` | Sequencing rehearsal only; actual rendered experience is not established |
| C06 | `tranche-only-plan`, `plan-domain-handoff` | Planning-only authority and no implementation write; the latter grants only the existing record |
| C07 | `plan-resume-reconcile` | All four corrected the obsolete touchpoint and retained the settled local outcome; one baseline failed external-state retention |
| C08 | `plan-resume-reconcile` | All four checked stale completion against current source/tests before repair; no long-lived host-session recovery claim |
| C09 | `plan-resume-reconcile` | All four used the explicit entry and preserved the unrelated lane; simultaneous-writer stress remains untested |
| C10 | `plan-shared-assumption`, `plan-resume-reconcile` | These expose an initial false assumption; mid-run contradiction with independent work remains a live perturbation |
| C11 | `tranche-only-plan`, `spec-chain` | Bounded tranche versus complete coverage |
| C12 | `plan-domain-handoff` | One commission, domain judgment alters effort/order, no new tracker |
| C13 | `plan-resume-reconcile` | Three of four recovery attempts accepted; baseline repeat 1 omitted unknown historical publication state. Replacement/cancellation and missing-record variants remain due |
| C14 | All three new cases | Observed target attempts used shell without workers/native task tools; domain handoff still awaits a live attempt |

The three new cases add two executable CLI repairs and one domain-handoff rehearsal.
They reuse Field Lab v2 and the existing assertion helpers. The CLI's JSON, CSV and
count paths are exercised in separate processes; source variants reject first-page
only collection, title-based identity, duplicated overlap and hardcoded cursors.
The resume case rejects edits to the unrelated plan, private input or a parallel
active pointer. Synthetic private content is test data, never an actual export.

Fifteen adversarial controls include three new deltas. Correct files with fabricated
recovery/deployment claims and a domain plan with inverted judgment dependencies
still pass structural assertions; mandatory semantic review must reject them.
No fixed headings or word count prove strategy. Method-path mentions are not content
read evidence; absence of a leaf read does not automatically mean incorrect behavior.

## Authorized bounded live comparison

The owner authorized at most 12 target invocations and 8 independent semantic reviews on 2026-10-02. Two saved canary plans pin the same fixtures and settings, six target invocations each. Field Lab’s matched mode requires an isolated control, so the two version subjects remain separate canary plans for this bounded comparison; neither represents an isolated-host attribution experiment. The owner selected `gpt-6.1-sol` with `xhigh` effort before any target invocation. The superseded Astra plans were never run. The inspected Codex CLI is 0.159.1.

The baseline plugin came from `128cd20777d3660c50449cb653f207ddab893c78`;
the candidate skill snapshot matched `fcc053b34c13eaeb01f9e01499c93e553e5f43b7`.
Both used identical current case fixtures:

- `tiny-copy` (negative control), `plan-shared-assumption` (strategy),
  `plan-resume-reconcile` (fresh-context recovery).
- Two repeats per case and subject: **12 target-agent invocations total**.
- Pin one available Codex model and effort in saved Field Lab plans, identical for
  both subjects; workspace-write, no network, no subagent, 600 seconds per attempt.
  Model selection must be observed from the configured host before planning; do not
  infer capability or quota from a name. No retries or extra model graders are included.
- The eight semantic receipts each received one independent agent review, also
  requesting `gpt-6.1-sol` / `xhigh`, against the full trace, diff, final output and
  exact requirements. The four `tiny-copy` receipts need no semantic review.
  Actual use: **12 target attempts + 8 review-agent invocations**, with no retries.
  These count agent invocations, not individual backend requests within an agent.
- Keep every result, failure and environment difference outside the source tree.
  Compare actions and full outputs before costs. A baseline success is not credited
  as a candidate improvement. Unavailable or timed-out runs remain observations.

## Observed results — 2026-10-02

Both six-attempt runs completed, without timeout, forced termination or retained
orphan processes. All twelve passed the declared deterministic assertions. The
receipt-bound acceptance results are:

| Case | Baseline accepted | Candidate accepted |
|---|---|---|
| `tiny-copy` | 2/2 | 2/2 |
| `plan-shared-assumption` | 2/2 | 2/2 |
| `plan-resume-reconcile` | 1/2 | 2/2 |

Baseline recovery repeat 1 was rejected for a specific semantic omission: it
avoided replay and repaired the code, but never read the ambiguous publication
receipt or retained the unknown historical submission outcome in its final task
record or response. Saying that this session did not publish did not preserve
that uncertainty. Baseline repeat 2 and both candidate repeats retained the
unknown state. Candidate repeat 2 briefly wrote “not published”, then corrected
that unsupported wording before final verification and delivery; the final
judgment does not erase that intermediate correction.

All four shared-assumption attempts inspected the actual provider and observed a
real JSON CLI failure before editing the shared collector. They completed all
three consumers and edge cases without reopening intake. This was success for
both versions, not a measured improvement attributable to the candidate. The
candidate's four semantic traces contain commands reading the Plan reference;
the baseline's contain no Plan-reference reads. That is a routing diagnostic,
not proof of exclusive host selection or sufficient method application.

Recorded command counts by repeat were baseline/candidate: `tiny-copy` 5,2 / 6,3;
shared assumption 17,13 / 16,16; recovery 13,14 / 14,14. Totals were 64 / 69 shell
commands, 823.655 / 905.193 summed target-process seconds, and 18,117 / 19,007
reported output tokens. These are descriptive costs, not a speed or quality score:
the two version runs overlapped on one host, individual durations varied, and
there were only two repeats per case. No general efficiency gain is established.

Run IDs are `20261002T150948036899Z-9db05732` (baseline) and
`20261002T150948131386Z-03ee0027` (candidate). Raw traces, immutable receipts,
independent judgments and receipt-bound reviews remain outside the public tree.
Reviewers were separate agents using the same requested model; they were not
blinded to subject identity. Receipts record the requested model, not verified
backend model identity. Workspace delivery was verified, but host selection
remains unknown; this is not an isolated-host causal experiment.

The acceptance checker initially rejected the separately named study because
its expected lab ID was fixed to `servotab`. The added explicit `--lab-id` option
preserves the original default, exact case/prompt comparison, artifact integrity
and independent review requirements. No receipt was rewritten and no target was
rerun. Nineteen focused checker tests passed, including wrong-study rejection,
required semantic review, tamper rejection and the read-only CLI path. Independent
review outputs were normalized into Field Lab's exact-key mapping without changing
their judgments; original reviewer output is retained.

## Remaining acceptance

This first comparison does not close the whole matrix. Follow-up coverage must be
chosen from the observed failures and remaining boundaries: accurate/stale/missing
records, true mid-run evidence change, replacement/cancellation, and a representative
rendered task. That follow-up requires its own bounded plan and authority.

The current Servotab upgrade is longitudinal dogfood of a coordinator/worker and one
shared plan; it is not an independent matched experiment. A separate ordinary
engineering task remains required for full REQ-12 acceptance. The synthetic export
repair cannot be relabeled as that ordinary-use receipt.

## Reading an attempt

Inspect order and consequences: when did evidence capable of changing the route
arrive, did the agent propagate an assumption before inspecting it, was the entire
result delivered, and did recovery change the correct record? Assess actual user
questions and domain acceptance. Preserve costs as context, not a quality score.
Use [acceptance.md](acceptance.md) for receipt-bound independent judgments; a local
expected overlay, structural pass, plan self-report or dogfood note does not close
those requirements.
