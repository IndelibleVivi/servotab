#!/usr/bin/env python3
from __future__ import annotations

ROUTER = {
    "name": "softpowers",
    "description": (
        "Use for hands-on software repository work: implementation, debugging, "
        "refactoring, testing, code review, or repository-grounded architecture "
        "decisions. Silently choose the smallest useful method and keep clear local "
        "work direct. Do not use for general technical explanations, simple file "
        "lookup, casual discussion, or non-engineering writing."
    ),
    "display_name": "Softpowers",
    "short_description": "Quiet risk-scaled routing for repository work",
    "default_prompt": (
        "Use $softpowers to handle this repository task with the smallest useful "
        "engineering method and fresh, risk-matched verification."
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
        "skill": "soft-plan",
        "method": "plan",
        "description": (
            "Create an implementation plan sized to the work. Use when requirements are "
            "sufficiently settled and a multi-step change benefits from sequencing, file "
            "targets, and explicit verification."
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
            "design is already clear."
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
            "Delegate independent engineering domains to a small number of subagents when "
            "parallelism materially improves speed or context quality. Use selectively; "
            "avoid for tiny or tightly coupled work."
        ),
        "display_name": "Soft Parallel",
        "short_description": "Delegate only genuinely independent work",
        "default_prompt": (
            "Use $soft-parallel to identify independent domains, dispatch a small bounded "
            "set of subagents, and integrate their results safely."
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

METHOD_BY_SKILL = {entry["skill"]: entry["method"] for entry in METHODS}
SKILL_BY_METHOD = {entry["method"]: entry["skill"] for entry in METHODS}
SKILL_NAMES = (ROUTER["name"],) + tuple(entry["skill"] for entry in METHODS)
METHOD_NAMES = tuple(entry["method"] for entry in METHODS)
