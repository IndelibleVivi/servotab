# Dependency-aware decision frontier from `grilling`

Status: `DECIDED`
Decision: `ADAPT`

## Source

- Repository: `mattpocock/skills`
- Components: `grill-me`, `grilling`
- Pinned ref: `1bb95954ef0d06ba4d64a9c267fb75f57c614a1f`
- License: MIT
- Reviewed files: `skills/productivity/grill-me/SKILL.md`, `skills/productivity/grilling/SKILL.md`, `skills/productivity/grill-me/agents/openai.yaml`, `skills/productivity/grilling/agents/openai.yaml`, `.agents/invocation.md`, `README.md`
- Review date: `2026-08-19`

## Discovery context

A community recommendation presented `grill-me` as a must-install and encouraged serious forks of Matt's repository. Popularity and recommendation strength were treated as discovery signals only, not as authority over Softpowers.

## Distilled pattern

Represent an unsettled design as a dependency tree. In each round, ask only the current frontier: decisions whose prerequisites are already settled. Recompute the frontier after the user's answers rather than asking downstream questions prematurely.

Environmental facts belong to the agent: inspect the repository, tools, runtime, or authoritative sources instead of delegating searchable facts to the user. Product and value decisions remain with the user. Each material question includes the agent's recommended answer. An unresolved fact blocks only the branches that depend on it, not the rest of the conversation.

## Local signal

No repeated Softpowers failure is currently recorded for this exact behavior. `Soft Brainstorm` already reconstructs the real problem, separates settled choices from open decisions, asks only material questions, and rejects mandatory interviews.

The remaining possible gap is narrower: a complex design conversation may flatten independent and dependent decisions into one round, or ask a downstream question before its upstream semantics are stable. The source gives that ordering problem a precise and reusable model.

## Existing coverage

- `methods/brainstorm.md` starts from repository evidence and asks only questions that materially change behavior or architecture.
- It recommends one focused question at a time when useful, and permits explicit assumptions when best-effort progress is requested.
- It already rejects mandatory interviews, reopening settled choices, and ceremony before implementation.
- Softpowers uses one implicit router plus explicit leaves; it does not need a new wrapper-to-core skill dependency to express this behavior.

## Decision hypothesis

- Accepted kernel: dependency-aware decision frontier; facts versus decisions responsibility split; a recommended answer beside each material question; branch-local blocking while evidence is unresolved.
- Excluded machinery: exhaustive traversal for every design; mandatory multi-round interviewing; asking the whole frontier as a fixed response format; requiring shared-understanding confirmation before any action; a new `$soft-grill` wrapper or hidden cross-skill invocation topology.
- Landing plane: eval / maintainer first; possible narrow `brainstorm.md` clarification only after a reproduced local gap.
- Smallest useful delta: retain this candidate and design one shadow probe. Do not change runtime methods or start a live target-agent run in this intake.

## Probe

- Fixture or task: a design with decisions A, B, and C, where B depends on A, C is independent, and two relevant facts are available in the repository.
- Candidate behavior: inspect the facts independently; ask A and C in the first round with recommendations; ask B only after A is settled; do not block C while an A-dependent fact remains open.
- Baseline/control: a clear local copy or wiring change must proceed directly without a grilling session.
- Deterministic assertions: no question asks the user for repository facts; no downstream B question appears before A is settled; the control task creates no interview artifact.
- Semantic judgment: questions capture decisions that actually change behavior and do not reopen settled choices.
- Falsifier: current Softpowers already handles the dependency ordering consistently, or the added frontier language causes routine tasks to become interrogations.

## Verification if applied

- Search existing dogfood before creating a synthetic case.
- Start with one positive case and one clear-task negative control.
- Treat question ordering and relevance as human judgment unless a stable trace assertion is available.
- Use Skill Field Lab only when the behavior claim remains unresolved; no live run is authorized by this record.

## Result

`ADAPT` at the intake and probe plane. The source is genuinely useful but not a system-level reset for Softpowers: it makes a decision-topology invariant explicit where the current method is already close in spirit.

No runtime wording, new skill, installer change, dependency, or live evaluation is approved in this record.

Reopen when a comparable design session exposes premature downstream questions, when a representative dogfood trace becomes available, or when the upstream frontier mechanism changes materially.
