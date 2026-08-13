---
name: soft-debug
description: "Investigate and fix bugs, failing tests, regressions, build failures, or unexpected behavior using boundary localization, evidence, and bounded hypotheses. Use before speculative patching, especially for hidden-state or cross-component failures."
---

# Soft Debug

Find the causal mechanism, then fix it with the least risky change. Be systematic without forcing a four-phase ceremony onto an obvious compiler error.

A debug request restores the verified existing or requested contract. It does not authorize adjacent features, fallback systems, broad refactors, or extra infrastructure merely because they might make the system more robust.

## 1. Define the failure

Capture:

- Observed behavior
- Expected behavior
- The required outcome independent of the current implementation mechanism
- Reproduction path
- Environment or data conditions
- First known bad version or recent relevant changes, when available

Read the complete error, stack trace, failed assertion, logs, or browser console output. Do not summarize away the line that identifies the failing boundary.

If the failure is already precise and local, move directly to tracing it.

## 2. Reproduce or gather evidence

Prefer the cheapest reliable reproducer:

- A focused existing test
- A new regression test
- A minimal command or script
- A deterministic UI sequence
- A targeted log or state inspection

When the problem crosses components, inspect inputs and outputs at the boundaries. Add temporary instrumentation only where it distinguishes hypotheses. Remove it after the issue is understood unless it is useful production observability.

If reproduction is intermittent, record frequency and conditions. Avoid treating one successful run as proof.

## 3. Trace the cause

Trace bad state backward:

- Where is the incorrect value or transition first observable?
- Which caller, event, mutation, or external response produced it?
- What assumption changed?
- Is there a nearby working path to compare?
- Could several visible failures share one upstream cause?

For an unclear cross-boundary failure, sketch only the shortest relevant path. At each boundary, name the assumption about input shape, identity, version, configuration, state, ordering, availability, or output. Compare cheap boundary evidence with a known-good case when available, and stop at the first violated assumption. Do not map the whole architecture before inspecting the failing path.

State one active hypothesis:

> X is causing Y because evidence Z distinguishes it from the alternatives.

Test the smallest discriminating change or observation. Avoid changing several variables at once.

## Hypothesis budget

- One active hypothesis at a time.
- After a failed hypothesis, record what the result ruled out.
- After two failed hypotheses, reconsider the chosen boundary and hidden assumptions before broadening the search or adding another patch.
- If each fix exposes a new failure in another owner, transport, or state boundary, treat the cascade itself as architecture evidence and reset before applying another patch.
- Three materially different failed fixes are a hard stop for re-evaluating the mechanism, even when every individual patch is locally plausible.

This is a guard against thrashing, not a reason to stop at an arbitrary number when new evidence is strong.

Do not delegate a vague symptom. Delegate only after localization reveals distinct evidence questions, then verify returned claims against the primary artifacts.

## Reset the mechanism when patches multiply

Debugging does not require preserving an optional implementation choice. When fixes behave like whack-a-mole across components:

1. Stop patching and separate the required outcome from the currently chosen mechanism.
2. Sketch the shortest relevant topology: owners, transports, persistent state, trust boundaries, and the observed failure at each hop.
3. Verify the assumption that originally ruled out a simpler path using current source, runtime help, a bounded probe, or authoritative documentation.
4. Compare at least one direct supported route. Prefer it when it removes moving parts and still satisfies the full contract.
5. If the existing mechanism remains necessary, state the evidence that makes its additional boundaries unavoidable before resuming fixes.

Sunk implementation cost, passing component tests, or a fix for the latest symptom does not prove the topology is sound.

## 4. Fix the source

Prefer the narrowest change that restores the intended invariant.

- Fix the origin of invalid state rather than every downstream symptom.
- Avoid opportunistic refactors unless the current design prevents a safe fix.
- Add validation at boundaries when it prevents recurrence.
- Preserve compatibility unless the user approved a change.
- For an external or environmental cause, improve diagnostics or error handling first. Add retries or fallback behavior only when the observed failure and product contract justify them.

## 5. Prove the fix

Use a regression test when practical. Prefer strict red-green when the failure sharpens a behavior contract; use test-alongside when the change is mostly styling, configuration, or simple wiring.

Verify:

- The original reproducer now succeeds.
- The regression test fails against the old behavior when that can be demonstrated safely.
- Nearby behavior remains intact.
- Temporary diagnostics and experimental changes are removed.
- The final diff contains one understandable causal fix.

Before declaring the issue fixed, rerun the original reproducer after the final relevant edit, run the focused regression checks, and broaden verification when shared state, public contracts, data, security, or multiple consumers changed.

## Confidence labels

Use precise language:

- **Confirmed root cause:** direct evidence links cause to failure and the reproducer is fixed.
- **Probable cause:** evidence is strong but the environment prevents full reproduction.
- **Unknown:** investigation narrowed the space but did not establish causality.

Do not turn a probable explanation into a certainty.

## Avoid

- “It is probably X” followed immediately by a patch
- Re-running the same command without changing evidence
- Broad dependency upgrades as a first move
- Multiple unrelated fixes in one attempt
- Fixing a timeout with a longer arbitrary timeout when a condition can be observed
- Declaring a flaky issue solved after one passing run
