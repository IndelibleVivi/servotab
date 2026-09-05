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
        "ERROR: PyYAML is required for maintainer validation. Run with "
        "`python -m pip install -r requirements-dev.txt`.",
        file=sys.stderr,
    )
    raise SystemExit(3) from exc

from asset_validation import validate_png, validate_svg

from skill_catalog import IMPLICIT_SKILL_NAMES, REFERENCE_METHOD_NAMES, ROUTER, SKILL_NAMES

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_DIR = ROOT / "plugins" / "servotab" / "skills"
ROUTER_NAME = str(ROUTER["name"])
EXPECTED = frozenset(SKILL_NAMES)
REFERENCE_NAMES = frozenset(f"{name}.md" for name in REFERENCE_METHOD_NAMES)
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
RETIRED_ACTIVE_TOKENS = (
    "$softpowers",
    "$soft-",
    "references/brainstorm.md",
    "references/receive-review.md",
    "references/parallel.md",
)
ICON_INTERFACE = {
    "icon_small": "./assets/icon-400.png",
    "icon_large": "./assets/icon.svg",
}
class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys instead of silently changing policy."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            if key in result:
                raise yaml.constructor.ConstructorError(None, None, "duplicate mapping key", key_node.start_mark)
            result[key] = loader.construct_object(value_node, deep=deep)
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(None, None, "unhashable mapping key", key_node.start_mark) from exc
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_yaml(text: str, label: str) -> dict[str, Any]:
    try:
        parsed = yaml.load(text, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise ValueError(f"{label}: invalid YAML: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"{label}: expected a YAML mapping")
    return parsed


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_RE.match(text)
    if match is None:
        raise ValueError("missing or malformed YAML frontmatter")
    return load_yaml(match.group(1), "SKILL.md frontmatter"), text[match.end() :]


def expected_payload_files() -> set[str]:
    files = {
        f"{name}/SKILL.md" for name in SKILL_NAMES
    } | {
        f"{name}/agents/openai.yaml" for name in SKILL_NAMES
    }
    files |= {f"{ROUTER_NAME}/references/{name}" for name in REFERENCE_NAMES}
    files |= {
        f"{name}/assets/{asset}"
        for name in SKILL_NAMES
        for asset in ("icon.svg", "icon-400.png")
    }
    return files


def validate_icon_asset(path: Path, *, field: str) -> list[str]:
    if field == "icon_small":
        return validate_png(path, (400, 400))
    if field == "icon_large":
        return validate_svg(path)
    return [f"unknown icon field: {field}"]


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    name = skill_dir.name
    skill_path = skill_dir / "SKILL.md"
    agent_path = skill_dir / "agents" / "openai.yaml"

    try:
        text = skill_path.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(text)
    except (OSError, ValueError) as exc:
        return [f"{name}: {exc}"]

    if frontmatter.get("name") != name:
        errors.append(f"{name}: frontmatter name is {frontmatter.get('name')!r}")
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{name}: missing non-empty frontmatter description")
    elif len(description) > 500:
        errors.append(f"{name}: description exceeds 500 characters")

    max_lines = 130 if name == ROUTER_NAME else 260
    if len(body.splitlines()) > max_lines:
        errors.append(f"{name}: body exceeds {max_lines} lines")
    for token in RETIRED_ACTIVE_TOKENS:
        if token in text:
            errors.append(f"{name}: active payload contains retired identifier {token!r}")

    try:
        agent = load_yaml(agent_path.read_text(encoding="utf-8"), "agents/openai.yaml")
    except (OSError, ValueError) as exc:
        errors.append(f"{name}: {exc}")
        return errors

    if set(agent) != {"interface", "policy"}:
        errors.append(f"{name}: openai.yaml must contain only interface and policy")
    interface = agent.get("interface")
    policy = agent.get("policy")
    if not isinstance(interface, dict):
        errors.append(f"{name}: openai.yaml interface must be a mapping")
        interface = {}
    if not isinstance(policy, dict):
        errors.append(f"{name}: openai.yaml policy must be a mapping")
        policy = {}

    required_interface = {
        "display_name",
        "short_description",
        "default_prompt",
        "brand_color",
        *ICON_INTERFACE,
    }
    if set(interface) != required_interface:
        errors.append(f"{name}: openai.yaml interface fields do not match the package contract")
    for field in ("display_name", "short_description", "default_prompt"):
        if not isinstance(interface.get(field), str) or not interface[field].strip():
            errors.append(f"{name}: openai.yaml missing non-empty interface.{field}")
    if interface.get("brand_color") != "#315EFB":
        errors.append(f"{name}: interface.brand_color must be #315EFB")
    for field, expected in ICON_INTERFACE.items():
        raw = interface.get(field)
        if raw != expected:
            errors.append(f"{name}: interface.{field} must be {expected!r}")
        if not isinstance(raw, str):
            continue
        relative = Path(raw)
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"{name}: interface.{field} must stay inside the skill directory")
            continue
        target = skill_dir / relative
        errors.extend(
            f"{name}: {error}" for error in validate_icon_asset(target, field=field)
        )
    default_prompt = interface.get("default_prompt", "")
    if isinstance(default_prompt, str) and f"${name}" not in default_prompt:
        errors.append(f"{name}: default_prompt does not explicitly invoke ${name}")

    expected_implicit = name in IMPLICIT_SKILL_NAMES
    if set(policy) != {"allow_implicit_invocation"}:
        errors.append(f"{name}: policy must contain only allow_implicit_invocation")
    if policy.get("allow_implicit_invocation") is not expected_implicit:
        errors.append(
            f"{name}: allow_implicit_invocation must be "
            f"{'true' if expected_implicit else 'false'}"
        )
    return errors


def validate_directory(skills_dir: Path, *, exact: bool = True) -> list[str]:
    if not skills_dir.is_dir():
        return [f"skills directory not found: {skills_dir}"]
    if skills_dir.is_symlink():
        return [f"skills directory must not be a symlink: {skills_dir}"]

    found = {
        path.name
        for path in skills_dir.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    }
    errors: list[str] = []
    missing = EXPECTED - found
    extra = found - EXPECTED
    if missing:
        errors.append(f"missing skill directories: {', '.join(sorted(missing))}")
    if exact and extra:
        errors.append(f"unexpected skill directories: {', '.join(sorted(extra))}")

    actual_files = {
        path.relative_to(skills_dir).as_posix()
        for path in skills_dir.rglob("*")
        if path.is_file()
    }
    expected_files = expected_payload_files()
    missing_files = expected_files - actual_files
    extra_files = actual_files - expected_files
    if missing_files:
        errors.append(f"missing payload files: {', '.join(sorted(missing_files))}")
    if exact and extra_files:
        errors.append(f"unexpected payload files: {', '.join(sorted(extra_files))}")

    router_references = skills_dir / ROUTER_NAME / "references"
    found_references = (
        {path.name for path in router_references.iterdir() if path.is_file()}
        if router_references.is_dir()
        else set()
    )
    if found_references != REFERENCE_NAMES:
        errors.append("router reference set does not match the 12 canonical methods")

    for name in sorted(EXPECTED & found):
        errors.extend(validate_skill(skills_dir / name))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the generated Servotab skills.")
    parser.add_argument(
        "skills_dir",
        nargs="?",
        default=str(DEFAULT_SKILLS_DIR),
        help="Directory containing the Servotab skill folders",
    )
    parser.add_argument(
        "--allow-extra",
        action="store_true",
        help="Allow unrelated sibling skill directories (not for the plugin package)",
    )
    args = parser.parse_args()
    skills_dir = Path(args.skills_dir).expanduser().absolute()
    errors = validate_directory(skills_dir, exact=not args.allow_extra)
    if errors:
        print("Servotab skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Servotab skill validation passed: {len(EXPECTED)} skills, "
        f"{len(REFERENCE_NAMES)} router references, exact package directory set."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
