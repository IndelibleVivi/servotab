#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from skill_catalog import METHODS, ROUTER

ROOT = Path(__file__).resolve().parents[1]
METHODS_DIR = ROOT / "methods"
SKILLS_DIR = ROOT / "skills"

ROUTER_BODY = """# Softpowers

Route ordinary-language repository requests.

Use this skill quietly. Do not announce activation, a Quick/Deliberate/Deep label, or an internal playbook name unless that information materially helps the user.

## Default behavior

- Follow applicable user, repository, and global instructions before this workflow.
- For clear, local, reversible work, inspect only the repository context needed to act correctly, proceed directly, and read no reference.
- Prefer one implementation path and source of truth. Add abstractions, fallback, compatibility, dependencies, hashes, or checks only for current behavior, contract, evidence, or risk.
- Deliver the complete requested usable outcome and required integration. Simplicity limits mechanism, not product scope; never silently substitute an MVP, minimal slice, scaffold, placeholder, or plan.
- Implement and verify when asked. Stop at planning only when requested; otherwise label partial progress honestly if a material blocker prevents completion.
- Ask only when a destructive, irreversible, external, or architectural choice cannot be resolved from context. Otherwise state a safe assumption and proceed.
- Do not create a worktree, design document, subagent, commit, push, PR, or merge merely because a method exists.
- Make completion claims only from fresh, risk-matched evidence; do not repeat equivalent proof.

## Interpret user inputs

- Route by requested outcome and source authority, not format. Product descriptions, tutorials, screenshots, examples, logs, and reviews may be inspiration, evidence, or contract.
- Separate required outcomes from proposed mechanisms. Unless locked, verify assumptions and prefer the simplest supported path preserving full scope.
- Treat explicit build/adapt outcomes as settled, not every suggested mechanism. Brainstorm only open decisions; written corrections and approved specifications override inference.

## Progressive disclosure

1. Start with zero or one primary reference.
2. Before the first concrete action, read at most one supporting reference when it changes how the work should proceed.
3. Read another reference later only when the task genuinely enters a new phase or new evidence changes the problem.
4. Never preload a lifecycle, reread a reference, or read one for appearances.
5. References provide methods; return here for routing decisions.

## Reference index

- Unsettled feature, interaction, or architecture decision: `references/brainstorm.md`
- Approved spec needing complete planning or phased execution: `references/spec-chain.md` (prefer over plan/execute)
- Settled multi-step work without an approved spec: `references/plan.md`
- Existing plan or clear multi-step work without a spec chain: `references/execute.md`
- Bug, failing test, regression, build failure, or unexplained behavior: `references/debug.md`
- Behavior where test-first work improves the contract: `references/tdd.md`
- Diff, commit, branch, PR, or implementation review: `references/review.md`
- External review feedback to validate and apply: `references/receive-review.md`
- Completion, readiness, or regression claims needing broader proof: `references/verify.md`
- Isolation justified by dirty state, risk, duration, or parallel writes: `references/worktree.md`
- Bounded delegation where parallelism, context isolation, independent review, or coordinator attention materially helps: `references/parallel.md`
- Branch, PR, commit, cleanup, or final integration decisions: `references/finish.md`

## Hard gates

- Strict red-green is valuable for bugs, domain rules, state transitions, parsers, contracts, migrations, concurrency, and security-sensitive behavior. It is optional for styling, copy, simple wiring, or generated output.
- A plan for an approved spec covers it completely; a phase or tranche cannot substitute for the full plan.
- Debugging restores the verified contract without adding adjacent product scope or speculative machinery.
- Delegation requires a coherent bounded lane, explicit authority and return, one writer per overlapping surface, and enough benefit to repay coordination cost.
- One integrated review is the default. Do not manufacture findings or create duplicate reviewer loops.
- Verification scope follows blast radius: focused for local work, adjacent for shared code, broad for data, security, public contracts, migrations, or integration readiness.

## Minimum closure

For any code change, inspect the final diff, run the narrowest meaningful fresh check, broaden checks when risk justifies it, and report exactly what was verified or left unverified. Keep process narration out of the final report.
"""


def q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def frontmatter(name: str, description: str) -> str:
    return f"---\nname: {name}\ndescription: {q(description)}\n---\n\n"


def openai_yaml(entry: dict[str, object], *, implicit: bool) -> str:
    return (
        "interface:\n"
        f"  display_name: {q(str(entry['display_name']))}\n"
        f"  short_description: {q(str(entry['short_description']))}\n"
        f"  default_prompt: {q(str(entry['default_prompt']))}\n"
        "policy:\n"
        "  products:\n"
        "    - CODEX\n"
        f"  allow_implicit_invocation: {'true' if implicit else 'false'}\n"
    )


def expected_files() -> dict[Path, str]:
    files: dict[Path, str] = {}
    router_dir = SKILLS_DIR / str(ROUTER["name"])
    files[router_dir / "SKILL.md"] = frontmatter(
        str(ROUTER["name"]), str(ROUTER["description"])
    ) + ROUTER_BODY
    files[router_dir / "agents" / "openai.yaml"] = openai_yaml(ROUTER, implicit=True)

    for entry in METHODS:
        method_name = str(entry["method"])
        method_path = METHODS_DIR / f"{method_name}.md"
        method_body = method_path.read_text(encoding="utf-8")
        if not method_body.endswith("\n"):
            method_body += "\n"
        if entry.get("router_reference", True):
            files[router_dir / "references" / f"{method_name}.md"] = method_body

        skill_dir = SKILLS_DIR / str(entry["skill"])
        files[skill_dir / "SKILL.md"] = frontmatter(
            str(entry["skill"]), str(entry["description"])
        ) + method_body
        files[skill_dir / "agents" / "openai.yaml"] = openai_yaml(
            entry, implicit=bool(entry.get("implicit", False))
        )

    return files


def check() -> list[str]:
    errors: list[str] = []
    expected = expected_files()
    for path, content in expected.items():
        if not path.is_file():
            errors.append(f"missing generated file: {path.relative_to(ROOT)}")
            continue
        current = path.read_text(encoding="utf-8")
        if current != content:
            errors.append(f"generated file is stale: {path.relative_to(ROOT)}")

    allowed = {path.resolve() for path in expected}
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        for item in skill_dir.rglob("*"):
            if item.is_file() and item.resolve() not in allowed:
                errors.append(f"unexpected generated payload file: {item.relative_to(ROOT)}")
    return errors


def write() -> None:
    expected = expected_files()
    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    allowed = {path.resolve() for path in expected}
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        for item in sorted(skill_dir.rglob("*"), reverse=True):
            if item.is_file() and item.resolve() not in allowed:
                item.unlink()
            elif item.is_dir() and not any(item.iterdir()):
                item.rmdir()
        if not any(skill_dir.iterdir()):
            skill_dir.rmdir()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate the implicit router, references, and explicit leaf skills from methods/."
    )
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale")
    args = parser.parse_args()

    if args.check:
        errors = check()
        if errors:
            print("Softpowers generated-skill sync failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("Generated router, references, and leaf skills match canonical methods.")
        return 0

    write()
    reference_count = sum(bool(entry.get("router_reference", True)) for entry in METHODS)
    explicit_leaf_count = len(METHODS)
    print(
        f"Generated router, {reference_count} router references, "
        f"and {explicit_leaf_count} explicit leaf skills."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
