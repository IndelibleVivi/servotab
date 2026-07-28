---
name: soft-worktree
description: "Create or use an isolated Git workspace when risk, duration, dirty state, or parallel writes justify it. Use explicitly for worktree setup; do not require isolation for every edit."
---

# Soft Worktree

Use isolation when it reduces real risk. Respect the host environment and repository conventions.

## Use a worktree when

- The user asks for one.
- The current workspace has unrelated changes.
- The task is long-running or cross-cutting.
- Several write agents need isolated branches.
- The work may be abandoned or compared with another approach.
- A migration or risky refactor should remain easy to discard.

Work in place when:

- The change is small and local.
- The current branch is intentionally dedicated to the task.
- The host already provides isolation.
- Worktree setup would cost more than the risk it removes.

Direct explicit use of this playbook counts as a request for isolation unless the user says to inspect only.

## Detect current state

Check:

- Repository root
- Current branch or detached HEAD
- `git status --short`
- Whether `git-dir` differs from `git-common-dir`
- Whether the repository is a submodule
- Existing host-managed worktree state

Do not create a worktree inside an existing linked worktree unless the environment explicitly supports it.

## Prefer native isolation

Use the Codex or host worktree feature when available. It owns placement, cleanup, and UI state.

Use `git worktree` directly only when native isolation is unavailable or the user specifically requests manual Git handling.

## Manual worktree safety

When using Git directly:

1. Follow repository or user naming conventions.
2. Prefer an existing ignored `.worktrees/` or `worktrees/` directory.
3. Verify a project-local worktree directory is ignored before adding content.
4. Do not commit a `.gitignore` change solely for the workflow unless requested or clearly appropriate.
5. Use a descriptive branch name.
6. Confirm the target branch does not already exist in a conflicting state.
7. Record the full worktree path and branch.

If no safe project-local location exists, use a sibling or user-level worktree location that will not be committed.

## Setup

Run only necessary setup:

- Use the package manager implied by the lockfile.
- Reuse caches where supported.
- Do not reinstall all dependencies automatically when the workspace already has a valid setup.
- Run a focused baseline check that can distinguish pre-existing failures from new ones.
- Use a broader baseline for risky work when practical.

If the baseline fails, record the failure before editing. Continue only when it is unrelated and the task can still be verified honestly.

## Ownership and cleanup

Track whether the worktree is:

- Created by this workflow,
- Host-managed, or
- Pre-existing.

Only remove a worktree created by this workflow, and only after its branch is safely integrated or the user explicitly discards it.

Never delete a branch, uncommitted changes, or another worktree as incidental cleanup.

## Report

Provide:

- Worktree path
- Branch
- Baseline status
- Any setup performed
- Cleanup ownership
