#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from common import (
    BUNDLED_RESOURCE_TARGETS,
    IMPLICIT_SKILL_NAMES,
    PACK_ROOT,
    PINNED_PROJECTION_TARGETS,
    REFERENCE_NAMES,
    ROUTER_NAME,
    SKILL_NAMES,
    VERSION,
)

PACK_MANIFEST = PACK_ROOT / "PACK_MANIFEST.json"


def expected_payload_files() -> frozenset[str]:
    files = {
        f"skills/{name}/SKILL.md" for name in SKILL_NAMES
    } | {
        f"skills/{name}/agents/openai.yaml" for name in SKILL_NAMES
    }
    files |= {
        f"skills/{ROUTER_NAME}/references/{reference}" for reference in REFERENCE_NAMES
    }
    files |= {f"skills/{relative}" for relative in BUNDLED_RESOURCE_TARGETS}
    files |= {f"skills/{relative}" for relative in PINNED_PROJECTION_TARGETS}
    return frozenset(files)


EXPECTED_PAYLOAD_FILES = expected_payload_files()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_pack_manifest(path: Path = PACK_MANIFEST) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"pack manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid pack manifest JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("pack manifest root must be an object")
    if data.get("schema_version") != 2:
        raise ValueError(f"unsupported pack manifest schema: {data.get('schema_version')!r}")
    if data.get("pack") != "softpowers-pack":
        raise ValueError(f"unexpected pack id: {data.get('pack')!r}")
    if data.get("version") != VERSION:
        raise ValueError(
            f"pack manifest version {data.get('version')!r} does not match VERSION {VERSION!r}"
        )

    skills = data.get("skills")
    if not isinstance(skills, list) or skills != list(SKILL_NAMES):
        raise ValueError("pack manifest skill order/set does not match this release")

    activation = data.get("activation")
    expected_activation = {
        "implicit": list(IMPLICIT_SKILL_NAMES),
        "explicit_only": [name for name in SKILL_NAMES if name not in IMPLICIT_SKILL_NAMES],
    }
    if activation != expected_activation:
        raise ValueError("pack manifest activation contract does not match this release")

    files = data.get("files")
    if not isinstance(files, list):
        raise ValueError("pack manifest files must be a list")

    seen: set[str] = set()
    for entry in files:
        if not isinstance(entry, dict):
            raise ValueError("pack manifest file entry must be an object")
        relative = entry.get("path")
        digest = entry.get("sha256")
        size = entry.get("size")
        if not isinstance(relative, str) or relative.startswith("/") or ".." in Path(relative).parts:
            raise ValueError(f"unsafe or invalid manifest path: {relative!r}")
        if relative in seen:
            raise ValueError(f"duplicate manifest path: {relative}")
        if not isinstance(digest, str) or len(digest) != 64:
            raise ValueError(f"invalid sha256 for {relative}")
        if not isinstance(size, int) or size < 0:
            raise ValueError(f"invalid size for {relative}")
        seen.add(relative)

    if seen != EXPECTED_PAYLOAD_FILES:
        missing = sorted(EXPECTED_PAYLOAD_FILES - seen)
        extra = sorted(seen - EXPECTED_PAYLOAD_FILES)
        details: list[str] = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if extra:
            details.append("unexpected: " + ", ".join(extra))
        raise ValueError("pack manifest payload set mismatch (" + "; ".join(details) + ")")

    return data


def validate_payload(
    skills_dir: Path,
    *,
    manifest_path: Path = PACK_MANIFEST,
    allow_other_skills: bool = False,
) -> list[str]:
    errors: list[str] = []
    skills_dir = skills_dir.resolve()

    try:
        manifest = load_pack_manifest(manifest_path)
    except ValueError as exc:
        return [str(exc)]

    if not skills_dir.is_dir():
        return [f"skills directory not found: {skills_dir}"]
    if skills_dir.is_symlink():
        return [f"skills directory must not be a symlink: {skills_dir}"]

    top_level = list(skills_dir.iterdir())
    found_skill_dirs = {
        path.name
        for path in top_level
        if path.is_dir() and not path.name.startswith(".")
    }
    expected_skills = set(SKILL_NAMES)
    missing_skills = expected_skills - found_skill_dirs
    if missing_skills:
        errors.append("missing skill directories: " + ", ".join(sorted(missing_skills)))
    if not allow_other_skills:
        unexpected_entries = sorted(path.name for path in top_level if path.name not in expected_skills)
        if unexpected_entries:
            errors.append("unexpected entries in skills directory: " + ", ".join(unexpected_entries))

    expected_local_files = {
        Path(entry["path"]).relative_to("skills").as_posix() for entry in manifest["files"]
    }
    expected_local_dirs: set[str] = set()
    for relative in expected_local_files:
        parent = Path(relative).parent
        while parent.as_posix() not in (".", ""):
            expected_local_dirs.add(parent.as_posix())
            parent = parent.parent
    expected_local_dirs -= set(SKILL_NAMES)

    actual_local_files: set[str] = set()
    actual_local_dirs: set[str] = set()

    for name in SKILL_NAMES:
        skill_dir = skills_dir / name
        if skill_dir.is_symlink():
            errors.append(f"skill directory must not be a symlink: {name}")
            continue
        if not skill_dir.is_dir():
            continue
        for item in skill_dir.rglob("*"):
            relative = item.relative_to(skills_dir).as_posix()
            if item.is_symlink():
                errors.append(f"symlink not allowed in payload: {relative}")
            elif item.is_dir():
                actual_local_dirs.add(relative)
            elif item.is_file():
                actual_local_files.add(relative)

    extra_dirs = actual_local_dirs - expected_local_dirs
    missing_dirs = expected_local_dirs - actual_local_dirs
    if missing_dirs:
        errors.append("missing payload directories: " + ", ".join(sorted(missing_dirs)))
    if extra_dirs:
        errors.append("unexpected payload directories: " + ", ".join(sorted(extra_dirs)))

    missing_files = expected_local_files - actual_local_files
    extra_files = actual_local_files - expected_local_files
    if missing_files:
        errors.append("missing payload files: " + ", ".join(sorted(missing_files)))
    if extra_files:
        errors.append("unexpected payload files: " + ", ".join(sorted(extra_files)))

    entries = {
        Path(entry["path"]).relative_to("skills").as_posix(): entry for entry in manifest["files"]
    }
    for relative in sorted(expected_local_files & actual_local_files):
        path = skills_dir / relative
        entry = entries[relative]
        actual_size = path.stat().st_size
        if actual_size != entry["size"]:
            errors.append(f"size mismatch for {relative}: expected {entry['size']}, got {actual_size}")
            continue
        actual_digest = file_sha256(path)
        if actual_digest != entry["sha256"]:
            errors.append(f"sha256 mismatch for {relative}")

    return errors
