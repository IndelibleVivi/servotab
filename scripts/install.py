#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import (
    IMPLICIT_SKILL_NAMES,
    SKILL_NAMES,
    VERSION,
    assert_child,
    directory_digest,
    path_exists,
    remove_path,
    resolve_skills_dir,
)
from runtime_validate import PACK_MANIFEST, validate_payload


def timestamp_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw_temp = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp = Path(raw_temp)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def active_manifest_retired_skills(dest: Path) -> tuple[str, ...]:
    pointer = dest / ".softpowers-current-manifest"
    if not pointer.is_file():
        return ()
    raw = pointer.read_text(encoding="utf-8").strip()
    if not raw:
        raise RuntimeError(f"Current manifest pointer is empty: {pointer}")
    manifest_path = Path(raw).expanduser().resolve()
    assert_child(manifest_path, dest / ".softpowers-manifests")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot inspect active Softpowers manifest: {manifest_path}") from exc
    if (
        not isinstance(manifest, dict)
        or manifest.get("pack") != "softpowers-pack"
        or manifest.get("status") != "installed"
        or not isinstance(manifest.get("skills"), list)
    ):
        raise RuntimeError(f"Invalid active Softpowers manifest: {manifest_path}")
    names = []
    for entry in manifest["skills"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
            raise RuntimeError(f"Malformed skill entry in active manifest: {manifest_path}")
        names.append(entry["name"])
    if len(names) != len(set(names)):
        raise RuntimeError(f"Duplicate skill entries in active manifest: {manifest_path}")
    return tuple(sorted(set(names) - set(SKILL_NAMES)))


def install_pack(
    source: Path,
    dest: Path,
    *,
    fail_after: int | None = None,
) -> Path:
    source = source.resolve()
    dest = dest.resolve()

    errors = validate_payload(source, manifest_path=PACK_MANIFEST, allow_other_skills=False)
    if errors:
        raise RuntimeError("Source validation failed:\n- " + "\n- ".join(errors))

    retired = active_manifest_retired_skills(dest)
    if retired:
        names = ", ".join(retired)
        guidance = (
            " The License Boundary skill must be installed independently from "
            "IndelibleVivi/license-boundary at v0.1.0-rc3."
            if "license-boundary" in retired
            else ""
        )
        raise RuntimeError(
            "The active historical Softpowers layer still manages retired skill(s): "
            f"{names}. Run this release's `./uninstall.sh --dest <skills-dir>`; repeat "
            "while this message appears, then run the installer again."
            + guidance
        )

    dest.mkdir(parents=True, exist_ok=True)
    stamp = timestamp_slug()
    staging = Path(tempfile.mkdtemp(prefix=".softpowers-staging-", dir=dest))
    backup_root = dest / ".softpowers-backups" / stamp
    manifest_dir = dest / ".softpowers-manifests"
    manifest_path = manifest_dir / f"softpowers-{VERSION}-{stamp}.json"
    pointer_path = dest / ".softpowers-current-manifest"

    previous_pointer = pointer_path.read_text(encoding="utf-8").strip() if pointer_path.is_file() else ""
    moved_backups: dict[str, Path] = {}
    installed_names: list[str] = []
    manifest_written = False

    try:
        for name in SKILL_NAMES:
            shutil.copytree(source / name, staging / name)

        staging_errors = validate_payload(staging, manifest_path=PACK_MANIFEST, allow_other_skills=False)
        if staging_errors:
            raise RuntimeError("Staging validation failed:\n- " + "\n- ".join(staging_errors))

        backup_root.mkdir(parents=True, exist_ok=True)

        for index, name in enumerate(SKILL_NAMES, start=1):
            target = dest / name
            staged_skill = staging / name
            backup = backup_root / name
            assert_child(target, dest)
            assert_child(backup, dest)

            if path_exists(target):
                backup.parent.mkdir(parents=True, exist_ok=True)
                os.replace(target, backup)
                moved_backups[name] = backup

            os.replace(staged_skill, target)
            installed_names.append(name)

            if fail_after is not None and index >= fail_after:
                raise RuntimeError(f"Injected self-test failure after {index} skills")

        target_errors = validate_payload(dest, manifest_path=PACK_MANIFEST, allow_other_skills=True)
        if target_errors:
            raise RuntimeError("Installed target validation failed:\n- " + "\n- ".join(target_errors))

        skills: list[dict[str, Any]] = []
        for name in SKILL_NAMES:
            target = dest / name
            backup = moved_backups.get(name)
            skills.append(
                {
                    "name": name,
                    "target": str(target),
                    "backup": str(backup) if backup else None,
                    "installed_sha256": directory_digest(target),
                }
            )

        manifest = {
            "schema_version": 1,
            "pack": "softpowers-pack",
            "version": VERSION,
            "status": "installed",
            "installed_at": datetime.now(timezone.utc).isoformat(),
            "destination": str(dest),
            "previous_manifest": previous_pointer or None,
            "skills": skills,
        }
        atomic_write_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        manifest_written = True
        atomic_write_text(pointer_path, str(manifest_path) + "\n")

        shutil.rmtree(staging, ignore_errors=True)
        if backup_root.exists() and not any(backup_root.iterdir()):
            backup_root.rmdir()
        return manifest_path

    except Exception:
        # Remove only directories installed by this transaction, then restore backups.
        for name in reversed(installed_names):
            remove_path(dest / name)
        for name, backup in reversed(list(moved_backups.items())):
            target = dest / name
            if path_exists(backup):
                os.replace(backup, target)

        if manifest_written and manifest_path.exists():
            manifest_path.unlink()
        if previous_pointer:
            atomic_write_text(pointer_path, previous_pointer + "\n")
        elif pointer_path.exists():
            pointer_path.unlink()

        shutil.rmtree(staging, ignore_errors=True)
        if backup_root.exists():
            shutil.rmtree(backup_root, ignore_errors=True)
        raise


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Install the Softpowers skill pack transactionally.")
    parser.add_argument("--dest", help="Override the Codex skills directory")
    args = parser.parse_args()

    source = root / "skills"
    try:
        dest = resolve_skills_dir(args.dest)
        manifest = install_pack(source, dest)
    except Exception as exc:
        print(f"Softpowers installation failed; prior state was restored.\nERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Installed {len(SKILL_NAMES)} Softpowers skills into {dest}")
    print(f"Install manifest: {manifest}")
    print("Existing unrelated skills were left untouched.")
    print(
        f"Implicit surfaces: {', '.join(IMPLICIT_SKILL_NAMES)}; "
        f"the {len(SKILL_NAMES) - len(IMPLICIT_SKILL_NAMES)} soft-* leaf skills "
        "remain explicit-only."
    )
    print("Open Codex and run /skills. Restart Codex if the skill list is stale.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
