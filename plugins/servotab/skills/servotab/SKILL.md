---
name: servotab
description: "Use for hands-on repository work when a quiet, risk-scaled engineering method can improve design, implementation, debugging, review, delegation, or verification. Keep clear local changes direct, preserve the complete requested outcome, and add method only where risk or uncertainty justifies it. Do not use for general technical explanations, simple file lookup, casual discussion, or non-engineering writing."
---

# Servotab

Use ordinary repository requests to select and apply engineering methods. The user need not name a skill. Keep communication quiet; keep the requested outcome complete.

## Before the first consequential action

- Read applicable instructions and the smallest relevant implementation, tests, and accepted contract. Establish the requested result, current behavior, and evidence needed to distinguish success from a plausible-looking patch.
- Size risk from the affected behavior, not confidence, file count, or patch size. Timers, shared state, persistence, recovery, generated artifacts, permissions, external calls, and public contracts can make a tiny edit consequential.
- Preserve explicit corrections and accepted scope. A newer plan, review, screenshot, generated artifact, or already-written code supplies evidence; it acquires authority only through the current request or repository contract.
- Keep clear local work direct. Do not create a plan, interview, search report, worktree, or delegation lane solely to demonstrate method use.

## Resolve decisions at their dependencies

When a material decision remains open, read `references/design.md` before committing to the dependent approach.

- Investigate repository and environmental facts yourself. Ask the user for intent or value choices that materially change the outcome and cannot safely be inferred.
- Ask only questions whose prerequisites are settled; include a grounded recommendation. Recompute dependent choices after an answer changes an assumption. An unresolved branch does not stop independent safe work.
- Use delegated reversible choices and explicit best-effort assumptions where authorized. Do not turn the absence of a prewritten design into a request for approval.
- Stop questioning when the current work is decision-ready. Do not exhaust unrelated future branches or reopen settled product decisions without contradictory evidence.

## Search before new common machinery

Before introducing a general-purpose helper, dependency, integration, transport, adapter, parser, validator, or fallback, inspect the existing repository path and installed dependencies or runtime first.

- Resolve any remaining capability question using relevant official documentation and maintained external implementations. Do not claim a platform limitation from old recollection alone.
- Search only channels that can change the decision. Stop when evidence supports reuse, extension, composition, or a justified custom implementation. A domain-specific requirement may warrant building directly after the local check.
- Report material unavailable coverage accurately. An unavailable channel does not establish that no solution exists.
- A reusable pattern can inform local code without becoming a dependency. Research results do not authorize installations, credentials, production calls, or a change to the accepted goal.

## Load methods at the action they govern

Read the applicable reference before its phase's first consequential action, including on a simple-looking task when its trigger is present. Reuse an unchanged reference already read in the available context; reload after context loss when needed. Combine complementary methods when the work crosses phases. No fixed full-stack workflow is required.

- Open feature, interaction, or architecture decisions: `references/design.md`
- Approved specification across planning and execution: `references/spec-chain.md`
- Settled multi-step work that needs sequencing: `references/plan.md`
- Existing plan or clear multi-step implementation: `references/execute.md`
- Bug, regression, failing test, or unexplained behavior: `references/debug.md`
- Contracts and behavior that benefit from test-first work: `references/tdd.md`
- Diff, commit, branch, PR, or implementation review: `references/review.md`
- External review feedback to validate and apply: `references/review-feedback.md`
- Completion and readiness claims needing fresh proof: `references/verify.md`
- Isolation justified by dirty state, risk, duration, or parallel writes: `references/worktree.md`
- Bounded worker lanes that materially improve the work: `references/delegate.md`
- Final integration, Git, PR, or cleanup decisions: `references/finish.md`

A bug requires investigation even when its eventual fix is one line. Review feedback requires adjudication before editing. An approved specification remains the whole acceptance contract when execution covers only one tranche. A user-requested planning-only or source-only boundary remains in force across method transitions.

If a needed reference is unavailable, use the applicable safeguards above, disclose only the material limitation, and continue safe work. Do not invent its contents or claim it was loaded.

## Preserve outcome and permission boundaries

- Choose the simplest mechanism that fulfills the complete accepted behavior, including its current consumers and integration. Do not silently replace the result with an MVP, placeholder, or backend-only slice.
- Evaluate a proposed mechanism independently while respecting user-selected meaning. Do not widen trust, change programme order, or introduce infrastructure with no present consumer.
- Keep the existing task record or complete plan current after a material correction. Preserve deferred scope and why it remains. Create a persistent record only when the work needs continuity; do not create a second tracker.
- Stop only at an unresolved authority boundary. Continue other safe, in-scope work. Research, file presence, reviewer advice, and test success confer no additional permission.
- Keep Git operations, deployment, publication, secret access, and paid or live-provider operations within their applicable authorization. No method grants them by itself.

## Choose evidence that could disprove the patch

- A meaningful check distinguishes the relevant failure from success. For a bug, use a reproducer that fails on the old behavior when this can be done safely in a disposable copy; do not revert unrelated live work.
- Inspect the failure families the change actually exposes. A timer needs repeated/interleaved activation; recovery needs interrupted or partial state; an input validator needs malformed inputs; UI motion needs its applicable accessibility behavior. Do not run every family for every edit.
- Do not weaken assertions, drop accepted scenarios, or edit only expected outputs to make a test green. Establish changed requirements before changing their oracle.
- After a check fails, distinguish patch regression, existing baseline failure, and environment failure. Repeated same-mechanism failures require a new causal investigation, not another cosmetic retry.
- When review findings arrive, resolve each material finding as fixed with evidence, rejected with evidence, or explicitly deferred under applicable authority. An open blocker cannot disappear behind a later summary or green CI.

## Close the actual claim

Inspect the final diff and run fresh, risk-matched verification after the last relevant edit. Broaden checks for affected shared consumers, data, security, or public contracts; keep bounded work bounded.

Separate delivered behavior, verified evidence, and remaining gaps. Package validity, installation, instruction delivery, successful use, deployment, and owner acceptance are distinct observations. A hash, checkbox, or configuration entry is not behavior proof.

A real failure may justify a local regression test or a reusable method change. Preserve a small, relevant observation and its causal limit; do not turn every incident into global policy or start an evaluation campaign without authorization.

These instructions guide model behavior. They do not enforce tool permissions or guarantee that the host selected this skill. Use repository tests and host-supported controls for boundaries that require deterministic enforcement.
