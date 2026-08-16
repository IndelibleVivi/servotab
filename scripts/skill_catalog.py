#!/usr/bin/env python3
from __future__ import annotations

ROUTER = {
    "name": "softpowers",
    "description": (
        "Use for hands-on software repository work: implementation, debugging, "
        "refactoring, testing, code review, or repository-grounded architecture "
        "decisions. Silently choose a proportionate method, preserve the complete "
        "requested outcome, and keep clear local work direct. Do not use for general "
        "technical explanations, simple file lookup, casual discussion, repository "
        "license selection, or non-engineering writing."
    ),
    "display_name": "Softpowers",
    "short_description": "Quiet risk-scaled routing for repository work",
    "default_prompt": (
        "Use $softpowers to deliver the complete requested repository outcome with a "
        "proportionate engineering method and fresh, risk-matched verification."
    ),
    "implicit": True,
}

METHODS = (
    {
        "skill": "soft-brainstorm",
        "method": "brainstorm",
        "description": (
            "Turn a rough feature, product interaction, or architectural idea into a "
            "concrete design. Use when meaningful decisions are still open; avoid for "
            "already-clear local edits."
        ),
        "display_name": "Soft Brainstorm",
        "short_description": "Turn rough ideas into implementable designs",
        "default_prompt": (
            "Use $soft-brainstorm to inspect the current context, resolve the real "
            "design decisions, and recommend an implementable direction."
        ),
    },
    {
        "skill": "soft-spec-chain",
        "method": "spec-chain",
        "description": (
            "Preserve an approved specification through a complete implementation plan "
            "and execution. Use for major refactors, migrations, or multi-session work "
            "when a confirmed spec is the authority; cover the whole spec and make scope "
            "or order changes explicit. Avoid for ordinary work without an approved spec."
        ),
        "display_name": "Soft Spec Chain",
        "short_description": "Carry an approved spec through full implementation",
        "default_prompt": (
            "Use $soft-spec-chain to turn this approved specification into a complete "
            "implementation plan and preserve its scope through execution."
        ),
    },
    {
        "skill": "soft-plan",
        "method": "plan",
        "description": (
            "Create an implementation plan sized to the work. Use when requirements are "
            "sufficiently settled and a multi-step change benefits from sequencing, file "
            "targets, and explicit verification; when an approved spec governs, cover its "
            "complete accepted scope rather than substituting a phase plan."
        ),
        "display_name": "Soft Plan",
        "short_description": "Create a practical implementation plan",
        "default_prompt": (
            "Use $soft-plan to produce a concise, repository-grounded implementation "
            "plan sized to this change."
        ),
    },
    {
        "skill": "soft-execute",
        "method": "execute",
        "description": (
            "Execute an existing implementation plan or settled multi-step request with "
            "coherent batches, targeted checks, and controlled plan drift. Use when the "
            "design is already clear; preserve any approved spec as the scope and "
            "acceptance authority across all tranches."
        ),
        "display_name": "Soft Execute",
        "short_description": "Execute a settled plan in coherent slices",
        "default_prompt": (
            "Use $soft-execute to implement the settled request or plan, verify each "
            "meaningful slice, and finish without unnecessary process."
        ),
    },
    {
        "skill": "soft-debug",
        "method": "debug",
        "description": (
            "Investigate and fix bugs, failing tests, regressions, build failures, or "
            "unexpected behavior using boundary localization, evidence, and bounded "
            "hypotheses. Use before speculative patching, especially for hidden-state "
            "or cross-component failures."
        ),
        "display_name": "Soft Debug",
        "short_description": "Evidence-driven debugging with bounded hypotheses",
        "default_prompt": (
            "Use $soft-debug to reproduce this issue, identify the causal mechanism, "
            "implement the narrowest fix, and verify it."
        ),
    },
    {
        "skill": "soft-tdd",
        "method": "tdd",
        "description": (
            "Apply risk-based test-driven development. Use for bugs, domain logic, state "
            "transitions, parsers, contracts, migrations, and other behavior where a "
            "failing test sharpens the design or prevents regression."
        ),
        "display_name": "Soft TDD",
        "short_description": "Risk-based test-driven development",
        "default_prompt": (
            "Use $soft-tdd to choose the appropriate testing mode and implement this "
            "behavior with high-signal regression evidence."
        ),
    },
    {
        "skill": "soft-review",
        "method": "review",
        "description": (
            "Review a diff, commit, branch, PR, or implementation for actionable "
            "correctness and risk issues. Use when the user wants rigorous review without "
            "duplicate reviewer loops or invented findings."
        ),
        "display_name": "Soft Review",
        "short_description": "Actionable code review without invented findings",
        "default_prompt": (
            "Use $soft-review to inspect the requested diff or implementation and report "
            "only verified, actionable P0-P2 findings."
        ),
    },
    {
        "skill": "soft-receive-review",
        "method": "receive-review",
        "description": (
            "Evaluate and act on code review feedback with technical judgment. Use before "
            "applying external suggestions, especially when feedback is ambiguous, broad, "
            "or may conflict with repository constraints."
        ),
        "display_name": "Soft Receive Review",
        "short_description": "Evaluate review feedback before applying it",
        "default_prompt": (
            "Use $soft-receive-review to verify each review item against the repository, "
            "implement valid feedback, and push back where needed."
        ),
    },
    {
        "skill": "soft-verify",
        "method": "verify",
        "description": (
            "Verify code or product claims after changes using fresh, risk-matched "
            "evidence. Use before saying a bug is fixed, tests pass, requirements are met, "
            "or a branch is ready."
        ),
        "display_name": "Soft Verify",
        "short_description": "Fresh verification matched to risk",
        "default_prompt": (
            "Use $soft-verify to prove the relevant completion claims with fresh, "
            "appropriately scoped evidence."
        ),
    },
    {
        "skill": "soft-eval",
        "method": "eval",
        "description": (
            "Run reproducible Softpowers behavior evaluations with repository-owned "
            "canaries, JSONL traces, deterministic assertions, and evidence-bounded "
            "comparisons. Use explicitly for maintainer evals, release evidence, or "
            "investigating routing and workflow behavior; do not run model evals as a "
            "routine gate for ordinary repository work."
        ),
        "display_name": "Soft Eval",
        "short_description": "Run reproducible Softpowers behavior canaries",
        "default_prompt": (
            "Use $soft-eval to select the smallest relevant Softpowers canary set, run "
            "it with explicit identity and permissions, and report the saved evidence."
        ),
    },
    {
        "skill": "soft-worktree",
        "method": "worktree",
        "description": (
            "Create or use an isolated Git workspace when risk, duration, dirty state, or "
            "parallel writes justify it. Use explicitly for worktree setup; do not require "
            "isolation for every edit."
        ),
        "display_name": "Soft Worktree",
        "short_description": "Use Git isolation only when it adds value",
        "default_prompt": (
            "Use $soft-worktree to create or select a safe isolated workspace for this "
            "task and report its baseline state."
        ),
    },
    {
        "skill": "soft-parallel",
        "method": "parallel",
        "description": (
            "Delegate a small number of bounded engineering lanes to subagents when "
            "parallelism, context isolation, independent review, or coordinator attention "
            "materially improves the work. Use selectively; avoid for tiny or tightly "
            "coupled work."
        ),
        "display_name": "Soft Parallel",
        "short_description": "Delegate bounded worker lanes with explicit authority",
        "default_prompt": (
            "Use $soft-parallel to define bounded worker lanes, dispatch the fewest useful "
            "subagents with explicit authority and return contracts, and verify their "
            "results before integration."
        ),
    },
    {
        "skill": "soft-finish",
        "method": "finish",
        "description": (
            "Finish a development change safely: inspect the final tree, verify at the "
            "right scope, prepare commits or PRs when requested, and preserve or clean "
            "workspaces deliberately."
        ),
        "display_name": "Soft Finish",
        "short_description": "Verify and close a development change safely",
        "default_prompt": (
            "Use $soft-finish to inspect the final tree, run risk-matched checks, and "
            "perform only the requested Git or PR actions."
        ),
    },
)

PINNED_PROJECTIONS = (
    {
        "skill": "license-boundary",
        "manifest": "sources/license-boundary.json",
        "files": ("SKILL.md", "agents/openai.yaml", "LICENSE.txt", "NOTICE.md"),
        "implicit": True,
    },
)

METHOD_BY_SKILL = {entry["skill"]: entry["method"] for entry in METHODS}
SKILL_BY_METHOD = {entry["method"]: entry["skill"] for entry in METHODS}
SKILL_NAMES = (
    (ROUTER["name"],)
    + tuple(entry["skill"] for entry in METHODS)
    + tuple(entry["skill"] for entry in PINNED_PROJECTIONS)
)
METHOD_NAMES = tuple(entry["method"] for entry in METHODS)
REFERENCE_METHOD_NAMES = tuple(
    entry["method"] for entry in METHODS if entry.get("router_reference", True)
)
IMPLICIT_SKILL_NAMES = (ROUTER["name"],) + tuple(
    entry["skill"] for entry in METHODS if entry.get("implicit", False)
) + tuple(
    entry["skill"] for entry in PINNED_PROJECTIONS if entry.get("implicit", False)
)

# Canonical eval resources are projected into the installed soft-eval skill. The
# source paths remain the only authoring authority; skills/ is generated output.
BUNDLED_RESOURCE_FILES = (
    ("evals/run_behavior_evals.py", "soft-eval/scripts/run_behavior_evals.py"),
    ("evals/schemas/case.schema.json", "soft-eval/assets/schemas/case.schema.json"),
    ("evals/schemas/result.schema.json", "soft-eval/assets/schemas/result.schema.json"),
)

BUNDLED_RESOURCE_TREES = (
    ("evals/cases", "soft-eval/assets/cases"),
)
