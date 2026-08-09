# Soft Verify

Evidence must support the exact claim. Fresh verification is required after the final relevant change, but verification scope should match risk rather than defaulting blindly to the largest test suite.

## Define the claims

List the claims that matter, such as:

- The original bug no longer reproduces.
- A new behavior matches acceptance criteria.
- Targeted tests pass.
- The module builds or type-checks.
- No existing behavior in the affected area regressed.
- A migration is safe.
- The branch is ready to integrate.

For each claim, identify the command, inspection, or manual scenario that proves it.

## Evidence budget

- Run a check only when its result supports a named claim or can change the next action.
- Do not calculate hashes without an identity or integrity decision that will use them.
- Do not rerun unchanged checks or add a second acceptance loop merely to restate existing proof.
- Stop when every material claim has proportionate fresh evidence; more commands do not automatically create more confidence.

## Verification ladder

### Level 1: Focused

Use for local, low-risk changes:

- Regression test
- Affected test file
- Component or module check
- Targeted type-check or lint
- Focused manual interaction

### Level 2: Adjacent

Add when the change touches shared code or several consumers:

- Package or feature suite
- Integration tests around the boundary
- Build for the affected application
- Representative platform or browser check

### Level 3: Broad

Use for high-risk or integration-ready changes:

- Full relevant test suite
- Full build
- Migration dry run
- End-to-end path
- Security or compatibility checks
- Multiple environments when the risk requires it

Do not run Level 3 merely to make a small change look rigorous. Do not stop at Level 1 when shared state, data, security, or public contracts are involved.

## Run and read

For every command:

1. Run it after the final relevant change.
2. Read the complete result needed to assess success.
3. Check exit status, failure counts, warnings, skipped tests, and environment limitations.
4. Record what it actually proves.
5. Do not extrapolate beyond that scope.

A prior run before later edits is stale evidence for the affected behavior.

## Non-test checks

Inspect:

- Final diff and scope
- Untracked or generated files
- Debug output and temporary instrumentation
- Secrets or sensitive data
- Schema and fixture consistency
- Documentation when public behavior or setup changed

For UI work, include a real rendered or interaction check when practical. Unit tests alone may not prove layout or input behavior.

## Regression evidence

For a bug fix, prefer a reproducer or test that would fail under the old behavior. Revert or mutation proof is useful when safe and efficient, but it is not mandatory when it would destabilize the workspace.

## Blocked verification

When a check cannot run:

- State the exact reason.
- Separate environmental failure from code failure.
- Run the strongest available alternative.
- Narrow the completion claim.
- Give the command or condition needed to complete verification later.

## Output format

Use three categories:

- **Verified:** claim and evidence
- **Failed:** actual failure and impact
- **Not verified:** omitted or blocked checks and why

Do not say “all tests pass” when only targeted tests ran. Say exactly which tests passed.
