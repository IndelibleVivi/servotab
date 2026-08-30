export type Method = {
  name: string;
  purpose: string;
  signal: string;
};

export const methods: Method[] = [
  {
    name: "design",
    purpose:
      "Clarifies unsettled product, interaction, or architecture choices until implementation can proceed with confidence.",
    signal: "Use when a real decision is still open.",
  },
  {
    name: "spec-chain",
    purpose:
      "Carries an approved specification into a complete, traceable implementation plan without shrinking the accepted outcome.",
    signal: "Use when the specification is already authoritative.",
  },
  {
    name: "plan",
    purpose:
      "Structures settled multi-step work when no adopted specification already owns the complete plan.",
    signal: "Use when sequencing matters before edits begin.",
  },
  {
    name: "execute",
    purpose:
      "Turns a settled request or plan into working code through coherent, verified slices.",
    signal: "Use when the route is known and the work should move.",
  },
  {
    name: "debug",
    purpose:
      "Reproduces the failure, traces its causal mechanism, and restores the contract with focused evidence.",
    signal: "Use when behavior is wrong or unexplained.",
  },
  {
    name: "tdd",
    purpose:
      "Uses tests as design and evidence, with strict red-green discipline where it materially sharpens the contract.",
    signal: "Use for rules, state, parsers, regressions, and risky boundaries.",
  },
  {
    name: "review",
    purpose:
      "Inspects a diff or implementation for concrete, actionable defects against the real goal and repository truth.",
    signal: "Use when another pair of eyes should challenge the change.",
  },
  {
    name: "review-feedback",
    purpose:
      "Validates external review feedback against current source before applying a narrow, justified correction.",
    signal: "Use when feedback arrives from a reviewer or bot.",
  },
  {
    name: "verify",
    purpose:
      "Matches fresh evidence to the exact claim, broadening checks only when the blast radius requires it.",
    signal: "Use when readiness or completion needs proof.",
  },
  {
    name: "worktree",
    purpose:
      "Creates isolation when it reduces real risk while preserving ownership, existing work, and cleanup boundaries.",
    signal: "Use for long, risky, or concurrent repository work.",
  },
  {
    name: "delegate",
    purpose:
      "Splits genuinely independent work into bounded lanes with one writer per surface and an explicit return.",
    signal: "Use when parallelism repays its coordination cost.",
  },
  {
    name: "finish",
    purpose:
      "Closes the engineering loop with scoped validation, documentation truth, integration choices, and an honest handoff.",
    signal: "Use when the work must become safely resumable or ready to integrate.",
  },
];
