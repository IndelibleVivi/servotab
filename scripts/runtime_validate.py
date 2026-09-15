#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata
from pathlib import Path
from typing import Any

from skill_catalog import IMPLICIT_SKILL_NAMES, REFERENCE_METHOD_NAMES, SKILL_NAMES

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
PUBLISHER_NAME = "Yifei Fang"
PLUGIN_RELATIVE = Path("plugins/servotab")
PLUGIN_ROOT = ROOT / PLUGIN_RELATIVE
PORTABLE_PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
PORTABLE_PLUGIN_MANIFEST = PLUGIN_RELATIVE / "plugin.json"
COMPAT_PLUGIN_MANIFEST = PLUGIN_RELATIVE / ".codex-plugin/plugin.json"
PACK_MANIFEST = ROOT / "PACK_MANIFEST.json"
MARKETPLACE = ROOT / ".agents/plugins/marketplace.json"
ASSET_NAMES = ("composer-icon.png", "logo.png")
SKILL_ICON_NAMES = ("icon.svg", "icon-400.png")
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
    files = {PORTABLE_PLUGIN_MANIFEST.as_posix(), COMPAT_PLUGIN_MANIFEST.as_posix()}
    files |= {f"plugins/servotab/{name}" for name in LEGAL_FILES}
    files |= {f"plugins/servotab/assets/{name}" for name in ASSET_NAMES}
    files |= {
        f"plugins/servotab/skills/{name}/SKILL.md" for name in SKILL_NAMES
    }
    files |= {
        f"plugins/servotab/skills/{name}/agents/openai.yaml" for name in SKILL_NAMES
    }
    files |= {
        f"plugins/servotab/skills/{name}/assets/{asset}"
        for name in SKILL_NAMES
        for asset in SKILL_ICON_NAMES
    }
    files |= {
        f"plugins/servotab/skills/servotab/references/{name}.md"
        for name in REFERENCE_METHOD_NAMES
    }
    return frozenset(files)


EXPECTED_PAYLOAD_FILES = expected_payload_files()
BINARY_PAYLOAD_SUFFIXES = frozenset({".png"})


def payload_bytes(path: Path) -> bytes:
    """Read one payload file in its canonical package representation.

    Text payloads are canonically LF. This lets package verification remain
    truthful in Windows worktrees that still contain CRLF from an earlier
    checkout, while PNG assets retain strict byte identity.
    """
    data = path.read_bytes()
    if path.suffix.lower() in BINARY_PAYLOAD_SUFFIXES:
        return data
    return data.replace(b"\r\n", b"\n")


def payload_size(path: Path) -> int:
    return len(payload_bytes(path))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(payload_bytes(path)).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("non-finite JSON number")


def finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("non-finite JSON number")
    return number


def load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object, parse_constant=reject_constant, parse_float=finite_float)
    except FileNotFoundError as exc:
        raise ValueError(f"missing {label}: {path}") from exc
    except (ValueError, UnicodeError) as exc:
        raise ValueError(f"invalid {label} JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} root must be an object")
    return value


def load_pack_manifest(path: Path = PACK_MANIFEST) -> dict[str, Any]:
    data = load_json_object(path, "pack manifest")
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
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
        if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
            raise ValueError(f"invalid sha256 for {relative}")
        if type(size) is not int or size < 0:
            raise ValueError(f"invalid size for {relative}")
        seen.add(relative)
    if seen != EXPECTED_PAYLOAD_FILES:
        missing = sorted(EXPECTED_PAYLOAD_FILES - seen)
        extra = sorted(seen - EXPECTED_PAYLOAD_FILES)
        raise ValueError(f"pack manifest payload set mismatch; missing={missing}, extra={extra}")
    return data


def _validate_plugin_identity(
    manifest: dict[str, Any],
    *,
    root: Path,
    label: str,
) -> list[str]:
    errors: list[str] = []
    if manifest.get("name") != "servotab":
        errors.append(f"{label} name must be servotab")
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if manifest.get("version") != version:
        errors.append(f"{label} version must match VERSION")
    if manifest.get("description") != "A quiet, risk-scaled engineering method layer for Codex.":
        errors.append(f"{label} description drifted from the product contract")
    expected_public_urls = {
        "homepage": "https://servotab.com",
        "repository": "https://github.com/IndelibleVivi/servotab",
    }
    for field, expected in expected_public_urls.items():
        if manifest.get(field) != expected:
            errors.append(f"{label} {field} must be {expected!r}")
    author = manifest.get("author")
    if not isinstance(author, dict):
        errors.append(f"{label} author must be an object")
    else:
        if set(author) != {"name", "url"}:
            errors.append(f"{label} author must contain exactly name and url")
        if author.get("name") != PUBLISHER_NAME:
            errors.append(f"{label} author.name must be {PUBLISHER_NAME!r}")
        if author.get("url") != "https://servotab.com":
            errors.append(f"{label} author.url must be 'https://servotab.com'")
    keywords = manifest.get("keywords")
    if keywords != ["codex", "engineering", "methods", "verification"]:
        errors.append(f"{label} keywords drifted from the package contract")
    return errors


def _validate_plugin_interface(
    interface: object,
    *,
    plugin_root: Path,
    label: str,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(interface, dict):
        return [f"{label} interface must be an object"]
    expected_values = {
        "displayName": "Servotab",
        "shortDescription": "Risk-scaled repository methods",
        "developerName": PUBLISHER_NAME,
        "category": "Developer Tools",
        "capabilities": [
            "Repository engineering",
            "Risk-scaled methods",
            "Fresh verification",
        ],
        "websiteURL": "https://servotab.com",
        "supportURL": "https://servotab.com/support",
        "privacyPolicyURL": "https://servotab.com/privacy",
        "termsOfServiceURL": "https://servotab.com/terms",
        "brandColor": "#315EFB",
        "composerIcon": "./assets/composer-icon.png",
        "logo": "./assets/logo.png",
    }
    allowed_fields = set(expected_values) | {"longDescription", "defaultPrompt"}
    if set(interface) != allowed_fields:
        errors.append(f"{label} interface must contain exactly the approved listing fields")
    for field, expected in expected_values.items():
        if interface.get(field) != expected:
            errors.append(f"{label} interface.{field} must be {expected!r}")

    display_name = interface.get("displayName")
    if isinstance(display_name, str) and len(display_name) > 30:
        errors.append(
            f"{label} interface.displayName must be no longer than 30 characters "
            "for final directory submission"
        )
    long_description = interface.get("longDescription")
    if not isinstance(long_description, str) or not long_description.strip():
        errors.append(f"{label} interface.longDescription must be non-empty")
    elif len(long_description) > 4000:
        errors.append(
            f"{label} interface.longDescription must be no longer than 4000 characters"
        )
    short_description = interface.get("shortDescription")
    if isinstance(short_description, str) and len(short_description) > 30:
        errors.append(
            f"{label} interface.shortDescription must be no longer than "
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
            f"{label} interface.defaultPrompt must be an array of 1-3 "
            "non-empty single-line strings no longer than 128 characters"
        )
    elif not any("$servotab" in prompt for prompt in default_prompts):
        errors.append(f"{label} defaultPrompt must invoke $servotab")
    else:
        normalized_prompts = [
            " ".join(unicodedata.normalize("NFKC", prompt).split())
            for prompt in default_prompts
        ]
        if len(normalized_prompts) != len(set(normalized_prompts)):
            errors.append(f"{label} defaultPrompt entries must be unique")
        if any("@" in prompt for prompt in default_prompts):
            errors.append(f"{label} defaultPrompt must not contain app @mentions")

    for field in ("composerIcon", "logo"):
        raw = interface.get(field)
        if isinstance(raw, str) and not (plugin_root / raw).is_file():
            errors.append(f"{label} interface.{field} points to a missing file")
    return errors


def validate_plugin_manifest(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    plugin_root = root / PLUGIN_RELATIVE
    for name in LEGAL_FILES:
        if not (plugin_root / name).is_file():
            errors.append(f"plugin package is missing {name}")

    try:
        portable = load_json_object(
            root / PORTABLE_PLUGIN_MANIFEST, "portable plugin manifest"
        )
    except ValueError as exc:
        return errors + [str(exc)]
    portable_allowed = {
        "$schema",
        "name",
        "version",
        "description",
        "author",
        "homepage",
        "repository",
        "keywords",
        "extensions",
    }
    if set(portable) != portable_allowed:
        errors.append(
            "portable plugin manifest must contain exactly the Agent Plugins "
            "identity and OpenAI extension fields"
        )
    if portable.get("$schema") != PORTABLE_PLUGIN_SCHEMA:
        errors.append("portable plugin manifest must declare the Agent Plugins 1.0 schema")
    errors.extend(
        _validate_plugin_identity(portable, root=root, label="portable plugin manifest")
    )
    extensions = portable.get("extensions")
    if not isinstance(extensions, dict) or set(extensions) != {"com.openai"}:
        errors.append("portable plugin manifest extensions must contain only com.openai")
        portable_interface: object = None
    else:
        openai_extension = extensions.get("com.openai")
        if not isinstance(openai_extension, dict) or set(openai_extension) != {"interface"}:
            errors.append(
                "portable plugin manifest extensions.com.openai must contain only interface"
            )
            portable_interface = None
        else:
            portable_interface = openai_extension.get("interface")
    errors.extend(
        _validate_plugin_interface(
            portable_interface,
            plugin_root=plugin_root,
            label="portable plugin manifest",
        )
    )

    try:
        compatibility = load_json_object(
            root / COMPAT_PLUGIN_MANIFEST, "compatibility plugin manifest"
        )
    except ValueError as exc:
        return errors + [str(exc)]
    compatibility_allowed = {
        "name",
        "version",
        "description",
        "author",
        "homepage",
        "repository",
        "keywords",
        "skills",
        "interface",
    }
    if set(compatibility) != compatibility_allowed:
        errors.append(
            "compatibility plugin manifest must contain exactly the skills-only "
            "fallback fields"
        )
    if compatibility.get("skills") != "./skills/":
        errors.append("compatibility plugin manifest skills path must be ./skills/")
    errors.extend(
        _validate_plugin_identity(
            compatibility, root=root, label="compatibility plugin manifest"
        )
    )
    compatibility_interface = compatibility.get("interface")
    errors.extend(
        _validate_plugin_interface(
            compatibility_interface,
            plugin_root=plugin_root,
            label="compatibility plugin manifest",
        )
    )

    identity_fields = (
        "name",
        "version",
        "description",
        "author",
        "homepage",
        "repository",
        "keywords",
    )
    if any(portable.get(field) != compatibility.get(field) for field in identity_fields):
        errors.append(
            "portable and compatibility plugin manifests must carry identical identity metadata"
        )
    if portable_interface != compatibility_interface:
        errors.append(
            "portable OpenAI interface and compatibility plugin interface must be identical"
        )
    return errors


def validate_marketplace(root: Path = ROOT) -> list[str]:
    try:
        marketplace = load_json_object(root / ".agents/plugins/marketplace.json", "marketplace")
    except ValueError as exc:
        return [str(exc)]
    errors: list[str] = []
    if set(marketplace) != {"name", "interface", "plugins"} or marketplace.get("name") != "personal":
        errors.append("repo marketplace name and fields must match personal")
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

    plugin = root / PLUGIN_RELATIVE
    expected_directories = {
        parent.as_posix()
        for relative in EXPECTED_PAYLOAD_FILES
        for parent in Path(relative).parents
        if parent.as_posix().startswith("plugins/servotab")
    }
    # Inspect lexical paths before following any expected file or its parents.
    for parent in (root / "plugins", plugin):
        if parent.is_symlink():
            return ["package directory must not be a symlink"]
    for path in plugin.rglob("*"):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            errors.append(f"package payload must not contain symlinks: {relative}")
        elif path.is_dir():
            if relative not in expected_directories:
                errors.append(f"unexpected package directory: {relative}")
        elif not path.is_file() or relative not in EXPECTED_PAYLOAD_FILES:
            errors.append(f"unexpected package payload: {relative}")
    if errors:
        return errors

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
        if payload_size(path) != entry["size"]:
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
