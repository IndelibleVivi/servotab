# Soft Plan

Create a plan that helps implementation, review, and recovery. Avoid plans that are longer than the work or split one coherent change into dozens of mechanical steps.

## Inputs

Before planning, establish:

- The requested outcome and acceptance criteria
- Relevant repository instructions
- Current implementation and nearby patterns
- Known constraints or decisions
- Verification commands or test locations

Inspect enough code to name realistic touchpoints. Do not invent exact file paths when the repository does not support them.

## Approved specifications

When an approved specification governs the work:

- Treat it as the authority for scope, settled semantics, and acceptance.
- Make the implementation plan cover the complete accepted specification, even when execution will span phases, PRs, or sessions.
- Keep the current phase or tranche inside that full plan. Never present a partial tranche as the implementation plan for the specification.
- Map every normative requirement to a slice and verification outcome, and state every proposed scope or order delta explicitly.
- If the user explicitly requests only a tranche plan, label it `Execution Tranche` and link it to the existing complete plan. If no complete plan exists, establish it first.

Use compact specification IDs or heading anchors rather than repeating the source document.

## Choose plan depth

### Inline plan

Use for a moderate change that can be completed in the current session.

Provide three to seven coherent steps. Each step should produce a meaningful, testable increment.

### Durable plan

Use when:

- The work will span sessions,
- Several subsystems must coordinate,
- A migration or rollout exists,
- Another agent or developer may execute it, or
- The user explicitly requests a plan document.

Store it where the repository expects design or implementation plans. Do not create a new planning directory without checking local conventions.

## Plan structure

Include only what is useful:

1. **Goal and boundaries**
   - Intended behavior
   - Explicit non-goals
   - Material assumptions

2. **Implementation slices**
   - Outcome of the slice
   - Files or areas likely to change
   - Core logic or data-flow change
   - Tests or checks for that slice
   - Dependencies on earlier slices

3. **Cross-cutting concerns**
   - Compatibility or migration
   - Error handling
   - Security/privacy
   - Performance or concurrency
   - Rollback or feature flag, when applicable

4. **Acceptance verification**
   - Targeted tests
   - Broader checks justified by risk
   - Manual or visual verification where automation is not sufficient

## Granularity

A good task is independently understandable and verifiable. Prefer vertical slices over file-by-file chores.

Good:

- Add stale-cursor validation across backend mutation and pagination paths; cover it with regression tests.
- Introduce the new note artifact contract, update producers and consumers, then validate existing fixtures.

Weak:

- Open file A.
- Add import.
- Write ten lines.
- Run tests.
- Commit.

Do not include complete production code in a plan unless a subtle algorithm, schema, or protocol requires a precise example. Pseudocode and data shapes are usually enough.

## Plan review

Review the plan once against the requirements:

- Every acceptance criterion maps to a task or verification step.
- Every accepted specification requirement remains visible in the complete plan, including work scheduled after the current tranche.
- Dependencies are ordered correctly.
- Any narrowing, removal, deferral outside the plan, or reordering is an explicit specification delta rather than an implementation convenience.
- No hidden migration or compatibility issue is ignored.
- The plan does not add speculative infrastructure.
- The verification scope matches the risk.

Fix gaps directly. Do not dispatch a separate plan reviewer by default.

## Implementation handoff

When another agent or session will execute the plan, include:

- Current branch or workspace assumptions
- Commands needed to start
- Important files and repository guidance
- Known risks and stopping conditions
- Exact expected final report

Do not paste large source files into the plan.

## Exit behavior

- If the user asked for a plan only, stop after the plan.
- If the user asked for implementation, proceed into coherent, independently verifiable slices without waiting for ritual approval.
- Ask before proceeding only when the plan exposes an unresolved, material product or destructive decision.
