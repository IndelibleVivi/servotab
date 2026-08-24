# Session-boundary open-loop continuity from `session-spoor`

Status: `DECIDED`
Decision: `ADAPT`

## Source

- Repository: `ennisaaaaaaaa-stack/session-spoor`
- Components: current-state / journal separation and session-boundary gap reminders
- Pinned ref: `6651a92da19f74c557684f5ccd319efdcc2ef9d8`
- License / rights note: the repository-root `LICENSE` is PolyForm Noncommercial 1.0.0. `DESIGN.md` still contains an older MIT label, so this review treats the root license as authoritative, copies no code or wording, and records only a clean-room mechanism summary.
- Reviewed files: `README.md`, `DESIGN.md`, `docs/spoor-hooks-proposal.zh.md`, `spoor_hooks.py`, `tests/test_spoor_hooks.py`, `bin/journal_append.py`, `LICENSE`
- Review date: `2026-08-24`

## Discovery context

The source addresses a broad agent trace and continuity problem through several storage, search, hook, and presentation surfaces. This record reviews only one narrower mechanism: recovering unfinished engineering work across real session or agent-handoff boundaries without turning every task into a continuity subsystem.

## Distilled pattern

Keep an overwritable current-state view separate from append-only records of decisions, confirmed pitfalls, and unresolved review items. At a real session-resume or agent-handoff boundary, inspect task-relevant open loops and surface a reminder through an action that already occurs, such as reading current state or beginning closure.

The reminder presents evidence; it does not decide what deserves a durable record or write on the agent's behalf. Retention follows a future caller: preserve information that a later session, reviewer, or operator is expected to use, and let task-local working detail end with the task.

## Local signal

Softpowers PR #3 is one narrow, public example. The owner draft remained open from `2026-08-19` while `main` advanced from `4180b49` through the goal-authority and verdict-precedence changes at `8e5fa9e`. It resurfaced in a later session, where the branch had to be compared with current authority, rebased, freshly validated, and then merged as `83a1ae5`.

That episode supports a shadow probe for task-scoped open-loop recovery. It does not establish a repeated runtime failure, justify global PR surveillance, or authorize a daily Softpowers behavior change.

## Existing coverage

- `Soft Plan` preserves complete scope across sessions and asks an implementation handoff to name branch or workspace assumptions.
- `Soft Finish` inspects the active branch, workspace, diff, verification, and Git / PR state before integration.
- GitHub retained the draft PR, branch, review surface, and historical checks. The remaining gap was discovery: a later session still had to identify that this particular owner-controlled open loop was relevant and stale.
- The accepted scope for this intake is documentation / probe only. The source, this record, and PR #3 do not authorize a runtime method or infrastructure change by their own existence.

## Decision hypothesis

- Accepted kernel: separate replaceable current state from append-only decisions, pitfalls, and pending-review traces; inspect unfinished work at real session or agent-handoff boundaries; attach reminders to existing start, finish, or state-read actions; keep the hook advisory and leave recording judgment to the agent; retain information only when a future caller exists.
- Excluded machinery: the source's MCP servers, three-layer directory model, archive, FTS, dashboard, ledger, fixed four-hour threshold, background daemon, global PR surveillance, new implicit router, new skill, dependency, runtime method wording, installer, generated pack, version, changelog, or live target-agent run.
- Landing plane: Field Lab / maintainer first.
- Smallest useful delta: retain this candidate and add one task-scoped shadow probe. Do not change Softpowers runtime behavior in this intake.

## Probe

- Fixture or task: resume repository work that has an owner draft PR while its base branch has advanced since the last active session.
- Candidate behavior: discover and report the relevant PR, head and base relationship, ahead / behind state, CI freshness for the current head, conflict risk, and the smallest closure action before editing or merging.
- Baseline/control: complete an ordinary local change within one session. Do not scan unrelated PRs, create a journal, start background monitoring, or add a fixed end-of-session ritual.
- Deterministic assertions: the positive case identifies the exact task-relevant PR and current refs; distinguishes historical green checks from checks on the current head; reports merge or conflict state without mutating unrelated branches; the negative control creates no continuity artifact or global repository scan.
- Semantic judgment: the reminder recovers a real open loop with less work than manual archaeology while remaining quiet for self-contained tasks.
- Falsifier: existing `Soft Plan` and `Soft Finish` already recover comparable dormant open loops consistently, or the additional mechanism causes low-value PR scans and workflow noise.

## Verification if applied

- Start with the PR #3 replay as existing dogfood and preserve its exact public Git / GitHub evidence.
- Add one owner-draft positive case and one single-session negative control before considering method wording.
- Evaluate relevance and noise, not the number of repositories or PRs scanned.
- Use Skill Field Lab only if the behavior claim remains unresolved. No live target-agent run is authorized by this record.

## Result

`ADAPT` at the documentation and maintainer shadow-probe plane. The source exposes a useful separation between current state, durable engineering judgment, and boundary-triggered reminders, while the local evidence supports only task-scoped recovery.

No runtime method, skill, dependency, installer, generated payload, version, changelog, background process, or live evaluation is approved here. The source's `Dying Will` process-ownership mode remains outside this record; it needs a separate candidate and a concrete Soft Debug or infrastructure signal.

Reopen when a comparable owned PR or handoff is missed again, the shadow probe shows a gap in current Plan / Finish behavior, or the source materially changes its session-boundary contract.
