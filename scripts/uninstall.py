#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import SKILL_NAMES, assert_child, directory_digest, path_exists, resolve_skills_dir
from install import atomic_write_text, timestamp_slug


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("pack") != "softpowers-pack":
        raise ValueError(f"Not a Softpowers install manifest: {path}")
    if not isinstance(data.get("skills"), list):
        raise ValueError(f"Manifest has no skills list: {path}")
    return data


def uninstall_pack(dest: Path, manifest_path: Path | None = None) -> tuple[Path, list[Path]]:
    dest = dest.resolve()
    pointer_path = dest / ".softpowers-current-manifest"

    if not pointer_path.is_file():
        raise RuntimeError(
            f"No current install manifest found at {pointer_path}. Refusing a blind uninstall."
        )

    current_raw = pointer_path.read_text(encoding="utf-8").strip()
    if not current_raw:
        raise RuntimeError(f"Current manifest pointer is empty: {pointer_path}")
    current_manifest = Path(current_raw).expanduser().resolve()

    if manifest_path is None:
        manifest_path = current_manifest
    else:
        manifest_path = manifest_path.expanduser().resolve()
        if manifest_path != current_manifest:
            raise RuntimeError(
                "Non-LIFO uninstall refused: the requested manifest is not the current "
                f"install layer. Uninstall the latest layer first ({current_manifest})."
            )

    manifest = load_manifest(manifest_path)

    manifest_dest = Path(str(manifest.get("destination", ""))).expanduser().resolve()
    if manifest_dest != dest:
        raise RuntimeError(f"Manifest destination {manifest_dest} does not match requested {dest}")
    if manifest.get("status") != "installed":
        raise RuntimeError(f"Manifest status is {manifest.get('status')!r}, expected 'installed'")

    entries = manifest["skills"]
    names = [entry.get("name") for entry in entries if isinstance(entry, dict)]
    if len(entries) != len(SKILL_NAMES) or set(names) != set(SKILL_NAMES) or len(names) != len(set(names)):
        raise RuntimeError("Manifest skill set does not exactly match this Softpowers pack")

    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
            raise RuntimeError("Malformed skill entry in install manifest")
        name = entry["name"]
        target = Path(str(entry.get("target", ""))).resolve(strict=False)
        assert_child(target, dest)
        if target != (dest / name).resolve(strict=False):
            raise RuntimeError(f"Manifest target does not match expected skill path for {name}: {target}")
        backup_value = entry.get("backup")
        if backup_value:
            backup = Path(str(backup_value)).resolve(strict=False)
            assert_child(backup, dest)
            if not path_exists(backup):
                raise RuntimeError(f"Required backup is missing: {backup}")

    stamp = timestamp_slug()
    staging = dest / f".softpowers-uninstall-staging-{stamp}"
    snapshots = dest / ".softpowers-uninstall-snapshots" / stamp
    staged_active: dict[str, Path] = {}
    restored_backups: dict[str, Path] = {}
    moved_snapshots: dict[str, Path] = {}
    original_pointer = pointer_path.read_text(encoding="utf-8") if pointer_path.is_file() else ""
    preserved: list[Path] = []
    committed = False

    try:
        staging.mkdir(parents=True, exist_ok=False)

        for entry in entries:
            name = entry["name"]
            target = Path(entry["target"])
            backup = Path(entry["backup"]) if entry.get("backup") else None

            if path_exists(target):
                staged = staging / name
                os.replace(target, staged)
                staged_active[name] = staged

            if backup is not None:
                os.replace(backup, target)
                restored_backups[name] = backup

        # Move edited installed skills to durable snapshots. This remains reversible
        # until the manifest is committed; unchanged copies stay in staging.
        for entry in entries:
            name = entry["name"]
            staged = staged_active.get(name)
            if staged is None:
                continue
            current_digest = directory_digest(staged)
            if current_digest != entry.get("installed_sha256"):
                snapshots.mkdir(parents=True, exist_ok=True)
                preserved_path = snapshots / name
                os.replace(staged, preserved_path)
                moved_snapshots[name] = preserved_path
                preserved.append(preserved_path)

        previous_manifest = manifest.get("previous_manifest")
        if previous_manifest and Path(str(previous_manifest)).is_file():
            atomic_write_text(pointer_path, str(previous_manifest) + "\n")
        elif pointer_path.exists():
            pointer_path.unlink()

        manifest["status"] = "uninstalled"
        manifest["uninstalled_at"] = datetime.now(timezone.utc).isoformat()
        manifest["preserved_modified_skills"] = [str(path) for path in preserved]
        atomic_write_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        committed = True

    except Exception:
        if not committed:
            # Return modified snapshots to staging before restoring active state.
            for name, snapshot in reversed(list(moved_snapshots.items())):
                staged = staging / name
                if path_exists(snapshot):
                    os.replace(snapshot, staged)

            # Remove any restored pre-install version back to its backup location.
            for entry in reversed(entries):
                name = entry["name"]
                target = Path(entry["target"])
                backup = Path(entry["backup"]) if entry.get("backup") else None
                if name in restored_backups and backup is not None and path_exists(target):
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(target, backup)

            # Restore the active installed version from uninstall staging.
            for name, staged in reversed(list(staged_active.items())):
                target_entry = next(item for item in entries if item["name"] == name)
                target = Path(target_entry["target"])
                if path_exists(staged):
                    os.replace(staged, target)

            if original_pointer:
                atomic_write_text(pointer_path, original_pointer)
            elif pointer_path.exists():
                pointer_path.unlink()

            if staging.exists():
                shutil.rmtree(staging, ignore_errors=True)
            if snapshots.exists() and not any(snapshots.iterdir()):
                snapshots.rmdir()
        raise

    # Post-commit cleanup cannot invalidate the restored active state.
    try:
        if staging.exists():
            shutil.rmtree(staging)

        backup_parents = {
            Path(entry["backup"]).parent
            for entry in entries
            if entry.get("backup")
        }
        for parent in backup_parents:
            if parent.exists() and not any(parent.iterdir()):
                parent.rmdir()

        backups_root = dest / ".softpowers-backups"
        if backups_root.exists() and not any(backups_root.iterdir()):
            backups_root.rmdir()

        snapshots_root = dest / ".softpowers-uninstall-snapshots"
        if snapshots.exists() and not any(snapshots.iterdir()):
            snapshots.rmdir()
        if snapshots_root.exists() and not any(snapshots_root.iterdir()):
            snapshots_root.rmdir()
    except OSError as exc:
        print(f"WARNING: uninstall succeeded but metadata cleanup was incomplete: {exc}", file=sys.stderr)

    return manifest_path, preserved


def main() -> int:
    parser = argparse.ArgumentParser(description="Uninstall Softpowers and restore replaced skills.")
    parser.add_argument("--dest", help="Override the Codex skills directory")
    parser.add_argument("--manifest", help="Use a specific install manifest instead of the current one")
    args = parser.parse_args()

    manifest = Path(args.manifest).expanduser() if args.manifest else None

    try:
        dest = resolve_skills_dir(args.dest)
        used_manifest, preserved = uninstall_pack(dest, manifest)
    except Exception as exc:
        print(f"Softpowers uninstall failed; active state was restored.\nERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Uninstalled Softpowers from {dest}")
    print(f"Manifest updated: {used_manifest}")
    if preserved:
        print("Modified installed skills were preserved at:")
        for path in preserved:
            print(f"- {path}")
    print("Any pre-install same-named skills recorded in the manifest were restored.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
