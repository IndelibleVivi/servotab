#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

import migrate_legacy_install as legacy_migration
from build_skills import check as check_generated
from build_skills import write as write_generated
from migrate_legacy_install import directory_digest
from runtime_validate import (
    PACK_MANIFEST,
    RETIRED_METHOD_FILES,
    RETIRED_REPO_PATHS,
    load_pack_manifest,
    validate_marketplace,
    validate_package,
    validate_plugin_manifest,
)
from skill_catalog import IMPLICIT_SKILL_NAMES, REFERENCE_METHOD_NAMES, SKILL_NAMES
from validate import validate_directory


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = (
    "servotab",
    "design",
    "spec-chain",
    "plan",
    "execute",
    "debug",
    "tdd",
    "review",
    "review-feedback",
    "verify",
    "worktree",
    "delegate",
    "finish",
)


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def assert_detected(errors: list[str], message: str) -> None:
    assert_true(bool(errors), message)


def assert_error_contains(errors: list[str], expected: str, message: str) -> None:
    assert_true(
        any(expected in error for error in errors),
        f"{message}; got {errors!r}",
    )


def contract_copy(source: Path, destination: Path) -> Path:
    destination.mkdir(parents=True)
    for directory in ("methods", "assets", "plugins", ".agents"):
        shutil.copytree(source / directory, destination / directory)
    for filename in ("PACK_MANIFEST.json", "VERSION"):
        shutil.copy2(source / filename, destination / filename)
    return destination


def mutate_json(path: Path, callback) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    callback(payload)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def make_legacy_fixture(root: Path) -> Path:
    skills_root = root / "skills"
    skill = skills_root / "soft-debug"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("legacy\n", encoding="utf-8")
    manifests = skills_root / ".softpowers-manifests"
    manifests.mkdir(parents=True)
    manifest_path = manifests / "softpowers-test.json"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "pack": "softpowers-pack",
                "version": "test",
                "status": "installed",
                "destination": str(skills_root),
                "previous_manifest": None,
                "skills": [
                    {
                        "name": "soft-debug",
                        "target": str(skill),
                        "backup": None,
                        "installed_sha256": directory_digest(skill),
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (skills_root / ".softpowers-current-manifest").write_text(
        str(manifest_path) + "\n", encoding="utf-8"
    )
    return skills_root


def make_two_layer_legacy_fixture(root: Path) -> tuple[Path, Path, Path]:
    skills_root = root / "skills"
    skill = skills_root / "soft-debug"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("previous\n", encoding="utf-8")
    manifests = skills_root / ".softpowers-manifests"
    manifests.mkdir(parents=True)
    previous_manifest = manifests / "softpowers-previous.json"
    previous_manifest.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "pack": "softpowers-pack",
                "version": "previous",
                "status": "installed",
                "destination": str(skills_root),
                "previous_manifest": None,
                "skills": [
                    {
                        "name": "soft-debug",
                        "target": str(skill),
                        "backup": None,
                        "installed_sha256": directory_digest(skill),
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    backup = skills_root / ".softpowers-backups/current/soft-debug"
    backup.parent.mkdir(parents=True)
    os.replace(skill, backup)
    skill.mkdir()
    (skill / "SKILL.md").write_text("current\n", encoding="utf-8")
    current_manifest = manifests / "softpowers-current.json"
    current_manifest.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "pack": "softpowers-pack",
                "version": "current",
                "status": "installed",
                "destination": str(skills_root),
                "previous_manifest": str(previous_manifest),
                "skills": [
                    {
                        "name": "soft-debug",
                        "target": str(skill),
                        "backup": str(backup),
                        "installed_sha256": directory_digest(skill),
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (skills_root / ".softpowers-current-manifest").write_text(
        str(current_manifest) + "\n", encoding="utf-8"
    )
    return skills_root, previous_manifest, current_manifest


def run_legacy_helper(skills_root: Path, *, retire: bool = False) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        str(ROOT / "scripts/migrate_legacy_install.py"),
        "--dest",
        str(skills_root),
    ]
    if retire:
        command.append("--retire")
    return subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def main() -> int:
    plugin_root = ROOT / "plugins" / "servotab"
    skills_root = plugin_root / "skills"

    assert_true(tuple(SKILL_NAMES) == EXPECTED_SKILLS, "catalog identity or skill count changed")
    assert_true(IMPLICIT_SKILL_NAMES == ("servotab",), "implicit activation must be servotab only")
    assert_true(len(REFERENCE_METHOD_NAMES) == 12, "router must expose exactly 12 references")
    assert_true(
        (ROOT / "VERSION").read_text(encoding="utf-8").strip() == "0.4.0-rc1",
        "candidate version must be 0.4.0-rc1",
    )

    method_files = {path.name for path in (ROOT / "methods").glob("*.md")}
    expected_method_files = {f"{name}.md" for name in REFERENCE_METHOD_NAMES}
    assert_true(method_files == expected_method_files, "canonical method file set drifted")
    assert_true(not check_generated(), "generated plugin skills or assets are stale")
    assert_true(not validate_directory(skills_root, exact=True), "generated skills are invalid")
    assert_true(not validate_package(ROOT), "repository plugin package is invalid")

    manifest = load_pack_manifest(PACK_MANIFEST)
    assert_true(manifest["pack"] == "servotab", "pack identity drifted")
    assert_true(manifest["skills"] == list(EXPECTED_SKILLS), "pack skill order drifted")
    for path in RETIRED_REPO_PATHS:
        assert_true(not (ROOT / path).exists(), f"retired global installer path remains: {path}")
    for filename in RETIRED_METHOD_FILES:
        assert_true(not (ROOT / "methods" / filename).exists(), f"retired method id remains: {filename}")

    router = (skills_root / "servotab" / "SKILL.md").read_text(encoding="utf-8")
    assert_true("# Servotab" in router, "router identity is wrong")
    assert_true("references/delegate.md" in router, "router lost delegate routing")
    assert_true("references/review-feedback.md" in router, "router lost feedback routing")
    assert_true("references/design.md" in router, "router lost design routing")
    assert_true("$soft" not in router and "Softpowers" not in router, "router retains old branding")

    execute = (ROOT / "methods" / "execute.md").read_text(encoding="utf-8")
    review = (ROOT / "methods" / "review.md").read_text(encoding="utf-8")
    feedback = (ROOT / "methods" / "review-feedback.md").read_text(encoding="utf-8")
    delegate = (ROOT / "methods" / "delegate.md").read_text(encoding="utf-8")
    design = (ROOT / "methods" / "design.md").read_text(encoding="utf-8")
    assert_true("`delegate` reference" in execute, "execute lost the delegation phase change")
    for verdict in ("advances", "research-only", "diverges", "authority unclear"):
        assert_true(verdict in review, f"review lost goal-integrity verdict: {verdict}")
    assert_true("not authority by authorship" in feedback, "review-feedback lost authority boundary")
    assert_true("harness-initiated spawn" in delegate, "delegate lost host attribution boundary")
    assert_true("capability boundary" in design.lower(), "design lost supported-path pressure test")

    with tempfile.TemporaryDirectory(prefix="servotab-selftest-") as raw:
        base = Path(raw)

        identity_root = contract_copy(ROOT, base / "identity")
        identity_manifest = identity_root / "plugins/servotab/.codex-plugin/plugin.json"
        mutate_json(identity_manifest, lambda data: data.__setitem__("name", "not-servotab"))
        assert_detected(validate_plugin_manifest(identity_root), "broken plugin identity was accepted")

        repository_root = contract_copy(ROOT, base / "repository-url")
        repository_manifest = repository_root / "plugins/servotab/.codex-plugin/plugin.json"
        mutate_json(
            repository_manifest,
            lambda data: data.__setitem__(
                "repository", "https://github.com/IndelibleVivi/not-servotab"
            ),
        )
        assert_detected(
            validate_plugin_manifest(repository_root),
            "broken plugin repository URL was accepted",
        )

        prompt_root = contract_copy(ROOT, base / "default-prompt")
        prompt_manifest = prompt_root / "plugins/servotab/.codex-plugin/plugin.json"
        mutate_json(
            prompt_manifest,
            lambda data: data["interface"].__setitem__(
                "defaultPrompt", "Use $servotab with the wrong scalar shape."
            ),
        )
        assert_detected(
            validate_plugin_manifest(prompt_root),
            "scalar plugin defaultPrompt was accepted",
        )

        directory_metadata_root = contract_copy(ROOT, base / "directory-metadata")
        directory_metadata_manifest = (
            directory_metadata_root / "plugins/servotab/.codex-plugin/plugin.json"
        )
        mutate_json(
            directory_metadata_manifest,
            lambda data: data["interface"].__setitem__(
                "shortDescription", "Quiet, risk-scaled engineering methods"
            ),
        )
        assert_error_contains(
            validate_plugin_manifest(directory_metadata_root),
            "must be no longer than 30 characters for final directory submission",
            "overlong directory short description was accepted",
        )

        duplicate_prompt_root = contract_copy(ROOT, base / "duplicate-prompt")
        duplicate_prompt_manifest = (
            duplicate_prompt_root / "plugins/servotab/.codex-plugin/plugin.json"
        )
        mutate_json(
            duplicate_prompt_manifest,
            lambda data: data["interface"].__setitem__(
                "defaultPrompt",
                [
                    "Use $servotab to fix this repository bug.",
                    "  Use $servotab to fix this repository bug.  ",
                ],
            ),
        )
        assert_detected(
            validate_plugin_manifest(duplicate_prompt_root),
            "normalized duplicate plugin prompts were accepted",
        )

        multiline_prompt_root = contract_copy(ROOT, base / "multiline-prompt")
        multiline_prompt_manifest = (
            multiline_prompt_root / "plugins/servotab/.codex-plugin/plugin.json"
        )
        mutate_json(
            multiline_prompt_manifest,
            lambda data: data["interface"].__setitem__(
                "defaultPrompt",
                ["Use $servotab to fix this repository bug.\nThen verify it."],
            ),
        )
        assert_detected(
            validate_plugin_manifest(multiline_prompt_root),
            "multiline plugin prompt was accepted",
        )

        app_mention_root = contract_copy(ROOT, base / "app-mention")
        app_mention_manifest = (
            app_mention_root / "plugins/servotab/.codex-plugin/plugin.json"
        )
        mutate_json(
            app_mention_manifest,
            lambda data: data["interface"].__setitem__(
                "defaultPrompt", ["Use $servotab with @servotab to fix this bug."]
            ),
        )
        assert_detected(
            validate_plugin_manifest(app_mention_root),
            "plugin app @mention was accepted",
        )

        count_root = contract_copy(ROOT, base / "count")
        shutil.rmtree(count_root / "plugins/servotab/skills/design")
        assert_detected(
            validate_directory(count_root / "plugins/servotab/skills", exact=True),
            "missing explicit leaf was accepted",
        )

        sync_root = contract_copy(ROOT, base / "sync")
        sync_skill = sync_root / "plugins/servotab/skills/debug/SKILL.md"
        sync_skill.write_text(sync_skill.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        assert_detected(check_generated(sync_root), "source/generated drift was accepted")

        generator_root = contract_copy(ROOT, base / "generator-legacy-root")
        legacy_projection = generator_root / "skills"
        legacy_projection.mkdir()
        legacy_sentinel = legacy_projection / "keep.txt"
        legacy_sentinel.write_text("unrelated\n", encoding="utf-8")
        try:
            write_generated(generator_root)
        except FileExistsError as exc:
            assert_true(
                "retired root skills/ projection still exists" in str(exc),
                "generator reported the wrong legacy-root failure",
            )
        else:
            raise AssertionError("generator deleted or accepted a retired root skills/ projection")
        assert_true(
            legacy_sentinel.read_text(encoding="utf-8") == "unrelated\n",
            "generator mutated content under the retired root skills/ projection",
        )

        legacy_root = contract_copy(ROOT, base / "legacy-id")
        (legacy_root / "methods" / "brainstorm.md").write_text("retired\n", encoding="utf-8")
        assert_detected(validate_package(legacy_root), "retired method id was accepted")

        asset_root = contract_copy(ROOT, base / "asset-path")
        asset_manifest = asset_root / "plugins/servotab/.codex-plugin/plugin.json"
        mutate_json(
            asset_manifest,
            lambda data: data["interface"].__setitem__("composerIcon", "./assets/missing.png"),
        )
        assert_detected(validate_plugin_manifest(asset_root), "broken manifest asset path was accepted")

        marketplace_root = contract_copy(ROOT, base / "marketplace")
        marketplace_path = marketplace_root / ".agents/plugins/marketplace.json"
        mutate_json(
            marketplace_path,
            lambda data: data["plugins"][0]["source"].__setitem__("path", "./plugins/wrong"),
        )
        assert_detected(validate_marketplace(marketplace_root), "broken marketplace path was accepted")

        digest_root = contract_copy(ROOT, base / "digest")
        digest_asset = digest_root / "plugins/servotab/assets/composer-icon.png"
        digest_asset.write_bytes(digest_asset.read_bytes() + b"tamper")
        assert_detected(validate_package(digest_root), "tampered package asset was accepted")

        legacy_fixture = make_legacy_fixture(base / "legacy-helper")
        before = directory_digest(legacy_fixture)
        result = run_legacy_helper(legacy_fixture)
        assert_true(result.returncode == 2, "legacy helper did not report active ownership")
        assert_true(directory_digest(legacy_fixture) == before, "default legacy preflight mutated state")
        pointer = legacy_fixture / ".softpowers-current-manifest"
        manifest_path = Path(pointer.read_text(encoding="utf-8").strip())
        retire = run_legacy_helper(legacy_fixture, retire=True)
        assert_true(retire.returncode == 0, f"explicit legacy retirement failed: {retire.stderr}")
        assert_true(not pointer.exists(), "explicit retirement left the active manifest pointer")
        assert_true(not (legacy_fixture / "soft-debug").exists(), "explicit retirement left owned skill")
        retired_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert_true(retired_manifest.get("status") == "uninstalled", "retirement status not recorded")

        two_layer_fixture, previous_manifest, current_manifest = make_two_layer_legacy_fixture(
            base / "legacy-two-layer"
        )
        two_layer_retire = run_legacy_helper(two_layer_fixture, retire=True)
        assert_true(
            two_layer_retire.returncode == 0,
            f"two-layer retirement failed: {two_layer_retire.stderr}",
        )
        two_layer_pointer = two_layer_fixture / ".softpowers-current-manifest"
        assert_true(
            Path(two_layer_pointer.read_text(encoding="utf-8").strip()).resolve()
            == previous_manifest.resolve(),
            "two-layer retirement did not promote the previous manifest",
        )
        assert_true(
            (two_layer_fixture / "soft-debug/SKILL.md").read_text(encoding="utf-8")
            == "previous\n",
            "two-layer retirement did not restore the previous skill",
        )
        assert_true(
            json.loads(current_manifest.read_text(encoding="utf-8")).get("status")
            == "uninstalled",
            "two-layer retirement did not close the current manifest",
        )
        assert_true(
            json.loads(previous_manifest.read_text(encoding="utf-8")).get("status") == "installed",
            "two-layer retirement modified the promoted manifest",
        )

        symlink_fixture = make_legacy_fixture(base / "legacy-symlink-leaf")
        symlink_skill = symlink_fixture / "soft-debug"
        shutil.rmtree(symlink_skill)
        unrelated = symlink_fixture / "unrelated"
        unrelated.mkdir()
        (unrelated / "keep.txt").write_text("unrelated\n", encoding="utf-8")
        symlink_skill.symlink_to(unrelated, target_is_directory=True)
        symlink_manifest_path = Path(
            (symlink_fixture / ".softpowers-current-manifest").read_text(encoding="utf-8").strip()
        )
        mutate_json(
            symlink_manifest_path,
            lambda data: data["skills"][0].__setitem__(
                "installed_sha256", directory_digest(symlink_skill)
            ),
        )
        symlink_retire = run_legacy_helper(symlink_fixture, retire=True)
        assert_true(
            symlink_retire.returncode == 0,
            f"safe symlink-leaf retirement failed: {symlink_retire.stderr}",
        )
        assert_true(
            (unrelated / "keep.txt").read_text(encoding="utf-8") == "unrelated\n",
            "legacy retirement mutated a symlink referent",
        )
        assert_true(
            not legacy_migration.path_exists(symlink_skill),
            "legacy retirement left an owned symlink",
        )

        missing_fixture = make_legacy_fixture(base / "legacy-missing-previous")
        missing_pointer = missing_fixture / ".softpowers-current-manifest"
        missing_manifest = Path(missing_pointer.read_text(encoding="utf-8").strip())
        missing_target = missing_fixture / "soft-debug"
        missing_before = directory_digest(missing_fixture)
        mutate_json(
            missing_manifest,
            lambda data: data.__setitem__(
                "previous_manifest",
                str(missing_fixture / ".softpowers-manifests/missing.json"),
            ),
        )
        missing_before = directory_digest(missing_fixture)
        missing_retire = run_legacy_helper(missing_fixture, retire=True)
        assert_true(missing_retire.returncode == 1, "missing predecessor was accepted")
        assert_true(directory_digest(missing_fixture) == missing_before, "missing predecessor mutated state")
        assert_true(missing_pointer.is_file() and missing_target.is_dir(), "missing predecessor retired ownership")

        missing_key_fixture = make_legacy_fixture(base / "legacy-missing-previous-key")
        missing_key_pointer = missing_key_fixture / ".softpowers-current-manifest"
        missing_key_manifest = Path(missing_key_pointer.read_text(encoding="utf-8").strip())
        mutate_json(
            missing_key_manifest,
            lambda data: data.pop("previous_manifest"),
        )
        missing_key_before = directory_digest(missing_key_fixture)
        missing_key_retire = run_legacy_helper(missing_key_fixture, retire=True)
        assert_true(missing_key_retire.returncode == 1, "missing predecessor key was accepted")
        assert_true(
            directory_digest(missing_key_fixture) == missing_key_before,
            "missing predecessor key mutated state",
        )

        malformed_fixture = make_legacy_fixture(base / "legacy-malformed-previous")
        malformed_pointer = malformed_fixture / ".softpowers-current-manifest"
        malformed_manifest = Path(malformed_pointer.read_text(encoding="utf-8").strip())
        malformed_previous = malformed_fixture / ".softpowers-manifests/malformed.json"
        malformed_previous.write_text("{}\n", encoding="utf-8")
        mutate_json(
            malformed_manifest,
            lambda data: data.__setitem__("previous_manifest", str(malformed_previous)),
        )
        malformed_before = directory_digest(malformed_fixture)
        malformed_retire = run_legacy_helper(malformed_fixture, retire=True)
        assert_true(malformed_retire.returncode == 1, "malformed predecessor was accepted")
        assert_true(
            directory_digest(malformed_fixture) == malformed_before,
            "malformed predecessor mutated state",
        )

        manifest_link_fixture = make_legacy_fixture(base / "legacy-manifest-root-link")
        manifest_root = manifest_link_fixture / ".softpowers-manifests"
        outside_manifest_root = base / "outside-manifests"
        os.replace(manifest_root, outside_manifest_root)
        manifest_root.symlink_to(outside_manifest_root, target_is_directory=True)
        manifest_link_before = directory_digest(manifest_link_fixture)
        manifest_link_result = run_legacy_helper(manifest_link_fixture)
        assert_true(manifest_link_result.returncode == 1, "symlinked manifest root was accepted")
        assert_true(
            directory_digest(manifest_link_fixture) == manifest_link_before,
            "symlinked manifest-root preflight mutated state",
        )

        backup_link_fixture = make_legacy_fixture(base / "legacy-backup-root-link")
        backup_pointer = backup_link_fixture / ".softpowers-current-manifest"
        backup_manifest = Path(backup_pointer.read_text(encoding="utf-8").strip())
        outside_backup_root = base / "outside-backups"
        outside_backup = outside_backup_root / "stamp/soft-debug"
        outside_backup.mkdir(parents=True)
        (outside_backup / "SKILL.md").write_text("older\n", encoding="utf-8")
        (backup_link_fixture / ".softpowers-backups").symlink_to(
            outside_backup_root, target_is_directory=True
        )
        mutate_json(
            backup_manifest,
            lambda data: data["skills"][0].__setitem__(
                "backup", str(backup_link_fixture / ".softpowers-backups/stamp/soft-debug")
            ),
        )
        backup_link_before = directory_digest(backup_link_fixture)
        backup_link_result = run_legacy_helper(backup_link_fixture)
        assert_true(backup_link_result.returncode == 1, "symlinked backup root was accepted")
        assert_true(
            directory_digest(backup_link_fixture) == backup_link_before,
            "symlinked backup-root preflight mutated state",
        )

        snapshot_link_fixture = make_legacy_fixture(base / "legacy-snapshot-root-link")
        outside_snapshot_root = base / "outside-snapshots"
        outside_snapshot_root.mkdir()
        (snapshot_link_fixture / ".softpowers-retire-snapshots").symlink_to(
            outside_snapshot_root, target_is_directory=True
        )
        snapshot_link_before = directory_digest(snapshot_link_fixture)
        snapshot_link_result = run_legacy_helper(snapshot_link_fixture, retire=True)
        assert_true(snapshot_link_result.returncode == 1, "symlinked snapshot root was accepted")
        assert_true(
            directory_digest(snapshot_link_fixture) == snapshot_link_before,
            "symlinked snapshot-root retirement mutated state",
        )

        pointer_dir_fixture = make_legacy_fixture(base / "legacy-pointer-directory")
        pointer_dir = pointer_dir_fixture / ".softpowers-current-manifest"
        pointer_dir.unlink()
        pointer_dir.mkdir()
        pointer_dir_before = directory_digest(pointer_dir_fixture)
        pointer_dir_result = run_legacy_helper(pointer_dir_fixture)
        assert_true(pointer_dir_result.returncode == 1, "directory manifest pointer was reported clear")
        assert_true(
            directory_digest(pointer_dir_fixture) == pointer_dir_before,
            "directory manifest-pointer preflight mutated state",
        )

        broken_pointer_fixture = make_legacy_fixture(base / "legacy-pointer-broken-link")
        broken_pointer = broken_pointer_fixture / ".softpowers-current-manifest"
        broken_pointer.unlink()
        broken_pointer.symlink_to(broken_pointer_fixture / "missing-pointer-target")
        broken_pointer_before = directory_digest(broken_pointer_fixture)
        broken_pointer_result = run_legacy_helper(broken_pointer_fixture)
        assert_true(broken_pointer_result.returncode == 1, "broken manifest pointer was reported clear")
        assert_true(
            directory_digest(broken_pointer_fixture) == broken_pointer_before,
            "broken manifest-pointer preflight mutated state",
        )

        rollback_fixture = make_legacy_fixture(base / "legacy-rollback")
        rollback_skill = rollback_fixture / "soft-debug/SKILL.md"
        rollback_skill.write_text("locally modified\n", encoding="utf-8")
        rollback_before = directory_digest(rollback_fixture)
        original_atomic_write = legacy_migration.atomic_write_text

        def fail_manifest_commit(path: Path, text: str) -> None:
            if path.suffix == ".json":
                raise RuntimeError("injected manifest commit failure")
            original_atomic_write(path, text)

        with mock.patch.object(legacy_migration, "atomic_write_text", fail_manifest_commit):
            try:
                legacy_migration.retire_current_layer(rollback_fixture)
            except RuntimeError as exc:
                assert_true("injected manifest commit failure" in str(exc), "wrong rollback failure")
            else:
                raise AssertionError("injected retirement failure did not fail")
        assert_true(
            directory_digest(rollback_fixture) == rollback_before,
            "failed legacy retirement left rollback debris",
        )

    print(
        "Servotab packaging self-test passed: exact plugin identity and 13-skill topology, "
        "source/generated sync, fail-closed retired-root handling, old-ID retirement, manifest "
        "and asset integrity, marketplace routing, default read-only legacy ownership detection, "
        "and explicit one-layer retirement."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
