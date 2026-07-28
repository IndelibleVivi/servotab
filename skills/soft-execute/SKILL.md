---
name: soft-execute
description: "Execute an existing implementation plan or settled multi-step request with coherent batches, targeted checks, and controlled plan drift. Use when the design is already clear."
---

# Soft Execute

Turn a settled plan into working code. Preserve momentum while maintaining evidence and scope control.

## Load and sanity-check

Read:

- Applicable repository instructions
- The plan or settled request
- Files and tests directly named by it
- Any referenced schema or contract

Perform one sanity check before editing:

- Does the plan conflict with the current repository?
- Is a dependency missing?
- Would it cause data loss, a security regression, or a public compatibility break?
- Has the requested behavior already been implemented differently?

Correct small stale details yourself. Surface a concern only when it changes the approach materially.

## Execute in coherent slices

For each slice:

1. Mark the intended outcome.
2. Inspect the relevant implementation and existing tests.
3. Make the smallest coherent change that achieves the outcome.
4. Add or update high-value tests.
5. Run focused verification.
6. Inspect the resulting diff before moving on.

A slice may span several files. Do not create one task per file or one subagent per checklist item.

## Plan drift

Use judgment when reality differs from the plan.

Proceed and note the adjustment when:

- A file moved,
- An existing abstraction already solves part of the problem,
- A test requires a nearby fixture update,
- A smaller implementation satisfies the same contract.

Pause or explicitly flag the choice when:

- User-visible behavior changes,
- A public API or schema must differ,
- Data migration becomes necessary,
- Security or privacy assumptions change,
- The plan's central architecture is invalid.

When a safe reversible choice exists, take it and continue.

## Testing

Use strict red-green where a failing test clarifies the contract, especially for bugs, domain logic, state transitions, parsers, migrations, concurrency, or security-sensitive behavior. Use characterization-first for unclear legacy behavior and test-alongside for styling, copy, simple configuration, or low-risk wiring. Existing valid code does not need to be deleted because the test came later.

At minimum:

- Reproduce bugs with a regression test when practical.
- Test domain logic, state transitions, parsers, and contracts.
- Use visual/manual checks for styling and interaction where unit tests add little value.
- Keep mocks at stable boundaries.

## Delegation

Stay in the main agent by default.

Delegate only when there are genuinely independent domains with enough work to outweigh token, context, and integration cost. Keep the main agent as integration owner. Do not:

- Spawn a fresh implementer for every task,
- Add separate spec and quality reviewers after every slice,
- Nest subagents,
- Delegate tightly coupled writes to the same files.

## Checkpoints

Give the user an update when:

- A meaningful slice is complete,
- A material issue changes the plan,
- A root cause or hidden constraint is discovered.

Do not ask “continue?” after routine milestones. Continue until completion, a real blocker, or the requested stopping point.

## Failure handling

If focused verification fails:

1. Read the full failure.
2. Decide whether it is caused by the current slice, an existing baseline issue, or the environment.
3. Fix current-slice regressions before proceeding.
4. When the cause is uncertain, stop speculative implementation and switch to evidence-driven debugging with one active hypothesis.
5. Do not stack speculative fixes.

After two failed attempts based on the same idea, reset the hypothesis instead of adding another patch.

## Completion

After all slices:

- Review the combined diff for scope and accidental changes.
- Run fresh verification at a scope justified by risk: focused checks for local changes, adjacent checks for shared code, and broad checks for migrations, security, public contracts, or integration readiness.
- Update documentation only when behavior, interfaces, setup, or durable decisions changed.
- Do not commit, push, merge, or open a PR unless the user requests it or applicable repository/global instructions delegate it.

Report actual results, including checks not run.
