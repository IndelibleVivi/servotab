# External Pattern Candidates

`evals/candidates/` 保存已经值得形成具体 decision sample 的外部 pattern。这里不承担 feature backlog。一个 candidate 可以结束于 `ADOPT`、`ADAPT`、`REJECT`、`DEFER` 或 `ALREADY COVERED`。

Raw model traces、private repositories、tokens、account state、个人路径与不能公开的 prompts 不进入 public tree。

## Candidate template

```markdown
# <Pattern name>

Status: PROPOSED | PROBING | DECIDED | APPLIED | SUPERSEDED
Decision: ADOPT | ADAPT | REJECT | DEFER | ALREADY COVERED

## Source

- Repository:
- Pinned ref:
- License:
- Reviewed files:
- Review date:

## Distilled pattern

<Remove project-specific branding and state the mechanism.>

## Local signal

<Observed Servotab failure, repeated friction, evidence gap, compatibility change, or concrete caller.>

## Existing coverage

<What current router, method, eval, packaging, or docs already provide.>

## Decision hypothesis

- Accepted kernel:
- Excluded machinery:
- Landing plane:
- Smallest useful delta:

## Probe

- Fixture or task:
- Candidate behavior:
- Baseline/control:
- Deterministic assertions:
- Semantic judgment:
- Falsifier:

## Verification if applied

- Fresh checks:
- Repeats:
- Adjacent controls:
- Blocked or unavailable evidence:

## Result

- Decision:
- Evidence:
- Remaining uncertainty:
- Reopen condition:
```

## Candidate discipline

- Pin before interpreting.
- Test the behavior claim, not the source project's vocabulary.
- Prefer `ALREADY COVERED` when current Servotab reaches the same outcome.
- Record rejected machinery explicitly.
- Apply to the lowest plane that solves the problem.
- Every code or method change receives fresh, blast-radius-matched verification.
- A docs-only decision normally does not consume model runs.
- Same-task success proves the repair; later comparable evidence supports broader improvement.
