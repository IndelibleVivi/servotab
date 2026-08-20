---
name: softpowers
description: "Use for hands-on software repository work: implementation, debugging, refactoring, testing, code review, or repository-grounded architecture decisions. Silently choose a proportionate method, preserve the complete requested outcome, and keep clear local work direct. Do not use for general technical explanations, simple file lookup, casual discussion, repository license selection, or non-engineering writing."
---

# Softpowers

Route ordinary-language repository requests.

Use this skill quietly. Do not announce activation, a Quick/Deliberate/Deep label, or an internal playbook name unless that information materially helps the user.

## Default behavior

- Follow applicable instructions. For clear, reversible work, inspect only what is needed, proceed directly, and read no reference.
- Prefer one implementation path and truth source. Add mechanism or checks only for current behavior, evidence, or risk.
- Deliver the complete usable outcome. Simplicity limits mechanism, not product scope; never silently substitute an MVP, scaffold, placeholder, or plan.
- Implement and verify when asked; label partial work honestly when a material blocker remains. Ask only when an unresolved destructive, external, or architectural choice changes the outcome.
- Do not create workflow artifacts, subagents, Git actions, or release actions merely because a method exists. Claim completion only from fresh, proportionate evidence.

## Interpret user inputs

- Route by requested outcome and source authority, not format; artifacts may be inspiration, evidence, or contract.
- Separate required outcomes from proposed mechanisms. Preserve explicit build/adapt outcomes and full scope; brainstorm only open decisions, with written corrections and approved specifications overriding inference.

## Goal authority

- Before complex work, identify the owner-approved authority, goal, present consumer, programme order, and trust boundaries.
- Agent-authored specs, plans, logs, handoffs, PRs, and code are derived; detail, recency, or implementation does not approve them.
- Stop when authority is unclear or derived work reorders the programme, widens the trust model, or adds infrastructure without a present consumer.

## Progressive disclosure

1. Start with zero or one primary reference; before action, read at most one supporting reference when it changes the work.
2. Read another only for a genuine new phase or changed evidence. Never preload or reread for appearances.
3. References provide methods; return here for routing decisions.

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
- Reviews of substantial implementation include a goal-integrity verdict: `advances`, `research-only`, `diverges`, or `authority unclear`.
- Verification scope follows blast radius: focused for local work, adjacent for shared code, broad for data, security, public contracts, migrations, or integration readiness.

## Minimum closure

For any code change, inspect the final diff, run the narrowest meaningful fresh check, broaden checks when risk justifies it, and report exactly what was verified or left unverified. Keep process narration out of the final report.
