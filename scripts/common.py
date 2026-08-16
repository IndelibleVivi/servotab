#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import os
from pathlib import Path

from skill_catalog import (
    BUNDLED_RESOURCE_FILES,
    BUNDLED_RESOURCE_TREES,
    IMPLICIT_SKILL_NAMES,
    METHOD_BY_SKILL,
    REFERENCE_METHOD_NAMES,
    ROUTER,
    SKILL_NAMES,
)

PACK_ROOT = Path(__file__).resolve().parents[1]
VERSION = (PACK_ROOT / "VERSION").read_text(encoding="utf-8").strip()
ROUTER_NAME = str(ROUTER["name"])
EXPECTED = frozenset(SKILL_NAMES)
REFERENCE_NAMES = tuple(f"{name}.md" for name in REFERENCE_METHOD_NAMES)


def bundled_resource_targets() -> tuple[str, ...]:
    targets = [target for _, target in BUNDLED_RESOURCE_FILES]
    for source_text, target_text in BUNDLED_RESOURCE_TREES:
        source_root = PACK_ROOT / source_text
        for source in sorted(source_root.rglob("*")):
            if source.is_file():
                targets.append((Path(target_text) / source.relative_to(source_root)).as_posix())
    return tuple(targets)


BUNDLED_RESOURCE_TARGETS = bundled_resource_targets()


def _has_softpowers_install(skills_dir: Path) -> bool:
    return (
        (skills_dir / ".softpowers-current-manifest").is_file()
        or (skills_dir / ROUTER_NAME / "SKILL.md").is_file()
    )


def default_skills_dir() -> Path:
    """Resolve the user skill root while preserving upgrades from v0.1.x."""
    explicit = os.environ.get("SOFTPOWERS_SKILLS_DIR") or os.environ.get("AGENTS_SKILLS_DIR")
    if explicit:
        return Path(explicit).expanduser()

    codex_home_raw = os.environ.get("CODEX_HOME")
    if codex_home_raw:
        return Path(codex_home_raw).expanduser() / "skills"

    home = Path.home()
    official = home / ".agents" / "skills"
    legacy = home / ".codex" / "skills"
    installed = [path for path in (official, legacy) if _has_softpowers_install(path)]

    if len(installed) == 1:
        return installed[0]
    if len(installed) > 1:
        raise RuntimeError(
            "Softpowers appears in both ~/.agents/skills and ~/.codex/skills. "
            "Use --dest or SOFTPOWERS_SKILLS_DIR to select the active root explicitly."
        )

    if official.is_dir():
        return official
    if legacy.is_dir():
        return legacy
    return official


def resolve_skills_dir(value: str | None) -> Path:
    return (Path(value).expanduser() if value else default_skills_dir()).resolve()


def path_exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def remove_path(path: Path) -> None:
    if not path_exists(path):
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    import shutil

    shutil.rmtree(path)


def directory_digest(path: Path) -> str:
    """Hash a file, symlink, or directory deterministically."""
    digest = hashlib.sha256()

    if path.is_symlink():
        digest.update(b"L\0")
        digest.update(os.readlink(path).encode("utf-8", errors="surrogateescape"))
        return digest.hexdigest()

    if path.is_file():
        digest.update(b"F\0")
        digest.update(path.name.encode("utf-8", errors="surrogateescape"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        return digest.hexdigest()

    digest.update(b"D\0")
    for item in sorted(path.rglob("*"), key=lambda p: p.relative_to(path).as_posix()):
        relative = item.relative_to(path).as_posix().encode("utf-8", errors="surrogateescape")
        if item.is_symlink():
            digest.update(b"L\0" + relative + b"\0")
            digest.update(os.readlink(item).encode("utf-8", errors="surrogateescape"))
        elif item.is_dir():
            digest.update(b"D\0" + relative + b"\0")
        elif item.is_file():
            digest.update(b"F\0" + relative + b"\0")
            digest.update(item.read_bytes())
    return digest.hexdigest()


def assert_child(path: Path, parent: Path) -> None:
    path.resolve(strict=False).relative_to(parent.resolve(strict=False))
