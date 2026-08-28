---
name: soft-finish
description: "Finish a development change safely: inspect the final tree, verify at the right scope, prepare commits or PRs when requested, and preserve or clean workspaces deliberately."
---

# Soft Finish

Close the work without turning completion into an automatic merge ritual.

## 1. Inspect final state

Check:

- Current branch and workspace type
- `git status --short`
- Final diff and diff statistics
- Untracked, generated, or temporary files
- Debug logging, TODOs, fixtures, snapshots, or local config accidentally changed
- Secrets or sensitive data
- Whether unrelated user changes are present
- The canonical active path and its callers, including any superseded helper, flag, test, or documentation claim left by the replacement

Do not modify or discard unrelated changes.

When replacement is complete, remove the superseded path in the same change. Retain compatibility only for an evidenced current caller or staged boundary, and name the reason and removal condition; an inert parallel implementation is not a rollback plan.

## 2. Check requirements

Map the final implementation to the requested behavior:

- Completed acceptance criteria
- Intentionally omitted items
- Plan deviations
- Alignment with the applicable authorized goal and current programme
- Compatibility or migration status
- Documentation or setup changes
- Remaining risks

Do this once. Do not reopen accepted design decisions without evidence. Treat implementation deviations as evidence to review, not as authority that settles product meaning. Before integration, require applicable approval for any change to programme order, trust boundaries, or accepted product scope.

## 3. Verify

Use a risk-matched verification ladder:

- Focused regression or behavior checks
- Adjacent suite or build for shared code
- Broad checks for integration, migration, security, or public contracts
- Manual or visual verification where relevant
- Fresh named-host acceptance after the final relevant deployment when the behavior is host-specific

Run checks after the final relevant edit. State exactly what passed and what was not run.

## 4. Review the diff

Perform a compact self-review for:

- Correctness
- Accidental scope
- Data/state consistency
- Error paths
- Compatibility
- Test value
- Avoidable complexity

For high-risk work, one independent reviewer can add value. Verify that reviewer’s findings yourself. Do not require duplicate reviewers for ordinary changes.

## 5. Documentation

Update durable documentation when the change affects:

- Public behavior or APIs
- Setup, configuration, or operations
- Data contracts or migrations
- Architecture decisions another person will need
- User-facing workflows

Do not add changelog noise for invisible local refactors unless repository policy requires it.

## 6. Git and integration

Only commit, push, merge, or create a PR when the user requests that action or applicable repository/global instructions delegate it.

When committing:

- Preserve unrelated user changes.
- Stage intentionally, not with blind `git add .`.
- Use focused commits when it improves review or rollback.
- Follow repository message conventions.

When preparing a PR:

- Identify the correct base branch.
- Summarize behavior and risk.
- Include verification evidence.
- Mention migrations, rollout, screenshots, or follow-up where relevant.

When work remains local, report the branch and workspace path.

## Destructive cleanup

Deleting a branch, worktree, uncommitted changes, generated data, or stash requires explicit confirmation. State what will be deleted. Clean only resources created for this task and owned by this workflow.

Host-managed worktrees should be left to the host unless it exposes an explicit cleanup action.

## Completion report

Provide:

- Result
- Main areas changed
- Verification and exact outcomes
- Git/PR state
- Remaining risk or blocked checks

Keep it compact and factual.
