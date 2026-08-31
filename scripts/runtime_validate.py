#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import unicodedata
from pathlib import Path
from typing import Any

from skill_catalog import IMPLICIT_SKILL_NAMES, REFERENCE_METHOD_NAMES, SKILL_NAMES

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
PUBLISHER_NAME = "Yifei Fang"
PLUGIN_RELATIVE = Path("plugins/servotab")
PLUGIN_ROOT = ROOT / PLUGIN_RELATIVE
PACK_MANIFEST = ROOT / "PACK_MANIFEST.json"
MARKETPLACE = ROOT / ".agents/plugins/marketplace.json"
ASSET_NAMES = ("composer-icon.png", "logo.png")
LEGAL_FILES = ("LICENSE", "NOTICE.md")
RETIRED_METHOD_FILES = ("brainstorm.md", "receive-review.md", "parallel.md")
RETIRED_REPO_PATHS = (
    "skills",
    "install.sh",
    "uninstall.sh",
    "scripts/install.py",
    "scripts/uninstall.py",
)


def expected_payload_files() -> frozenset[str]:
    files = {f"plugins/servotab/.codex-plugin/plugin.json"}
    files |= {f"plugins/servotab/{name}" for name in LEGAL_FILES}
    files |= {f"plugins/servotab/assets/{name}" for name in ASSET_NAMES}
    files |= {
        f"plugins/servotab/skills/{name}/SKILL.md" for name in SKILL_NAMES
    }
    files |= {
        f"plugins/servotab/skills/{name}/agents/openai.yaml" for name in SKILL_NAMES
    }
    files |= {
        f"plugins/servotab/skills/servotab/references/{name}.md"
        for name in REFERENCE_METHOD_NAMES
    }
    return frozenset(files)


EXPECTED_PAYLOAD_FILES = expected_payload_files()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"missing {label}: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid {label} JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} root must be an object")
    return value


def load_pack_manifest(path: Path = PACK_MANIFEST) -> dict[str, Any]:
    data = load_json_object(path, "pack manifest")
    if data.get("schema_version") != 1:
        raise ValueError(f"unsupported pack manifest schema: {data.get('schema_version')!r}")
    if data.get("pack") != "servotab":
        raise ValueError(f"unexpected pack id: {data.get('pack')!r}")
    if data.get("version") != VERSION:
        raise ValueError(
            f"pack manifest version {data.get('version')!r} does not match VERSION {VERSION!r}"
        )
    if data.get("plugin") != PLUGIN_RELATIVE.as_posix():
        raise ValueError("pack manifest plugin path must be plugins/servotab")
    if data.get("skills") != list(SKILL_NAMES):
        raise ValueError("pack manifest skill order/set does not match the catalog")
    expected_activation = {
        "implicit": list(IMPLICIT_SKILL_NAMES),
        "explicit_only": [name for name in SKILL_NAMES if name not in IMPLICIT_SKILL_NAMES],
    }
    if data.get("activation") != expected_activation:
        raise ValueError("pack manifest activation contract does not match the catalog")

    files = data.get("files")
    if not isinstance(files, list):
        raise ValueError("pack manifest files must be a list")
    seen: set[str] = set()
    for entry in files:
        if not isinstance(entry, dict) or set(entry) != {"path", "size", "sha256"}:
            raise ValueError("pack manifest file entries require path, size, and sha256")
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
        raise ValueError(f"pack manifest payload set mismatch; missing={missing}, extra={extra}")
    return data


def validate_plugin_manifest(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    plugin_root = root / PLUGIN_RELATIVE
    try:
        manifest = load_json_object(plugin_root / ".codex-plugin/plugin.json", "plugin manifest")
    except ValueError as exc:
        return [str(exc)]

    if manifest.get("name") != "servotab":
        errors.append("plugin manifest name must be servotab")
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if manifest.get("version") != version:
        errors.append("plugin manifest version must match VERSION")
    if manifest.get("skills") != "./skills/":
        errors.append("plugin manifest skills path must be ./skills/")
    if manifest.get("description") != "A quiet, risk-scaled engineering method layer for Codex.":
        errors.append("plugin manifest description drifted from the product contract")
    expected_public_urls = {
        "homepage": "https://servotab.com",
        "repository": "https://github.com/IndelibleVivi/servotab",
    }
    for field, expected in expected_public_urls.items():
        if manifest.get(field) != expected:
            errors.append(f"plugin manifest {field} must be {expected!r}")
    for name in LEGAL_FILES:
        if not (plugin_root / name).is_file():
            errors.append(f"plugin package is missing {name}")
    author = manifest.get("author")
    if not isinstance(author, dict):
        errors.append("plugin manifest author must be an object")
    else:
        if author.get("name") != PUBLISHER_NAME:
            errors.append(f"plugin manifest author.name must be {PUBLISHER_NAME!r}")
        if author.get("url") != "https://servotab.com":
            errors.append("plugin manifest author.url must be 'https://servotab.com'")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        return errors + ["plugin manifest interface must be an object"]
    expected_values = {
        "displayName": "Servotab",
        "shortDescription": "Risk-scaled repository methods",
        "developerName": PUBLISHER_NAME,
        "websiteURL": "https://servotab.com",
        "supportURL": "https://servotab.com/support",
        "privacyPolicyURL": "https://servotab.com/privacy",
        "termsOfServiceURL": "https://servotab.com/terms",
        "brandColor": "#315EFB",
        "composerIcon": "./assets/composer-icon.png",
        "logo": "./assets/logo.png",
    }
    for field, expected in expected_values.items():
        if interface.get(field) != expected:
            errors.append(f"plugin manifest interface.{field} must be {expected!r}")
    long_description = interface.get("longDescription")
    if not isinstance(long_description, str) or not long_description.strip():
        errors.append("plugin manifest interface.longDescription must be non-empty")
    elif len(long_description) > 4000:
        errors.append("plugin manifest interface.longDescription must be no longer than 4000 characters")
    short_description = interface.get("shortDescription")
    if isinstance(short_description, str) and len(short_description) > 30:
        errors.append(
            "plugin manifest interface.shortDescription must be no longer than "
            "30 characters for final directory submission"
        )
    default_prompts = interface.get("defaultPrompt")
    if (
        not isinstance(default_prompts, list)
        or not 1 <= len(default_prompts) <= 3
        or any(
            not isinstance(prompt, str)
            or not prompt.strip()
            or len(prompt) > 128
            or "\n" in prompt
            or "\r" in prompt
            for prompt in default_prompts
        )
    ):
        errors.append(
            "plugin manifest interface.defaultPrompt must be an array of 1-3 "
            "non-empty single-line strings no longer than 128 characters"
        )
    elif not any("$servotab" in prompt for prompt in default_prompts):
        errors.append("plugin manifest defaultPrompt must invoke $servotab")
    else:
        normalized_prompts = [
            " ".join(unicodedata.normalize("NFKC", prompt).split())
            for prompt in default_prompts
        ]
        if len(normalized_prompts) != len(set(normalized_prompts)):
            errors.append("plugin manifest defaultPrompt entries must be unique")
        if any("@" in prompt for prompt in default_prompts):
            errors.append("plugin manifest defaultPrompt must not contain app @mentions")
    if "logoDark" in interface:
        errors.append("plugin manifest interface.logoDark must remain omitted until dark-mode acceptance")
    for field in ("composerIcon", "logo"):
        raw = interface.get(field)
        if isinstance(raw, str) and not (plugin_root / raw).is_file():
            errors.append(f"plugin manifest interface.{field} points to a missing file")
    return errors


def validate_marketplace(root: Path = ROOT) -> list[str]:
    try:
        marketplace = load_json_object(root / ".agents/plugins/marketplace.json", "marketplace")
    except ValueError as exc:
        return [str(exc)]
    errors: list[str] = []
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        return ["repo marketplace must contain exactly one Servotab entry"]
    entry = plugins[0]
    expected = {
        "name": "servotab",
        "source": {"source": "local", "path": "./plugins/servotab"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Developer Tools",
    }
    if entry != expected:
        errors.append("repo marketplace Servotab entry does not match the package contract")
    interface = marketplace.get("interface")
    if not isinstance(interface, dict) or interface.get("displayName") != "Servotab":
        errors.append("repo marketplace displayName must be Servotab")
    return errors


def validate_package(
    root: Path = ROOT,
    *,
    manifest_path: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    manifest_path = manifest_path or root / "PACK_MANIFEST.json"
    try:
        manifest = load_pack_manifest(manifest_path)
    except ValueError as exc:
        return [str(exc)]

    entries = {entry["path"]: entry for entry in manifest["files"]}
    for relative in sorted(EXPECTED_PAYLOAD_FILES):
        path = root / relative
        if path.is_symlink():
            errors.append(f"package payload must not contain symlinks: {relative}")
            continue
        if not path.is_file():
            errors.append(f"missing package payload file: {relative}")
            continue
        entry = entries[relative]
        if path.stat().st_size != entry["size"]:
            errors.append(f"size mismatch for {relative}")
        elif file_sha256(path) != entry["sha256"]:
            errors.append(f"sha256 mismatch for {relative}")

    errors.extend(validate_plugin_manifest(root))
    errors.extend(validate_marketplace(root))
    for relative in RETIRED_REPO_PATHS:
        if (root / relative).exists():
            errors.append(f"retired global-skill path still exists: {relative}")
    for name in RETIRED_METHOD_FILES:
        if (root / "methods" / name).exists():
            errors.append(f"retired canonical method id still exists: {name}")
    return errors
