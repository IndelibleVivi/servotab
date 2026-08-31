import debugIcon from "../../../assets/skill-icons/debug/icon.svg?url";
import delegateIcon from "../../../assets/skill-icons/delegate/icon.svg?url";
import designIcon from "../../../assets/skill-icons/design/icon.svg?url";
import executeIcon from "../../../assets/skill-icons/execute/icon.svg?url";
import finishIcon from "../../../assets/skill-icons/finish/icon.svg?url";
import planIcon from "../../../assets/skill-icons/plan/icon.svg?url";
import reviewFeedbackIcon from "../../../assets/skill-icons/review-feedback/icon.svg?url";
import reviewIcon from "../../../assets/skill-icons/review/icon.svg?url";
import specChainIcon from "../../../assets/skill-icons/spec-chain/icon.svg?url";
import tddIcon from "../../../assets/skill-icons/tdd/icon.svg?url";
import verifyIcon from "../../../assets/skill-icons/verify/icon.svg?url";
import worktreeIcon from "../../../assets/skill-icons/worktree/icon.svg?url";

export type Method = {
  name: string;
  icon: string;
  purpose: string;
  signal: string;
};

export const methods: Method[] = [
  {
    name: "design",
    icon: designIcon,
    purpose:
      "Clarifies unsettled product, interaction, or architecture choices until implementation can proceed with confidence.",
    signal: "Use when a real decision is still open.",
  },
  {
    name: "spec-chain",
    icon: specChainIcon,
    purpose:
      "Carries an approved specification into a complete, traceable implementation plan without shrinking the accepted outcome.",
    signal: "Use when the specification is already authoritative.",
  },
  {
    name: "plan",
    icon: planIcon,
    purpose:
      "Structures settled multi-step work when no adopted specification already owns the complete plan.",
    signal: "Use when sequencing matters before edits begin.",
  },
  {
    name: "execute",
    icon: executeIcon,
    purpose:
      "Turns a settled request or plan into working code through coherent, verified slices.",
    signal: "Use when the route is known and the work should move.",
  },
  {
    name: "debug",
    icon: debugIcon,
    purpose:
      "Reproduces the failure, traces its causal mechanism, and restores the contract with focused evidence.",
    signal: "Use when behavior is wrong or unexplained.",
  },
  {
    name: "tdd",
    icon: tddIcon,
    purpose:
      "Uses tests as design and evidence, with strict red-green discipline where it materially sharpens the contract.",
    signal: "Use for rules, state, parsers, regressions, and risky boundaries.",
  },
  {
    name: "review",
    icon: reviewIcon,
    purpose:
      "Inspects a diff or implementation for concrete, actionable defects against the real goal and repository truth.",
    signal: "Use when another pair of eyes should challenge the change.",
  },
  {
    name: "review-feedback",
    icon: reviewFeedbackIcon,
    purpose:
      "Validates external review feedback against current source before applying a narrow, justified correction.",
    signal: "Use when feedback arrives from a reviewer or bot.",
  },
  {
    name: "verify",
    icon: verifyIcon,
    purpose:
      "Matches fresh evidence to the exact claim, broadening checks only when the blast radius requires it.",
    signal: "Use when readiness or completion needs proof.",
  },
  {
    name: "worktree",
    icon: worktreeIcon,
    purpose:
      "Creates isolation when it reduces real risk while preserving ownership, existing work, and cleanup boundaries.",
    signal: "Use for long, risky, or concurrent repository work.",
  },
  {
    name: "delegate",
    icon: delegateIcon,
    purpose:
      "Splits genuinely independent work into bounded lanes with one writer per surface and an explicit return.",
    signal: "Use when parallelism repays its coordination cost.",
  },
  {
    name: "finish",
    icon: finishIcon,
    purpose:
      "Closes the engineering loop with scoped validation, documentation truth, integration choices, and an honest handoff.",
    signal: "Use when the work must become safely resumable or ready to integrate.",
  },
];
