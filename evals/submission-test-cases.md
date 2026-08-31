# OpenAI directory test-case draft

Status: prepared reviewer material for `0.4.0-rc1`. This document is not a
portal receipt, review result, submission claim, or publication claim.

These cases translate existing Servotab behavior fixtures into the compact
five-positive / three-negative format requested for directory review. The
positive cases preserve their checked-in fixture data and deterministic result
shape. The negative cases exercise the router's explicit exclusions and should
receive ordinary Codex help without activating Servotab.

## Positive cases

### 1. Keep a tiny repository edit direct

- **Prompt:** Change the empty-state copy in `app.txt` from `Nothing here` to
  `No saved items yet`. This is a tiny local edit. Make the change, run the
  narrowest meaningful verification, and do not change anything else.
- **Expected workflow:** The implicit `servotab` router recognizes a bounded
  repository change, keeps it on the direct path, and does not add a plan,
  subagent, or unrelated audit.
- **Expected result shape:** Only `app.txt` changes; its final value is
  `empty_state=No saved items yet`; `python3 check.py` passes.
- **Fixture data:** [`cases/tiny-copy/`](cases/tiny-copy/) contains the prompt,
  initial workspace, expected overlay, and command/workspace assertions.

### 2. Repair a causal regression at the shared invariant

- **Prompt:** Fix the stale-cursor regression in this repository. Reproduce the
  failing test, identify the violated consistency-window invariant, repair the
  canonical source without weakening or deleting tests, and run the focused
  regression suite. Keep the change scoped to the bug.
- **Expected workflow:** Servotab uses the debugging method, reproduces before
  editing, localizes the first violated invariant, and repairs the canonical
  implementation rather than weakening the test.
- **Expected result shape:** Only `cursor_window.py` changes;
  `python3 -m unittest -q` passes; the stale saved cursor is no longer returned
  across the invalid consistency-window boundary.
- **Fixture data:** [`cases/stale-cursor/`](cases/stale-cursor/) contains the
  failing implementation, regression test, expected repair, and assertions.

### 3. Preserve an approved specification through planning

- **Prompt:** `SPEC.md` is an approved specification and the complete scope
  authority. Inspect the repository and write `IMPLEMENTATION_PLAN.md`; do not
  implement the product yet. The plan must cover every requirement, preserve
  dependency order, name concrete file and verification targets, and distinguish
  execution tranches from full-spec completion.
- **Expected workflow:** Servotab routes through `spec-chain`, treats the
  approved specification as authority, and does not silently replace it with a
  convenient first tranche.
- **Expected result shape:** Only `IMPLEMENTATION_PLAN.md` is created; it maps
  `REQ-001` through `REQ-005`, preserves dependency order, and separates tranche
  completion from full-spec completion.
- **Fixture data:** [`cases/spec-chain/`](cases/spec-chain/) contains the
  approved specification, supporting source, expected plan, and assertions.

### 4. Review only what the evidence supports

- **Prompt:** Review the four bounded proposed changes in `REVIEW_CASES.md`
  against their accepted contracts. Write a report-only result to `REVIEW.md`;
  do not implement fixes or change `REVIEW_CASES.md`. For each case, use exactly
  one leading disposition line in the form `SR-XX: DISPOSITION`, choosing
  `CLEAN`, `FINDING`, or `CONDITIONAL` from the evidence. When a production
  trigger is unobserved, distinguish that uncertainty from the concrete code
  path and impact if the condition occurs.
- **Expected workflow:** Servotab uses `review`, protects the clean control,
  reports verified findings, and labels the unobserved production trigger as a
  conditional rather than inventing certainty.
- **Expected result shape:** Only `REVIEW.md` changes, with the four exact
  disposition lines and concise supporting evidence; no repair or repo-wide
  audit is performed.
- **Fixture data:** [`cases/review-evidence-boundaries/`](cases/review-evidence-boundaries/)
  contains the bounded review corpus, expected report, and assertions.

### 5. Add one bounded seam for a missing host reproducer

- **Prompt:** `SYSTEM.md` describes a repository whose focused contract tests
  are green, but an embedded-host capability failure can only be reproduced
  after production deployment. Establish the cheapest local executable seam for
  the documented host capability envelope, use it to reproduce and fix the
  route-selection defect, and run focused proof. Update `embedded_app.py`,
  implement `host_surrogate.py`, add `test_host_surrogate.py`, and record the
  three-layer boundary in `TEST_TOPOLOGY.md`; keep every other file unchanged.
- **Expected workflow:** Servotab uses debugging and TDD guidance to add one
  local host surrogate, avoids cloning the production host or building a general
  framework, and keeps named-host acceptance separate.
- **Expected result shape:** Exactly the four named files change; the two focused
  Python probes and `python3 -m unittest -q` pass; `TEST_TOPOLOGY.md` explicitly
  says local success does not prove production acceptance.
- **Fixture data:** [`cases/missing-host-test-seam/`](cases/missing-host-test-seam/)
  contains the system contract, initial implementation, expected four-file
  overlay, and assertions.

## Negative cases

### 1. General Git explanation without repository work

- **Prompt / scenario:** Explain rebase versus merge in two short paragraphs for
  a beginner. Do not inspect or edit a repository.
- **Expected fallback:** Codex answers directly using ordinary explanatory
  assistance. Servotab does not activate and does not introduce a repository
  workflow, plan, or verification ritual.
- **Why Servotab should not complete it:** This is general conceptual
  explanation, an explicit router exclusion, with no repository outcome.

### 2. Simple file lookup

- **Prompt / scenario:** Find the file that defines `SITE.origin` and return only
  its path. Do not edit anything.
- **Expected fallback:** Codex performs the smallest file search and returns the
  path only. Servotab does not activate or add method overhead.
- **Why Servotab should not complete it:** A simple file lookup is explicitly
  outside the router's activation boundary.

### 3. Non-engineering prose rewrite

- **Prompt / scenario:** Rewrite this personal paragraph so it feels warmer and
  more concise. It is not technical documentation and there is no repository
  task.
- **Expected fallback:** Codex provides the requested prose rewrite using
  ordinary writing assistance. Servotab does not activate.
- **Why Servotab should not complete it:** The request is non-engineering
  writing and has no repository implementation, debugging, review, or
  verification need.

## Use boundary

Before portal entry, recheck these cases against the exact final bundle and the
current submission form. Portal execution, identity selection, availability,
attestations, review, and publication remain separate owner-controlled steps.
