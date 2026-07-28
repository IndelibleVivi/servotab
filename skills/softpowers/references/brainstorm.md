# Soft Brainstorm

Develop the idea far enough that implementation can proceed confidently. Preserve exploration and design pressure without turning every request into a ceremony.

## Start with context

Inspect the smallest useful set of materials:

- Applicable `AGENTS.md`
- The current implementation path
- Nearby tests, schemas, or product documents
- Existing patterns that constrain the decision

Do not scan the whole repository unless the decision is truly cross-cutting.

## Reconstruct the problem

State, in compact form:

- Desired user or system outcome
- Current behavior
- Constraints and non-goals
- Decisions already made by the user
- Material unknowns

Treat the user's existing direction as real input. Do not reopen settled choices simply to manufacture alternatives.

## Explore the decision surface

Identify the few decisions that change implementation or product behavior. Common examples:

- State ownership
- Persistence and migration
- API or component boundaries
- Error and empty states
- Compatibility
- Rollout and reversibility
- Security or privacy boundaries

For each real decision:

1. Explain the tension.
2. Offer one recommended direction.
3. Include at most two alternatives when they are genuinely viable.
4. State the trade-off in concrete terms.

Do not provide three cosmetic variants merely to satisfy a format.

## Questions

Ask a question only when the answer:

- Changes externally visible behavior,
- Controls an irreversible or destructive choice,
- Selects between materially different architectures, or
- Cannot be inferred safely from the repository and prior discussion.

When useful, ask one focused question at a time during an interactive design conversation. When the user asked for a best-effort design or implementation, make explicit assumptions and continue.

## Produce a usable design

Scale the output.

For a local feature, a compact design may include:

- Behavior
- State/data flow
- Main implementation touchpoints
- Edge cases
- Verification

For a cross-cutting change, include:

- Goals and non-goals
- Proposed architecture
- Interfaces and ownership
- Data lifecycle or migration
- Failure handling
- Compatibility and rollout
- Testing strategy
- Open decisions

Use diagrams only when relationships are hard to express in prose.

## Stress-test the recommendation

Before finishing, check:

- What existing behavior could regress?
- What happens with stale, partial, duplicate, or missing data?
- What is the simplest path that still supports the real use case?
- Is the design creating infrastructure for an imagined future?
- Can the decision be reversed later?
- What evidence will show the implementation works?

Revise once. Do not create an endless self-review loop.

## Design documents

Write a persistent design document only when one of these applies:

- The user requests it.
- Multiple sessions or people will rely on it.
- The change alters architecture, public contracts, or stored data.
- The decision record will remain useful after implementation.

Otherwise keep the design inline.

## Exit behavior

- If the user asked only for brainstorming, stop with the recommendation and open decisions.
- If the user asked to implement, continue to a concise plan or direct implementation according to task size.
- Do not require a separate approval checkpoint when the recommended direction is already supported by the user's request and repository evidence.

## Avoid

- A mandatory interview before touching the problem
- Repeating the user's prompt as a long specification
- Reopening settled choices
- Designing every hypothetical future extension
- Treating a small UI adjustment as architecture
- Writing a design document solely to prove brainstorming occurred
