#!/usr/bin/env python3
from __future__ import annotations

ROUTER = {
    "name": "servotab",
    "description": (
        "Use for hands-on repository work when a quiet, risk-scaled engineering method "
        "can improve design, implementation, debugging, review, delegation, or verification. "
        "Keep clear local changes direct, preserve the complete requested outcome, and add "
        "method only where risk or uncertainty justifies it. Do not use for general technical "
        "explanations, simple file lookup, casual discussion, or non-engineering writing."
    ),
    "display_name": "Servotab",
    "short_description": "Quiet, risk-scaled engineering methods",
    "default_prompt": (
        "Use $servotab to deliver the complete repository outcome with proportional method "
        "and fresh, risk-matched verification."
    ),
    "implicit": True,
}

METHODS = (
    {
        "skill": "design",
        "method": "design",
        "description": (
            "Turn a rough feature, product interaction, or architecture idea into a concrete "
            "design. Use when meaningful decisions remain open; avoid for already-clear local edits."
        ),
        "display_name": "Design",
        "short_description": "Turn rough ideas into implementable designs",
        "default_prompt": (
            "Use $design to inspect the current context, resolve the real design decisions, "
            "and recommend an implementable direction."
        ),
    },
    {
        "skill": "spec-chain",
        "method": "spec-chain",
        "description": (
            "Preserve an approved specification through a complete implementation plan and "
            "execution. Use for major refactors, migrations, or multi-session work when a "
            "confirmed spec is authoritative; keep scope and order changes explicit."
        ),
        "display_name": "Spec Chain",
        "short_description": "Carry an approved spec through implementation",
        "default_prompt": (
            "Use $spec-chain to turn this approved specification into a complete implementation "
            "plan and preserve its scope through execution."
        ),
    },
    {
        "skill": "plan",
        "method": "plan",
        "description": (
            "Create an implementation plan sized to settled work. Use when a multi-step change "
            "benefits from sequencing, file targets, and explicit verification."
        ),
        "display_name": "Plan",
        "short_description": "Create a practical implementation plan",
        "default_prompt": (
            "Use $plan to produce a concise, repository-grounded implementation plan sized "
            "to this change."
        ),
    },
    {
        "skill": "execute",
        "method": "execute",
        "description": (
            "Execute an existing implementation plan or settled multi-step request in coherent "
            "batches with targeted checks and controlled plan drift."
        ),
        "display_name": "Execute",
        "short_description": "Execute settled work in coherent slices",
        "default_prompt": (
            "Use $execute to implement the settled request or plan, verify each meaningful "
            "slice, and finish without unnecessary process."
        ),
    },
    {
        "skill": "debug",
        "method": "debug",
        "description": (
            "Investigate and fix bugs, failing tests, regressions, build failures, or unexpected "
            "behavior using boundary localization, evidence, and bounded hypotheses."
        ),
        "display_name": "Debug",
        "short_description": "Debug with bounded, evidence-driven hypotheses",
        "default_prompt": (
            "Use $debug to reproduce this issue, identify the causal mechanism, implement the "
            "narrowest fix, and verify it."
        ),
    },
    {
        "skill": "tdd",
        "method": "tdd",
        "description": (
            "Apply risk-based test-driven development to bugs, domain logic, state transitions, "
            "parsers, contracts, migrations, and behavior where a failing test sharpens the design."
        ),
        "display_name": "TDD",
        "short_description": "Risk-based test-driven development",
        "default_prompt": (
            "Use $tdd to choose the appropriate testing mode and implement this behavior with "
            "high-signal regression evidence."
        ),
    },
    {
        "skill": "review",
        "method": "review",
        "description": (
            "Review a diff, commit, branch, PR, or implementation for actionable correctness "
            "and risk issues without duplicate reviewer loops or invented findings."
        ),
        "display_name": "Review",
        "short_description": "Actionable review without invented findings",
        "default_prompt": (
            "Use $review to inspect the requested diff or implementation and report only "
            "verified, actionable P0-P2 findings."
        ),
    },
    {
        "skill": "review-feedback",
        "method": "review-feedback",
        "description": (
            "Evaluate and act on code-review feedback with technical judgment. Use before "
            "applying external suggestions, especially when feedback is ambiguous, broad, or "
            "may conflict with repository constraints."
        ),
        "display_name": "Review Feedback",
        "short_description": "Verify review feedback before applying it",
        "default_prompt": (
            "Use $review-feedback to verify each review item against the repository, implement "
            "valid feedback, and push back where needed."
        ),
    },
    {
        "skill": "verify",
        "method": "verify",
        "description": (
            "Verify code or product claims after changes using fresh, risk-matched evidence. "
            "Use before saying a bug is fixed, tests pass, requirements are met, or a branch is ready."
        ),
        "display_name": "Verify",
        "short_description": "Match fresh verification to actual risk",
        "default_prompt": (
            "Use $verify to prove the relevant completion claims with fresh, appropriately "
            "scoped evidence."
        ),
    },
    {
        "skill": "worktree",
        "method": "worktree",
        "description": (
            "Create or use an isolated Git workspace when risk, duration, dirty state, or "
            "parallel writes justify it. Do not require isolation for every edit."
        ),
        "display_name": "Worktree",
        "short_description": "Use Git isolation only when it adds value",
        "default_prompt": (
            "Use $worktree to create or select a safe isolated workspace for this task and "
            "report its baseline state."
        ),
    },
    {
        "skill": "delegate",
        "method": "delegate",
        "description": (
            "Delegate a small number of bounded engineering lanes when parallelism, clean "
            "context, independent review, or coordinator attention materially improves the work."
        ),
        "display_name": "Delegate",
        "short_description": "Delegate bounded lanes with explicit ownership",
        "default_prompt": (
            "Use $delegate to define bounded worker lanes, dispatch the fewest useful agents "
            "with explicit authority, and verify their returns before integration."
        ),
    },
    {
        "skill": "finish",
        "method": "finish",
        "description": (
            "Finish a development change safely by inspecting the final tree, verifying at the "
            "right scope, and performing only the requested Git or PR actions."
        ),
        "display_name": "Finish",
        "short_description": "Verify and close a development change safely",
        "default_prompt": (
            "Use $finish to inspect the final tree, run risk-matched checks, and perform only "
            "the requested Git or PR actions."
        ),
    },
)

METHOD_BY_SKILL = {entry["skill"]: entry["method"] for entry in METHODS}
SKILL_BY_METHOD = {entry["method"]: entry["skill"] for entry in METHODS}
SKILL_NAMES = (ROUTER["name"],) + tuple(entry["skill"] for entry in METHODS)
METHOD_NAMES = tuple(entry["method"] for entry in METHODS)
REFERENCE_METHOD_NAMES = tuple(
    entry["method"] for entry in METHODS if entry.get("router_reference", True)
)
IMPLICIT_SKILL_NAMES = (ROUTER["name"],) + tuple(
    entry["skill"] for entry in METHODS if entry.get("implicit", False)
)
