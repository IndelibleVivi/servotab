---
name: soft-parallel
description: "Delegate independent engineering domains to a small number of subagents when parallelism materially improves speed or context quality. Use selectively; avoid for tiny or tightly coupled work."
---

# Soft Parallel

Use subagents as a leverage tool, not a default unit of work. Each subagent consumes additional context, tool calls, and integration effort.

## Parallelism gate

Delegate only when all are true:

- There are at least two substantial work domains.
- The domains can be understood with bounded context.
- They have no critical sequential dependency.
- They will not edit the same state or files without isolation.
- Parallel work is likely to save meaningful time or keep noisy investigation out of the main context.

Good uses:

- Independent failing test groups with different likely causes
- Read-only exploration of separate subsystems
- One implementation stream plus one independent compatibility or security analysis
- Platform-specific investigations
- Distinct migration and frontend preparation with stable contracts

Poor uses:

- One small feature split into mechanical pieces
- Several symptoms likely caused by one upstream bug
- Tasks that require constant shared design decisions
- Multiple agents editing the same component
- Duplicate reviewers asked the same question
- Any workflow that spawns subagents merely because they are available

## Budget

Default limits:

- At most three subagents at once.
- No nested subagents.
- One independent review agent at most unless the user requests a review panel.
- Prefer read-heavy delegation over write-heavy delegation.
- The main agent remains integration owner.

Increase the limit only when the task has clearly independent domains and the user values speed over token cost.

## Define domains

Before dispatch, specify:

- Scope
- Goal
- Relevant files or commands
- Constraints and non-goals
- Whether writing is allowed
- Expected concise output
- Verification responsibility

Provide only the context each agent needs. Do not dump the entire conversation, plan, or repository.

## Write safety

For parallel writes, use one of:

- Separate worktrees or branches
- Non-overlapping file ownership
- A stable interface agreed before dispatch

If agents may touch the same files, keep the work sequential.

Subagents should not commit, push, merge, or change public contracts unless explicitly assigned.

## Result contract

Ask each subagent to return:

- What it inspected or changed
- Evidence and commands
- Files touched
- Remaining uncertainty
- Integration notes

Require concise summaries rather than raw logs.

## Integration

The main agent:

1. Verifies each result instead of trusting success claims.
2. Resolves conflicting assumptions.
3. Reviews the combined diff.
4. Runs integration-level checks.
5. Removes duplicate or incompatible changes.
6. Reports failures honestly.

Do not run a second subagent wave by default. Dispatch again only when the first results reveal a new independent domain that justifies the cost.
