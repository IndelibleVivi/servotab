#!/usr/bin/env python3
"""Inspect or retire one manifest-owned global Softpowers layer.

The default command is read-only. Retirement requires both ``--retire`` and an
explicit ``--dest``. Remove this helper after every supported skill root has no
``.softpowers-current-manifest`` and the Servotab plugin migration is accepted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def path_exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def lexical_absolute(path: Path, label: str) -> Path:
    expanded = path.expanduser()
    if not expanded.is_absolute():
        raise RuntimeError(f"{label} must be an absolute path: {path}")
    return Path(os.path.normpath(os.fspath(expanded)))


def assert_lexical_child(path: Path, parent: Path, *, direct: bool = False) -> None:
    try:
        relative = path.relative_to(parent)
    except ValueError as exc:
        raise RuntimeError(f"path escapes allowed root {parent}: {path}") from exc
    if not relative.parts or (direct and len(relative.parts) != 1):
        raise RuntimeError(f"path is not an allowed child of {parent}: {path}")


def require_real_directory(path: Path, label: str) -> None:
    if path.is_symlink() or not path.is_dir():
        raise RuntimeError(f"{label} must be a real directory, not a symlink: {path}")


def require_real_parent_chain(path: Path, root: Path, label: str) -> None:
    """Require every existing parent from root through path.parent to be a real directory."""

    assert_lexical_child(path, root)
    require_real_directory(root, f"{label} root")
    current = root
    for part in path.relative_to(root).parts[:-1]:
        current = current / part
        require_real_directory(current, f"{label} parent")


def map_direct_child(path: Path, root: Path, label: str) -> Path:
    """Map an absolute legacy path alias to one direct child of a verified real root."""

    lexical = lexical_absolute(path, label)
    try:
        parent = lexical.parent.resolve(strict=True)
    except OSError as exc:
        raise RuntimeError(f"cannot resolve {label} parent: {lexical.parent}") from exc
    if parent != root:
        raise RuntimeError(f"{label} escapes allowed root {root}: {lexical}")
    mapped = root / lexical.name
    assert_lexical_child(mapped, root, direct=True)
    return mapped


def directory_digest(path: Path) -> str:
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
    for item in sorted(path.rglob("*"), key=lambda value: value.relative_to(path).as_posix()):
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


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw_temp = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp = Path(raw_temp)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def current_manifest_path(dest: Path) -> Path | None:
    pointer = dest / ".softpowers-current-manifest"
    if not path_exists(pointer):
        return None
    if pointer.is_symlink() or not pointer.is_file():
        raise RuntimeError(f"legacy manifest pointer is not a regular file: {pointer}")
    manifests_root = dest / ".softpowers-manifests"
    require_real_directory(manifests_root, "legacy manifest directory")
    raw = pointer.read_text(encoding="utf-8").strip()
    if not raw:
        raise RuntimeError(f"legacy manifest pointer is empty: {pointer}")
    manifest_path = map_direct_child(Path(raw), manifests_root, "legacy manifest path")
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise RuntimeError(f"legacy manifest is missing or not a regular file: {manifest_path}")
    return manifest_path


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot read legacy install manifest: {path}") from exc
    if (
        not isinstance(data, dict)
        or data.get("schema_version") != 1
        or data.get("pack") != "softpowers-pack"
        or data.get("status") != "installed"
        or not isinstance(data.get("skills"), list)
    ):
        raise RuntimeError(f"unsupported legacy install manifest: {path}")
    if "previous_manifest" not in data:
        raise RuntimeError(f"legacy install manifest is missing previous_manifest: {path}")
    return data


def validated_entries(manifest: dict[str, Any], dest: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    names: set[str] = set()
    backups: set[Path] = set()
    backup_root = dest / ".softpowers-backups"
    declared_dest = lexical_absolute(
        Path(str(manifest.get("destination", ""))), "legacy manifest destination"
    )
    try:
        resolved_declared_dest = declared_dest.resolve(strict=True)
    except OSError as exc:
        raise RuntimeError(f"cannot resolve legacy manifest destination: {declared_dest}") from exc
    if resolved_declared_dest != dest:
        raise RuntimeError(f"legacy manifest destination {declared_dest} does not match {dest}")
    declared_backup_root = declared_dest / ".softpowers-backups"
    for raw in manifest["skills"]:
        if not isinstance(raw, dict) or not isinstance(raw.get("name"), str):
            raise RuntimeError("malformed skill entry in legacy install manifest")
        name = raw["name"]
        if not name or Path(name).name != name or name.startswith(".") or name in names:
            raise RuntimeError(f"unsafe or duplicate legacy skill name: {name!r}")
        names.add(name)

        target_raw = raw.get("target")
        if not isinstance(target_raw, str) or not target_raw:
            raise RuntimeError(f"malformed target for legacy skill {name}")
        declared_target = lexical_absolute(Path(target_raw), f"target for legacy skill {name}")
        if declared_target != declared_dest / name:
            raise RuntimeError(f"legacy target does not match expected skill path: {declared_target}")
        target = dest / name

        digest = raw.get("installed_sha256")
        if (
            not isinstance(digest, str)
            or len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
        ):
            raise RuntimeError(f"invalid installed digest for legacy skill {name}")

        backup: Path | None = None
        backup_raw = raw.get("backup")
        if backup_raw is not None:
            if not isinstance(backup_raw, str) or not backup_raw:
                raise RuntimeError(f"malformed backup for legacy skill {name}")
            declared_backup = lexical_absolute(
                Path(backup_raw), f"backup for legacy skill {name}"
            )
            try:
                backup_relative = declared_backup.relative_to(declared_backup_root)
            except ValueError as exc:
                raise RuntimeError(
                    f"backup for legacy skill {name} escapes {declared_backup_root}: "
                    f"{declared_backup}"
                ) from exc
            if not backup_relative.parts:
                raise RuntimeError(f"backup for legacy skill {name} is not a child path")
            backup = backup_root / backup_relative
            require_real_parent_chain(backup, backup_root, f"backup for legacy skill {name}")
            if backup in backups or not path_exists(backup):
                raise RuntimeError(f"missing or duplicate legacy backup: {backup}")
            backups.add(backup)
        entries.append({**raw, "target": str(target), "backup": str(backup) if backup else None})
    if not entries:
        raise RuntimeError("legacy install manifest contains no skills")
    return entries


def manifest_destination(manifest: dict[str, Any]) -> Path:
    raw = manifest.get("destination")
    if not isinstance(raw, str) or not raw:
        raise RuntimeError("legacy install manifest has no valid destination")
    lexical = lexical_absolute(Path(raw), "legacy manifest destination")
    try:
        return lexical.resolve(strict=True)
    except OSError as exc:
        raise RuntimeError(f"cannot resolve legacy manifest destination: {lexical}") from exc


def previous_manifest_path(manifest: dict[str, Any], dest: Path) -> Path | None:
    raw = manifest.get("previous_manifest")
    if raw is None:
        return None
    if not isinstance(raw, str) or not raw:
        raise RuntimeError("malformed previous legacy manifest path")
    manifests_root = dest / ".softpowers-manifests"
    require_real_directory(manifests_root, "legacy manifest directory")
    previous = map_direct_child(Path(raw), manifests_root, "previous legacy manifest path")
    if previous.is_symlink() or not previous.is_file():
        raise RuntimeError(f"previous legacy manifest is missing or not a regular file: {previous}")
    return previous


def validate_manifest_chain(
    manifest_path: Path, dest: Path
) -> tuple[dict[str, Any], list[dict[str, Any]], Path | None]:
    """Validate the complete predecessor chain before any retirement mutation."""

    seen: set[Path] = set()
    current = manifest_path
    first_manifest: dict[str, Any] | None = None
    first_entries: list[dict[str, Any]] | None = None
    first_previous: Path | None = None
    while True:
        if current in seen:
            raise RuntimeError(f"cycle in legacy manifest chain at {current}")
        seen.add(current)
        manifest = load_manifest(current)
        if manifest_destination(manifest) != dest:
            raise RuntimeError(
                f"legacy manifest destination {manifest_destination(manifest)} does not match {dest}"
            )
        entries = validated_entries(manifest, dest)
        previous = previous_manifest_path(manifest, dest)
        if first_manifest is None:
            first_manifest = manifest
            first_entries = entries
            first_previous = previous
        if previous is None:
            break
        current = previous
    assert first_manifest is not None and first_entries is not None
    return first_manifest, first_entries, first_previous


def inspect_root(dest: Path) -> dict[str, Any] | None:
    dest = dest.expanduser().resolve()
    manifest_path = current_manifest_path(dest)
    if manifest_path is None:
        return None
    manifest, entries, previous = validate_manifest_chain(manifest_path, dest)
    modified = [
        entry["name"]
        for entry in entries
        if path_exists(Path(entry["target"]))
        and directory_digest(Path(entry["target"])) != entry["installed_sha256"]
    ]
    return {
        "destination": str(dest),
        "manifest": str(manifest_path),
        "version": manifest.get("version"),
        "skills": [entry["name"] for entry in entries],
        "modified_skills": modified,
        "previous_manifest": str(previous) if previous else None,
    }


def retire_current_layer(dest: Path) -> tuple[Path, list[Path]]:
    dest = dest.expanduser().resolve()
    pointer = dest / ".softpowers-current-manifest"
    manifest_path = current_manifest_path(dest)
    if manifest_path is None:
        raise RuntimeError(f"no legacy manifest pointer at {pointer}")
    manifest, entries, previous_path = validate_manifest_chain(manifest_path, dest)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    staging = dest / f".softpowers-retire-staging-{stamp}"
    snapshot_root = dest / ".softpowers-retire-snapshots"
    snapshots = snapshot_root / stamp
    staged_active: dict[str, Path] = {}
    restored_backups: dict[str, Path] = {}
    moved_snapshots: dict[str, Path] = {}
    original_pointer = pointer.read_text(encoding="utf-8")
    preserved: list[Path] = []
    committed = False
    created_snapshot_root = False

    if path_exists(snapshot_root):
        require_real_directory(snapshot_root, "legacy retirement snapshot directory")

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

        for entry in entries:
            name = entry["name"]
            staged = staged_active.get(name)
            if staged is None or directory_digest(staged) == entry["installed_sha256"]:
                continue
            if not path_exists(snapshot_root):
                snapshot_root.mkdir(parents=False, exist_ok=False)
                created_snapshot_root = True
            else:
                require_real_directory(snapshot_root, "legacy retirement snapshot directory")
            if not path_exists(snapshots):
                snapshots.mkdir(parents=False, exist_ok=False)
            elif snapshots.is_symlink() or not snapshots.is_dir():
                raise RuntimeError(f"unsafe legacy retirement snapshot path: {snapshots}")
            preserved_path = snapshots / name
            os.replace(staged, preserved_path)
            moved_snapshots[name] = preserved_path
            preserved.append(preserved_path)

        if previous_path is not None:
            refreshed_previous = previous_manifest_path(manifest, dest)
            if refreshed_previous != previous_path:
                raise RuntimeError("previous legacy manifest identity changed during retirement")
            validate_manifest_chain(previous_path, dest)
            atomic_write_text(pointer, str(previous_path) + "\n")
        else:
            pointer.unlink()
        manifest["status"] = "uninstalled"
        manifest["uninstalled_at"] = datetime.now(timezone.utc).isoformat()
        manifest["preserved_modified_skills"] = [str(path) for path in preserved]
        atomic_write_text(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        committed = True
    except Exception:
        if not committed:
            for name, snapshot in reversed(list(moved_snapshots.items())):
                if path_exists(snapshot):
                    os.replace(snapshot, staging / name)
            for entry in reversed(entries):
                name = entry["name"]
                target = Path(entry["target"])
                backup = Path(entry["backup"]) if entry.get("backup") else None
                if name in restored_backups and backup is not None and path_exists(target):
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(target, backup)
            for name, staged in reversed(list(staged_active.items())):
                target = next(Path(item["target"]) for item in entries if item["name"] == name)
                if path_exists(staged):
                    os.replace(staged, target)
            atomic_write_text(pointer, original_pointer)
            shutil.rmtree(staging, ignore_errors=True)
            if snapshots.is_dir() and not snapshots.is_symlink():
                shutil.rmtree(snapshots)
            if created_snapshot_root and snapshot_root.is_dir() and not any(snapshot_root.iterdir()):
                snapshot_root.rmdir()
        raise

    shutil.rmtree(staging, ignore_errors=True)
    return manifest_path, preserved


def default_roots() -> tuple[Path, Path]:
    return (Path.home() / ".agents" / "skills", Path.home() / ".codex" / "skills")


def main() -> int:
    removal_condition = (
        "Removal condition: delete this helper after supported roots have no active "
        ".softpowers-current-manifest and the Servotab plugin migration is accepted."
    )
    parser = argparse.ArgumentParser(
        description="Read-only legacy Softpowers ownership check, with explicit one-layer retirement.",
        epilog=removal_condition,
    )
    parser.add_argument("--dest", help="Exact legacy skills root to inspect")
    parser.add_argument(
        "--retire",
        action="store_true",
        help="Retire one current manifest layer; requires an explicit --dest",
    )
    args = parser.parse_args()
    if args.retire and not args.dest:
        parser.error("--retire requires an explicit --dest")

    roots = (Path(args.dest),) if args.dest else default_roots()
    try:
        reports = [(root.expanduser().resolve(), inspect_root(root)) for root in roots]
    except Exception as exc:
        print(f"Legacy ownership check failed: {exc}", file=sys.stderr)
        return 1

    if not args.retire:
        active = 0
        for root, report in reports:
            if report is None:
                print(f"CLEAR {root}: no active legacy manifest")
                continue
            active += 1
            print(
                f"ACTIVE {root}: version={report['version']}, skills={len(report['skills'])}, "
                f"modified={len(report['modified_skills'])}"
            )
            print(f"  manifest: {report['manifest']}")
            print(f"  previous layer: {report['previous_manifest'] or 'none'}")
        print(removal_condition)
        return 2 if active else 0

    dest = Path(args.dest).expanduser().resolve()
    try:
        manifest_path, preserved = retire_current_layer(dest)
    except Exception as exc:
        print(f"Legacy layer retirement failed; prior state was restored. ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Retired one manifest-owned Softpowers layer from {dest}")
    print(f"Manifest updated: {manifest_path}")
    for path in preserved:
        print(f"Preserved modified installed skill: {path}")
    next_report = inspect_root(dest)
    if next_report is not None:
        print("Another legacy manifest layer is now current; run a fresh read-only preflight before retiring it.")
    else:
        print("No active legacy manifest remains in this root.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
