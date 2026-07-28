#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from build_skills import check as check_generated
from common import PACK_ROOT, ROUTER_NAME, SKILL_NAMES, VERSION
from runtime_validate import EXPECTED_PAYLOAD_FILES, file_sha256
from validate import validate_directory


def build_manifest() -> dict[str, object]:
    skills_dir = PACK_ROOT / "skills"
    sync_errors = check_generated()
    if sync_errors:
        raise RuntimeError("generated-skill sync failed:\n- " + "\n- ".join(sync_errors))

    errors = validate_directory(skills_dir, exact=True)
    if errors:
        raise RuntimeError("YAML/source validation failed:\n- " + "\n- ".join(errors))

    files: list[dict[str, object]] = []
    for relative_text in sorted(EXPECTED_PAYLOAD_FILES):
        relative = Path(relative_text)
        absolute = PACK_ROOT / relative
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
        "schema_version": 2,
        "pack": "softpowers-pack",
        "version": VERSION,
        "skills": list(SKILL_NAMES),
        "activation": {
            "implicit": [ROUTER_NAME],
            "explicit_only": [name for name in SKILL_NAMES if name != ROUTER_NAME],
        },
        "files": files,
    }


def serialized_manifest() -> str:
    return json.dumps(build_manifest(), indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate or verify PACK_MANIFEST.json after sync and real YAML validation."
    )
    parser.add_argument("--check", action="store_true", help="Verify the committed manifest is current")
    args = parser.parse_args()

    manifest_path = PACK_ROOT / "PACK_MANIFEST.json"
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
        print("PACK_MANIFEST.json matches the synced, YAML-validated skill payload.")
        return 0

    manifest_path.write_text(expected, encoding="utf-8")
    print(f"Wrote {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
