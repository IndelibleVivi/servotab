#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from build_skills import check as check_generated
from runtime_validate import (
    EXPECTED_PAYLOAD_FILES,
    PLUGIN_RELATIVE,
    ROOT,
    VERSION,
    file_sha256,
    validate_marketplace,
    validate_plugin_manifest,
)
from skill_catalog import IMPLICIT_SKILL_NAMES, SKILL_NAMES
from validate import validate_directory


def build_manifest(root: Path = ROOT) -> dict[str, object]:
    sync_errors = check_generated(root)
    if sync_errors:
        raise RuntimeError("source/generated sync failed:\n- " + "\n- ".join(sync_errors))

    skills_dir = root / PLUGIN_RELATIVE / "skills"
    skill_errors = validate_directory(skills_dir, exact=True)
    if skill_errors:
        raise RuntimeError("skill validation failed:\n- " + "\n- ".join(skill_errors))
    contract_errors = validate_plugin_manifest(root) + validate_marketplace(root)
    if contract_errors:
        raise RuntimeError("plugin contract validation failed:\n- " + "\n- ".join(contract_errors))

    files: list[dict[str, object]] = []
    for relative_text in sorted(EXPECTED_PAYLOAD_FILES):
        relative = Path(relative_text)
        absolute = root / relative
        if not absolute.is_file() or absolute.is_symlink():
            raise RuntimeError(f"invalid payload file: {relative.as_posix()}")
        files.append(
            {
                "path": relative.as_posix(),
                "size": absolute.stat().st_size,
                "sha256": file_sha256(absolute),
            }
        )

    return {
        "schema_version": 1,
        "pack": "servotab",
        "version": (root / "VERSION").read_text(encoding="utf-8").strip(),
        "plugin": PLUGIN_RELATIVE.as_posix(),
        "skills": list(SKILL_NAMES),
        "activation": {
            "implicit": list(IMPLICIT_SKILL_NAMES),
            "explicit_only": [
                name for name in SKILL_NAMES if name not in IMPLICIT_SKILL_NAMES
            ],
        },
        "files": files,
    }


def serialized_manifest(root: Path = ROOT) -> str:
    return json.dumps(build_manifest(root), indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate or verify PACK_MANIFEST.json for the Servotab plugin package."
    )
    parser.add_argument("--check", action="store_true", help="Verify the committed manifest")
    args = parser.parse_args()
    manifest_path = ROOT / "PACK_MANIFEST.json"
    try:
        expected = serialized_manifest()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.check:
        try:
            current = manifest_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"ERROR: missing {manifest_path}", file=sys.stderr)
            return 1
        if current != expected:
            print("ERROR: PACK_MANIFEST.json is stale; regenerate it.", file=sys.stderr)
            return 1
        print("PACK_MANIFEST.json matches the validated Servotab plugin payload.")
        return 0

    manifest_path.write_text(expected, encoding="utf-8")
    print(f"Wrote {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
