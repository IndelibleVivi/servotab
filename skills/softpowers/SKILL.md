---
name: softpowers
description: "Use for hands-on software repository work: implementation, debugging, refactoring, testing, code review, or repository-grounded architecture decisions. Silently choose the smallest useful method and keep clear local work direct. Do not use for general technical explanations, simple file lookup, casual discussion, or non-engineering writing."
---

# Softpowers

The user describes the work in ordinary language. Routing is your responsibility.

Use this skill quietly. Do not announce activation, a Quick/Deliberate/Deep label, or an internal playbook name unless that information materially helps the user.

## Default behavior

- Follow applicable user, repository, and global instructions before this workflow.
- Inspect the smallest repository context that can support a correct action.
- For clear, local, reversible work, proceed directly and read no reference.
- When the user asks for implementation, continue through implementation and verification. Stop at planning only when the user requested a plan or a material unresolved decision blocks safe progress.
- Ask only when a choice is destructive, irreversible, externally visible, or materially changes architecture and cannot be resolved from context. Otherwise state a safe assumption briefly and proceed.
- Do not create a worktree, design document, subagent, commit, push, PR, or merge merely because a method exists.
- Make completion claims only from fresh evidence gathered after the final relevant change.

## Progressive disclosure

1. Start with zero or one primary reference.
2. Before the first concrete action, read at most one supporting reference when it changes how the work should proceed.
3. Read another reference later only when the task genuinely enters a new phase or new evidence changes the problem.
4. Never preload a full lifecycle, reread the same reference, or read a reference just to appear rigorous.
5. References provide methods; they do not route to other references. Return here for every routing decision.
6. Keep simple tasks simple even when this router activates.

## Reference index

- Unsettled feature, interaction, or architecture decision: `references/brainstorm.md`
- Settled multi-step work that needs sequencing: `references/plan.md`
- Existing plan or clear multi-step implementation: `references/execute.md`
- Bug, failing test, regression, build failure, or unexplained behavior: `references/debug.md`
- Behavior where test-first work improves the contract: `references/tdd.md`
- Diff, commit, branch, PR, or implementation review: `references/review.md`
- External review feedback to validate and apply: `references/receive-review.md`
- Completion, readiness, or regression claims needing broader proof: `references/verify.md`
- Isolation justified by dirty state, risk, duration, or parallel writes: `references/worktree.md`
- At least two substantial and independent work domains: `references/parallel.md`
- Branch, PR, commit, cleanup, or final integration decisions: `references/finish.md`

## Hard gates

- Strict red-green is valuable for bugs, domain rules, state transitions, parsers, contracts, migrations, concurrency, and security-sensitive behavior. It is optional for styling, copy, simple wiring, or generated output.
- Parallel work requires independent domains, bounded context, non-overlapping writes or isolation, and enough benefit to repay token and integration cost. No nested subagents.
- One integrated review is the default. Do not manufacture findings or create duplicate reviewer loops.
- Verification scope follows blast radius: focused for local work, adjacent for shared code, broad for data, security, public contracts, migrations, or integration readiness.

## Minimum closure

For any code change, inspect the final diff, run the narrowest meaningful fresh check, broaden checks when risk justifies it, and report exactly what was verified or left unverified. Keep process narration out of the final report.
