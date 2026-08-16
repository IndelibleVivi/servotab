#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment dependent
    print(
        "ERROR: PyYAML is required for maintainer YAML validation. Install it with "
        "`python3 -m pip install PyYAML`.",
        file=sys.stderr,
    )
    raise SystemExit(3) from exc

from common import (
    BUNDLED_RESOURCE_TARGETS,
    EXPECTED,
    IMPLICIT_SKILL_NAMES,
    REFERENCE_NAMES,
    ROUTER_NAME,
)

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def load_yaml(text: str, label: str) -> dict[str, Any]:
    try:
        parsed = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ValueError(f"{label}: invalid YAML: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"{label}: YAML root must be a mapping")
    return parsed


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")
    return load_yaml(match.group(1), "frontmatter"), text[match.end() :]


def expected_payload_files(name: str) -> set[str]:
    files = {"SKILL.md", "agents/openai.yaml"}
    if name == ROUTER_NAME:
        files.update(f"references/{reference}" for reference in REFERENCE_NAMES)
    prefix = f"{name}/"
    files.update(
        relative.removeprefix(prefix)
        for relative in BUNDLED_RESOURCE_TARGETS
        if relative.startswith(prefix)
    )
    return files


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    name = skill_dir.name
    skill_path = skill_dir / "SKILL.md"
    agent_path = skill_dir / "agents" / "openai.yaml"

    if skill_dir.is_symlink():
        return [f"{name}: skill directory must not be a symlink"]
    if not skill_path.is_file():
        return [f"{name}: missing SKILL.md"]
    if not agent_path.is_file():
        return [f"{name}: missing agents/openai.yaml"]

    actual_files: set[str] = set()
    for item in skill_dir.rglob("*"):
        relative = item.relative_to(skill_dir).as_posix()
        if item.is_symlink():
            errors.append(f"{name}: symlink not allowed in pack: {relative}")
        elif item.is_file():
            actual_files.add(relative)

    expected_files = expected_payload_files(name)
    missing = expected_files - actual_files
    extra = actual_files - expected_files
    if missing:
        errors.append(f"{name}: missing payload files: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"{name}: unexpected payload files: {', '.join(sorted(extra))}")

    text = skill_path.read_text(encoding="utf-8")
    try:
        fm, body = parse_frontmatter(text)
    except ValueError as exc:
        errors.append(f"{name}: {exc}")
        fm, body = {}, ""

    if fm.get("name") != name:
        errors.append(f"{name}: frontmatter name is {fm.get('name')!r}")
    description = fm.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{name}: missing or non-string frontmatter description")
    elif len(description) > 500:
        errors.append(f"{name}: description exceeds 500 characters")

    body_lines = body.splitlines()
    max_lines = 130 if name == ROUTER_NAME else 260
    if len(body_lines) > max_lines:
        errors.append(f"{name}: body is unusually long ({len(body_lines)} lines; max {max_lines})")
    if name == ROUTER_NAME and len(body.split()) > 650:
        errors.append(f"{name}: implicit router exceeds 650 words")
    if name != ROUTER_NAME and "$soft-" in body:
        errors.append(f"{name}: leaf body contains a cross-skill invocation")

    try:
        agent = load_yaml(agent_path.read_text(encoding="utf-8"), "agents/openai.yaml")
    except ValueError as exc:
        errors.append(f"{name}: {exc}")
        agent = {}

    interface = agent.get("interface")
    policy = agent.get("policy")
    if not isinstance(interface, dict):
        errors.append(f"{name}: openai.yaml interface must be a mapping")
        interface = {}
    if not isinstance(policy, dict):
        errors.append(f"{name}: openai.yaml policy must be a mapping")
        policy = {}

    for field in ("display_name", "short_description", "default_prompt"):
        if not isinstance(interface.get(field), str) or not interface[field].strip():
            errors.append(f"{name}: openai.yaml missing non-empty interface.{field}")

    default_prompt = interface.get("default_prompt", "")
    if isinstance(default_prompt, str) and f"${name}" not in default_prompt:
        errors.append(f"{name}: default_prompt does not explicitly invoke ${name}")

    expected_implicit = name in IMPLICIT_SKILL_NAMES
    if policy.get("allow_implicit_invocation") is not expected_implicit:
        errors.append(
            f"{name}: allow_implicit_invocation must be "
            f"{'true' if expected_implicit else 'false'}"
        )

    products = policy.get("products")
    if not isinstance(products, list) or "CODEX" not in products:
        errors.append(f"{name}: policy.products must include CODEX")

    return errors


def validate_directory(skills_dir: Path, *, exact: bool = False) -> list[str]:
    if not skills_dir.is_dir():
        return [f"skills directory not found: {skills_dir}"]

    found = {
        p.name
        for p in skills_dir.iterdir()
        if p.is_dir() and not p.name.startswith(".") and ".backup." not in p.name
    }
    errors: list[str] = []

    missing = EXPECTED - found
    if missing:
        errors.append(f"missing skill directories: {', '.join(sorted(missing))}")

    if exact:
        extra = found - EXPECTED
        if extra:
            errors.append(f"unexpected skill directories: {', '.join(sorted(extra))}")

    for name in sorted(EXPECTED & found):
        errors.extend(validate_skill(skills_dir / name))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the Softpowers skill pack.")
    parser.add_argument(
        "skills_dir",
        nargs="?",
        default=str(Path(__file__).resolve().parents[1] / "skills"),
        help="Directory containing skill folders",
    )
    parser.add_argument(
        "--exact",
        action="store_true",
        help="Reject non-Softpowers sibling directories (source pack or staging only)",
    )
    args = parser.parse_args()
    skills_dir = Path(args.skills_dir).expanduser().resolve()

    errors = validate_directory(skills_dir, exact=args.exact)
    if errors:
        print("Softpowers validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    total_lines = sum(
        len((skills_dir / name / "SKILL.md").read_text(encoding="utf-8").splitlines())
        for name in EXPECTED
    )
    suffix = " (exact directory set)" if args.exact else " (other skills allowed)"
    print(
        f"Softpowers validation passed: {len(EXPECTED)} skills, "
        f"{len(REFERENCE_NAMES)} router references, {total_lines} SKILL.md lines{suffix}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
