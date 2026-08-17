---
name: softpowers
description: "Use for hands-on software repository work: implementation, debugging, refactoring, testing, code review, or repository-grounded architecture decisions. Silently choose a proportionate method, preserve the complete requested outcome, and keep clear local work direct. Do not use for general technical explanations, simple file lookup, casual discussion, repository license selection, or non-engineering writing."
---

# Softpowers

Route ordinary-language repository requests.

Use this skill quietly. Do not announce activation, a Quick/Deliberate/Deep label, or an internal playbook name unless that information materially helps the user.

## Default behavior

- Follow applicable user, repository, and global instructions before this workflow.
- For clear, local, reversible work, inspect only the repository context needed to act correctly, proceed directly, and read no reference.
- Prefer one implementation path and source of truth. Add abstractions, fallback, compatibility, dependencies, hashes, or checks only for current behavior, contract, evidence, or risk.
- Deliver the complete requested usable outcome and required integration. Simplicity limits mechanism, not product scope; never silently substitute an MVP, minimal slice, scaffold, placeholder, or plan.
- Implement and verify when asked. Stop at planning only when requested; otherwise label partial progress honestly if a material blocker prevents completion.
- Ask only when a destructive, irreversible, external, or architectural choice cannot be resolved from context. Otherwise state a safe assumption and proceed.
- Do not create a worktree, design document, subagent, commit, push, PR, or merge merely because a method exists.
- Make completion claims only from fresh, risk-matched evidence; do not repeat equivalent proof.

## Interpret user inputs

- Route by requested outcome and source authority, not format. Product descriptions, tutorials, screenshots, examples, logs, and reviews may be inspiration, evidence, or contract.
- Separate required outcomes from proposed mechanisms. Unless locked, verify assumptions and prefer the simplest supported path preserving full scope.
- Treat explicit build/adapt outcomes as settled, not every suggested mechanism. Brainstorm only open decisions; written corrections and approved specifications override inference.

## Progressive disclosure

1. Start with zero or one primary reference.
2. Before the first concrete action, read at most one supporting reference when it changes how the work should proceed.
3. Read another reference later only when the task genuinely enters a new phase or new evidence changes the problem.
4. Never preload a lifecycle, reread a reference, or read one for appearances.
5. References provide methods; return here for routing decisions.

## Reference index

- Unsettled feature, interaction, or architecture decision: `references/brainstorm.md`
- Approved spec needing complete planning or phased execution: `references/spec-chain.md` (prefer over plan/execute)
- Settled multi-step work without an approved spec: `references/plan.md`
- Existing plan or clear multi-step work without a spec chain: `references/execute.md`
- Bug, failing test, regression, build failure, or unexplained behavior: `references/debug.md`
- Behavior where test-first work improves the contract: `references/tdd.md`
- Diff, commit, branch, PR, or implementation review: `references/review.md`
- External review feedback to validate and apply: `references/receive-review.md`
- Completion, readiness, or regression claims needing broader proof: `references/verify.md`
- Isolation justified by dirty state, risk, duration, or parallel writes: `references/worktree.md`
- Bounded delegation where parallelism, context isolation, independent review, or coordinator attention materially helps: `references/parallel.md`
- Branch, PR, commit, cleanup, or final integration decisions: `references/finish.md`

## Hard gates

- Strict red-green is valuable for bugs, domain rules, state transitions, parsers, contracts, migrations, concurrency, and security-sensitive behavior. It is optional for styling, copy, simple wiring, or generated output.
- A plan for an approved spec covers it completely; a phase or tranche cannot substitute for the full plan.
- Debugging restores the verified contract without adding adjacent product scope or speculative machinery.
- Delegation requires a coherent bounded lane, explicit authority and return, one writer per overlapping surface, and enough benefit to repay coordination cost.
- One integrated review is the default. Do not manufacture findings or create duplicate reviewer loops.
- Verification scope follows blast radius: focused for local work, adjacent for shared code, broad for data, security, public contracts, migrations, or integration readiness.

## Minimum closure

For any code change, inspect the final diff, run the narrowest meaningful fresh check, broaden checks when risk justifies it, and report exactly what was verified or left unverified. Keep process narration out of the final report.
