---
name: delegate
description: "Delegate a small number of bounded engineering lanes when parallelism, clean context, independent review, or coordinator attention materially improves the work."
---

# Delegate

Use worker lanes to move bounded responsibility into clean agent contexts without confusing delegation with permission. Use the fewest work surfaces that materially improve the outcome.

## Capability and routing boundary

- The host and current instructions decide whether subagent tools exist, how much concurrency is available, and whether delegation is permitted. Servotab cannot create or override that capability.
- Select this method from task topology: independent substantial lanes, one noisy responsibility that benefits from clean context, distinct evidence questions after localization, or a genuinely useful independent review. Model or reasoning tier, idle slots, and a harness-initiated spawn are not evidence that this method was selected.
- In ordinary-language work, the implicit `servotab` router reads this reference and applies its contract. The explicit `delegate` leaf is a manual entry point; its name need not appear in the UI for the method to govern a delegation.
- If delegation is unavailable or forbidden, keep the same ownership boundaries while sequencing the work locally. Do not claim a parallel execution that did not occur.

## Responsibility model

- The **Requester** sets the objective and grants authority.
- The current user-facing agent is the **Coordinator**. It decomposes the outcome, protects boundaries, remains the integration owner, and accepts or rejects returns.
- A **Task Worker** owns one coherent engineering, research, audit, validation, or review lane and makes ordinary in-scope decisions.
- An optional **Helper** handles one narrow temporary subtask for a worker when the platform, current instructions, and work order allow it. It returns only to that worker and never declares the whole task complete.

These are responsibilities, not ranks. A fresh context is a clean workbench; it creates neither a new objective nor new permission. Keep the main conversation as the coordination and judgment surface rather than replacing it with a worker dashboard.

## Delegation gate

When delegation is available, use a lane when at least one brings material value:

- Two or more substantial domains can proceed independently.
- A noisy research or long-running responsibility benefits from clean context.
- An independent review would add genuinely different evidence.
- The Coordinator's context or attention is becoming too full for clean judgment.
- Parallel work saves meaningful time without write collisions.

Keep the work in the Coordinator when it is small, reversible, tightly coupled, driven by one likely common cause, or easier to finish directly. Do not split one feature by file, create duplicate reviewers, or spawn workers merely because they are available.

Use at most three concurrent Task Workers by default. Add a Helper only when it is cheaper than finishing the subtask directly; permit at most one helper edge and no delegation tree. One independent review lane is normally enough.

## Work-order contract

Give every Task Worker a compact order with:

- **Outcome:** the concrete result and completion condition for this lane.
- **Scope:** included files, systems, questions, and explicit exclusions.
- **Context:** the smallest canonical sources and known current facts needed to begin.
- **Authority:** allowed reads, writes, tool side effects, external actions, approval gates, and stop conditions.
- **Return:** destination, required evidence, unknowns, changed surfaces, and concise report shape.

The order must support independent judgment without hidden parent context. Delegation changes where authorized work happens, not what may happen. An instruction such as “if needed,” “if safe,” or “after approval” remains a gate. A worker that needs broader scope or authority stops the affected path and returns the exact conflict plus the smallest proposed correction.

Keep the order proportional: normally one to three bullets per field. Link canonical sources instead of restating whole plans or global rules, and include a constraint only when this lane needs it to judge or act correctly. A work order is not a second specification.

Before dispatch, the Coordinator checks that outcome, acceptance criteria, dependencies, authority, stop conditions, writer ownership, and return evidence are compatible. Ask the worker to validate that chain at entry, then make normal in-scope decisions without escalating trivia.

## Dispatch and write ownership

Create each lane once. If creation returns an error, timeout, or ambiguous result, inspect existing agents once before retrying; an error does not prove that no worker exists.

Keep one writer for every overlapping file, branch, database, or live-state surface. For concurrent writes, use non-overlapping ownership, separate worktrees or branches, or a stable interface fixed before dispatch. Otherwise sequence the work. Workers do not commit, push, merge, deploy, mutate production, or change public contracts unless the order explicitly grants that action.

After confirmed dispatch, continue a non-overlapping Coordinator responsibility or wait. Do not repeatedly poll healthy workers; resume on an explicit return, a concrete delivery problem, or a user status request.

## Return packet

Require one explicit return containing:

- Outcome and completion status
- Changed or inspected surfaces
- Evidence and verification
- Unknown or unverified items
- Risks or blockers
- Recommended next action

Treat the packet as claims, not proof. The Coordinator checks source evidence, authority compliance, acceptance criteria, unknowns, and the combined diff or runtime state before integration. Resolve conflicting assumptions and run the narrowest meaningful integration check.

Do not run another worker wave by default. Dispatch again only when returned evidence reveals a new bounded responsibility whose value repays the coordination cost.
