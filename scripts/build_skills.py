#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from skill_catalog import (
    BUNDLED_RESOURCE_FILES,
    BUNDLED_RESOURCE_TREES,
    METHODS,
    PINNED_PROJECTIONS,
    ROUTER,
)

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
- Softpowers behavior evals or release evidence: `references/eval.md`
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


def pinned_projection_status(
    *,
    root: Path = ROOT,
    skills_dir: Path = SKILLS_DIR,
) -> tuple[set[Path], list[str]]:
    targets: set[Path] = set()
    errors: list[str] = []

    for entry in PINNED_PROJECTIONS:
        skill = str(entry["skill"])
        required_files = {str(relative) for relative in entry["files"]}
        manifest_path = root / str(entry["manifest"])
        label = f"pinned projection {skill}"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if set(manifest) != {"schema_version", "skill", "source", "files"}:
                raise ValueError("invalid manifest fields")
            if manifest["schema_version"] != 1 or manifest["skill"] != skill:
                raise ValueError("invalid schema version or skill identity")

            source = manifest["source"]
            if not isinstance(source, dict) or set(source) != {
                "repository",
                "ref",
                "commit",
                "path",
            }:
                raise ValueError("invalid source identity")
            if any(not isinstance(source[field], str) for field in source):
                raise ValueError("source identity fields must be strings")
            if not source["repository"].startswith("https://github.com/"):
                raise ValueError("source repository must be a GitHub URL")
            if not source["ref"] or not source["path"]:
                raise ValueError("source ref and path must be non-empty")
            commit = source["commit"]
            if len(commit) != 40 or any(char not in "0123456789abcdef" for char in commit):
                raise ValueError("source commit must be a lowercase full SHA")
            source_path = Path(source["path"])
            if source_path.is_absolute() or ".." in source_path.parts:
                raise ValueError("source path must be repository-relative")

            files = manifest["files"]
            if not isinstance(files, list) or any(
                not isinstance(item, dict) or set(item) != {"path", "size", "sha256"}
                for item in files
            ):
                raise ValueError("invalid file entries")
            files_by_path = {item["path"]: item for item in files}
            if set(files_by_path) != required_files or len(files_by_path) != len(files):
                raise ValueError("projection file set does not match the registered package")

            for relative_text, file_entry in files_by_path.items():
                relative = Path(relative_text)
                if relative.is_absolute() or ".." in relative.parts:
                    raise ValueError(f"unsafe projected path {relative_text!r}")
                target = skills_dir / skill / relative
                targets.add(target)
                if not target.is_file() or target.is_symlink():
                    raise ValueError(f"missing projected file {target.relative_to(root)}")
                payload = target.read_bytes()
                digest = file_entry["sha256"]
                if file_entry["size"] != len(payload):
                    raise ValueError(f"size mismatch for {target.relative_to(root)}")
                if not isinstance(digest, str) or hashlib.sha256(payload).hexdigest() != digest:
                    raise ValueError(f"sha256 mismatch for {target.relative_to(root)}")
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            errors.append(f"{label}: {exc}")

    return targets, errors


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

    for source_text, target_text in BUNDLED_RESOURCE_FILES:
        source = ROOT / source_text
        files[SKILLS_DIR / target_text] = source.read_text(encoding="utf-8")

    for source_text, target_text in BUNDLED_RESOURCE_TREES:
        source_root = ROOT / source_text
        target_root = SKILLS_DIR / target_text
        for source in sorted(source_root.rglob("*")):
            if source.is_file():
                files[target_root / source.relative_to(source_root)] = source.read_text(
                    encoding="utf-8"
                )
    return files


def check() -> list[str]:
    errors: list[str] = []
    expected = expected_files()
    projection_targets, projection_errors = pinned_projection_status()
    errors.extend(projection_errors)
    for path, content in expected.items():
        if not path.is_file():
            errors.append(f"missing generated file: {path.relative_to(ROOT)}")
            continue
        current = path.read_text(encoding="utf-8")
        if current != content:
            errors.append(f"generated file is stale: {path.relative_to(ROOT)}")

    allowed = {path.resolve() for path in expected} | {
        path.resolve() for path in projection_targets
    }
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        for item in skill_dir.rglob("*"):
            if item.is_file() and item.resolve() not in allowed:
                errors.append(f"unexpected generated payload file: {item.relative_to(ROOT)}")
    return errors


def write() -> None:
    expected = expected_files()
    projection_targets, projection_errors = pinned_projection_status()
    if projection_errors:
        raise RuntimeError("pinned projection validation failed:\n- " + "\n- ".join(projection_errors))
    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    allowed = {path.resolve() for path in expected} | {
        path.resolve() for path in projection_targets
    }
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        for item in sorted(skill_dir.rglob("*"), reverse=True):
            if item.is_file() and item.resolve() not in allowed:
                item.unlink()
            elif item.is_dir() and not any(item.iterdir()):
                item.rmdir()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate canonical Softpowers methods and preserve verified pinned skill projections."
        )
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
        print("Generated methods and verified pinned skill projections are in sync.")
        return 0

    try:
        write()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    reference_count = sum(bool(entry.get("router_reference", True)) for entry in METHODS)
    implicit_specialist_count = sum(
        bool(entry.get("implicit", False)) for entry in PINNED_PROJECTIONS
    )
    explicit_leaf_count = len(METHODS)
    print(
        f"Generated router, {reference_count} router references, "
        f"preserved {implicit_specialist_count} pinned implicit specialist, and "
        f"generated {explicit_leaf_count} explicit leaf skills."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
