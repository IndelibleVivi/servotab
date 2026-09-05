#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from skill_catalog import METHODS, ROUTER, SKILL_ICON_SOURCES

ROOT = Path(__file__).resolve().parents[1]
ASSET_NAMES = ("composer-icon.png", "logo.png")

ROUTER_BODY = """# Servotab

Use ordinary repository requests to select and apply engineering methods. The user need not name a skill. Keep communication quiet; keep the requested outcome complete.

## Before the first consequential action

- Read applicable instructions and the smallest relevant implementation, tests, and accepted contract. Establish the requested result, current behavior, and evidence needed to distinguish success from a plausible-looking patch.
- Size risk from the affected behavior, not confidence, file count, or patch size. Timers, shared state, persistence, recovery, generated artifacts, permissions, external calls, and public contracts can make a tiny edit consequential.
- Preserve explicit corrections and accepted scope. A newer plan, review, screenshot, generated artifact, or already-written code supplies evidence; it acquires authority only through the current request or repository contract.
- Keep clear local work direct. Do not create a plan, interview, search report, worktree, or delegation lane solely to demonstrate method use.

## Resolve decisions at their dependencies

When a material decision remains open, read `references/design.md` before committing to the dependent approach.

- Investigate repository and environmental facts yourself. Ask the user for intent or value choices that materially change the outcome and cannot safely be inferred.
- Ask only questions whose prerequisites are settled; include a grounded recommendation. Recompute dependent choices after an answer changes an assumption. An unresolved branch does not stop independent safe work.
- Use delegated reversible choices and explicit best-effort assumptions where authorized. Do not turn the absence of a prewritten design into a request for approval.
- Stop questioning when the current work is decision-ready. Do not exhaust unrelated future branches or reopen settled product decisions without contradictory evidence.

## Search before new common machinery

Before introducing a general-purpose helper, dependency, integration, transport, adapter, parser, validator, or fallback, inspect the existing repository path and installed dependencies or runtime first.

- Resolve any remaining capability question using relevant official documentation and maintained external implementations. Do not claim a platform limitation from old recollection alone.
- Search only channels that can change the decision. Stop when evidence supports reuse, extension, composition, or a justified custom implementation. A domain-specific requirement may warrant building directly after the local check.
- Report material unavailable coverage accurately. An unavailable channel does not establish that no solution exists.
- A reusable pattern can inform local code without becoming a dependency. Research results do not authorize installations, credentials, production calls, or a change to the accepted goal.

## Load methods at the action they govern

Read the applicable reference before its phase's first consequential action, including on a simple-looking task when its trigger is present. Reuse an unchanged reference already read in the available context; reload after context loss when needed. Combine complementary methods when the work crosses phases. No fixed full-stack workflow is required.

- Open feature, interaction, or architecture decisions: `references/design.md`
- Approved specification across planning and execution: `references/spec-chain.md`
- Settled multi-step work that needs sequencing: `references/plan.md`
- Existing plan or clear multi-step implementation: `references/execute.md`
- Bug, regression, failing test, or unexplained behavior: `references/debug.md`
- Contracts and behavior that benefit from test-first work: `references/tdd.md`
- Diff, commit, branch, PR, or implementation review: `references/review.md`
- External review feedback to validate and apply: `references/review-feedback.md`
- Completion and readiness claims needing fresh proof: `references/verify.md`
- Isolation justified by dirty state, risk, duration, or parallel writes: `references/worktree.md`
- Bounded worker lanes that materially improve the work: `references/delegate.md`
- Final integration, Git, PR, or cleanup decisions: `references/finish.md`

A bug requires investigation even when its eventual fix is one line. Review feedback requires adjudication before editing. An approved specification remains the whole acceptance contract when execution covers only one tranche. A user-requested planning-only or source-only boundary remains in force across method transitions.

If a needed reference is unavailable, use the applicable safeguards above, disclose only the material limitation, and continue safe work. Do not invent its contents or claim it was loaded.

## Preserve outcome and permission boundaries

- Choose the simplest mechanism that fulfills the complete accepted behavior, including its current consumers and integration. Do not silently replace the result with an MVP, placeholder, or backend-only slice.
- Evaluate a proposed mechanism independently while respecting user-selected meaning. Do not widen trust, change programme order, or introduce infrastructure with no present consumer.
- Keep the existing task record or complete plan current after a material correction. Preserve deferred scope and why it remains. Create a persistent record only when the work needs continuity; do not create a second tracker.
- Stop only at an unresolved authority boundary. Continue other safe, in-scope work. Research, file presence, reviewer advice, and test success confer no additional permission.
- Keep Git operations, deployment, publication, secret access, and paid or live-provider operations within their applicable authorization. No method grants them by itself.

## Choose evidence that could disprove the patch

- A meaningful check distinguishes the relevant failure from success. For a bug, use a reproducer that fails on the old behavior when this can be done safely in a disposable copy; do not revert unrelated live work.
- Inspect the failure families the change actually exposes. A timer needs repeated/interleaved activation; recovery needs interrupted or partial state; an input validator needs malformed inputs; UI motion needs its applicable accessibility behavior. Do not run every family for every edit.
- Do not weaken assertions, drop accepted scenarios, or edit only expected outputs to make a test green. Establish changed requirements before changing their oracle.
- After a check fails, distinguish patch regression, existing baseline failure, and environment failure. Repeated same-mechanism failures require a new causal investigation, not another cosmetic retry.
- When review findings arrive, resolve each material finding as fixed with evidence, rejected with evidence, or explicitly deferred under applicable authority. An open blocker cannot disappear behind a later summary or green CI.

## Close the actual claim

Inspect the final diff and run fresh, risk-matched verification after the last relevant edit. Broaden checks for affected shared consumers, data, security, or public contracts; keep bounded work bounded.

Separate delivered behavior, verified evidence, and remaining gaps. Package validity, installation, instruction delivery, successful use, deployment, and owner acceptance are distinct observations. A hash, checkbox, or configuration entry is not behavior proof.

A real failure may justify a local regression test or a reusable method change. Preserve a small, relevant observation and its causal limit; do not turn every incident into global policy or start an evaluation campaign without authorization.

These instructions guide model behavior. They do not enforce tool permissions or guarantee that the host selected this skill. Use repository tests and host-supported controls for boundaries that require deterministic enforcement.
"""


def locations(root: Path) -> tuple[Path, Path, Path, Path]:
    plugin_root = root / "plugins" / "servotab"
    return (
        root / "methods",
        plugin_root / "skills",
        root / "skills",
        plugin_root / "assets",
    )


def quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def frontmatter(name: str, description: str) -> str:
    return f"---\nname: {name}\ndescription: {quote(description)}\n---\n\n"


def openai_yaml(entry: dict[str, object], *, implicit: bool) -> str:
    return (
        "interface:\n"
        f"  display_name: {quote(str(entry['display_name']))}\n"
        f"  short_description: {quote(str(entry['short_description']))}\n"
        f"  default_prompt: {quote(str(entry['default_prompt']))}\n"
        "  brand_color: \"#315EFB\"\n"
        "  icon_small: \"./assets/icon-400.png\"\n"
        "  icon_large: \"./assets/icon.svg\"\n"
        "policy:\n"
        f"  allow_implicit_invocation: {'true' if implicit else 'false'}\n"
    )


def add_skill_icons(
    files: dict[Path, bytes],
    *,
    root: Path,
    skill_dir: Path,
    skill_name: str,
) -> None:
    sources = SKILL_ICON_SOURCES[skill_name]
    for source_kind, output_name in (("svg", "icon.svg"), ("png", "icon-400.png")):
        source = root / "assets" / sources[source_kind]
        files[skill_dir / "assets" / output_name] = source.read_bytes()


def expected_files(root: Path = ROOT) -> dict[Path, bytes]:
    methods_dir, skills_dir, _, _ = locations(root)
    files: dict[Path, bytes] = {}
    router_dir = skills_dir / str(ROUTER["name"])
    files[router_dir / "SKILL.md"] = (
        frontmatter(str(ROUTER["name"]), str(ROUTER["description"])) + ROUTER_BODY
    ).encode("utf-8")
    files[router_dir / "agents" / "openai.yaml"] = openai_yaml(
        ROUTER, implicit=True
    ).encode("utf-8")
    add_skill_icons(
        files,
        root=root,
        skill_dir=router_dir,
        skill_name=str(ROUTER["name"]),
    )

    for entry in METHODS:
        method_name = str(entry["method"])
        method_path = methods_dir / f"{method_name}.md"
        method_body = method_path.read_text(encoding="utf-8")
        if not method_body.endswith("\n"):
            method_body += "\n"
        if entry.get("router_reference", True):
            files[router_dir / "references" / f"{method_name}.md"] = method_body.encode(
                "utf-8"
            )

        skill_dir = skills_dir / str(entry["skill"])
        files[skill_dir / "SKILL.md"] = (
            frontmatter(str(entry["skill"]), str(entry["description"])) + method_body
        ).encode("utf-8")
        files[skill_dir / "agents" / "openai.yaml"] = openai_yaml(
            entry, implicit=bool(entry.get("implicit", False))
        ).encode("utf-8")
        add_skill_icons(
            files,
            root=root,
            skill_dir=skill_dir,
            skill_name=str(entry["skill"]),
        )
    return files


def check(root: Path = ROOT) -> list[str]:
    _, skills_dir, legacy_skills_dir, plugin_assets_dir = locations(root)
    errors: list[str] = []
    try:
        expected = expected_files(root)
    except FileNotFoundError as exc:
        return [f"missing canonical source: {exc.filename}"]

    for path, content in expected.items():
        if not path.is_file():
            errors.append(f"missing generated file: {path.relative_to(root)}")
        elif path.read_bytes() != content:
            errors.append(f"generated file is stale: {path.relative_to(root)}")

    allowed = {path.resolve() for path in expected}
    if skills_dir.is_dir():
        for item in skills_dir.rglob("*"):
            if item.is_file() and item.resolve() not in allowed:
                errors.append(f"unexpected generated payload file: {item.relative_to(root)}")

    if legacy_skills_dir.exists():
        errors.append("retired root skills/ projection still exists")

    root_assets_dir = root / "assets"
    for name in ASSET_NAMES:
        source = root_assets_dir / name
        target = plugin_assets_dir / name
        if not source.is_file():
            errors.append(f"missing canonical asset: assets/{name}")
        elif not target.is_file():
            errors.append(f"missing plugin asset: plugins/servotab/assets/{name}")
        elif source.read_bytes() != target.read_bytes():
            errors.append(f"plugin asset is stale: plugins/servotab/assets/{name}")
    if plugin_assets_dir.is_dir():
        for item in plugin_assets_dir.iterdir():
            if item.name not in ASSET_NAMES:
                errors.append(f"unexpected plugin asset: {item.relative_to(root)}")
    return errors


def write(root: Path = ROOT) -> None:
    _, skills_dir, legacy_skills_dir, plugin_assets_dir = locations(root)
    if legacy_skills_dir.exists():
        raise FileExistsError(
            f"retired root skills/ projection still exists: {legacy_skills_dir}; "
            "remove it through the reviewed migration change, not the generator"
        )
    expected = expected_files(root)
    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    allowed = {path.resolve() for path in expected}
    if skills_dir.is_dir():
        for item in sorted(skills_dir.rglob("*"), reverse=True):
            if item.is_file() and item.resolve() not in allowed:
                item.unlink()
            elif item.is_dir() and not any(item.iterdir()):
                item.rmdir()

    plugin_assets_dir.mkdir(parents=True, exist_ok=True)
    for item in plugin_assets_dir.iterdir():
        if item.name in ASSET_NAMES:
            continue
        if item.is_dir() and not item.is_symlink():
            shutil.rmtree(item)
        else:
            item.unlink()
    for name in ASSET_NAMES:
        source = root / "assets" / name
        if not source.is_file():
            raise FileNotFoundError(f"missing canonical asset: {source}")
        shutil.copyfile(source, plugin_assets_dir / name)

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate the Servotab plugin skills and curated package assets."
    )
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale")
    args = parser.parse_args()

    if args.check:
        errors = check()
        if errors:
            print("Servotab source/generated sync failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        print("Servotab methods, plugin skills, and curated assets are in sync.")
        return 0

    try:
        write()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(
        f"Generated one implicit router, {len(METHODS)} explicit leaves, "
        f"{len(METHODS)} router references, {2 * (len(METHODS) + 1)} skill icon assets, "
        f"and {len(ASSET_NAMES)} plugin assets."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
