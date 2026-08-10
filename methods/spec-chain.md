# Soft Spec Chain

Preserve an approved specification from planning through execution. The specification defines the required outcome and acceptance contract; the plan defines implementation order and technique.

## Authority

- Treat the accepted specification as the canonical authority for **what** must be implemented, **why** it exists, and **how completion is accepted**.
- An implementation plan for that specification must cover its entire accepted implementation scope.
- A phase, milestone, or current tranche may subdivide execution, but it may not replace the complete implementation plan or be presented as though it covers the whole specification.
- Keep explicit non-goals excluded. Keep unresolved decisions inside the full plan as decision-closing prerequisites or blockers; do not make them disappear by narrowing the plan.
- Preserve settled semantics such as naming, cardinality, ownership, compatibility, and migration behavior. Implementation convenience is not authority to reopen them.

## Establish the source contract

Before planning or editing, identify:

- Canonical specification path
- Accepted revision or commit
- Approval state and any named open decisions
- Repository baseline the specification was grounded against
- Current implementation state where it may have moved

Use a stable path plus revision or commit. Do not calculate a hash unless an actual identity or integrity decision needs it.

If several documents contribute requirements, name one primary specification and list the exact normative companions. Do not silently choose whichever document makes the next slice smaller.

## Build the complete implementation plan

Create one program-level plan over the full accepted scope.

1. Extract normative requirements, settled decisions, acceptance criteria, migrations, compatibility obligations, and retained non-goals.
2. Refer to existing IDs or headings instead of copying specification prose. When the specification lacks stable identifiers, create compact plan-local IDs tied to its headings.
3. Map every accepted requirement to an implementation slice and verification outcome.
4. Order slices by real dependencies. A different order from the specification is allowed only when the plan records the dependency rationale and preserves the same outcome.
5. Identify the current execution tranche without removing later slices from the program plan.
6. Include decision-closing work before any slice that depends on an unresolved product or destructive choice.

The plan may use several PRs, releases, or sessions. Full coverage does not require a mega-PR.

## Required plan contract

Keep the artifact compact, but include:

### Spec authority

- Canonical path and accepted revision
- Normative companion documents, if any
- Repository baseline and freshness note

### Complete coverage ledger

For each requirement or acceptance ID, record:

- Intended outcome
- Owning implementation slice
- Dependency or decision gate
- Verification evidence
- Status: `planned`, `blocked-decision`, `in-progress`, `implemented`, or `verified`

`planned` may be scheduled later. An accepted requirement cannot be marked out of scope merely because it is outside the current tranche.

### Dependency order

Show the full program sequence or dependency graph. Distinguish definition, enforcement, migration, activation, and deployment when the specification distinguishes them.

### Scope and order deltas

List every proposed `added`, `removed`, `narrowed`, or `reordered` item with:

- Affected specification IDs
- Reason and impact
- Whether it changes product meaning or only implementation technique
- Required decision owner

No entry means no delta. Never hide a scope change inside “minimal,” “first slice,” “later,” or “implementation detail.” Obtain explicit approval before adopting a product or acceptance delta.

### Execution tranches

Name the current tranche and its stopping point, then keep all later tranches visible. Label a tranche document `Execution Tranche`, not “the implementation plan for the specification.” Link it to the complete plan.

### Full acceptance

Define completion against the specification coverage ledger, not only the current tranche checklist.

## Execute without losing the specification

At execution entry, read:

- The accepted specification and normative companions
- The complete implementation plan
- The current execution tranche, when separate
- Current repository instructions and directly affected code/tests

Before editing, check that the plan still covers the complete accepted specification. If the only available artifact is a partial phase plan masquerading as the full plan, repair the planning artifact before relying on it.

During implementation:

- Adapt file paths, internal abstractions, and test mechanics when repository evidence supports the same contract.
- Record any scope, meaning, acceptance, or dependency change as an explicit delta before proceeding.
- Update the coverage ledger as evidence lands.
- Report tranche completion separately from full-spec completion.
- Keep implementation, merge, migration, deployment, and live-state activation as separate authorization gates.

Do not claim the specification is implemented until every accepted coverage item is implemented and verified at the appropriate risk level.

## Token discipline

- Link to specification anchors; do not restate the document.
- Maintain one coverage ledger instead of duplicating requirements across checklists.
- Record deltas only when they exist.
- Do not add separate reviewers, hashes, or ceremonial checkpoints by default.
- Automate coverage checks only when stable IDs and repeated use make the script cheaper than manual reconciliation.

## Regression guard

If a specification settles one public operation over a package of one or many items, a plan may not implement single-item behavior first and defer package cardinality unless the specification is explicitly amended. More generally, an easier subset is not an implementation plan for the whole contract.
