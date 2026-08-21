#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from build_skills import check as check_generated
from common import (
    IMPLICIT_SKILL_NAMES,
    REFERENCE_NAMES,
    ROUTER_NAME,
    SKILL_NAMES,
    directory_digest,
)
from install import install_pack
from runtime_validate import PACK_MANIFEST, load_pack_manifest, validate_payload
from uninstall import uninstall_pack


def write_old_skill(path: Path, marker: str) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "OLD_MARKER.txt").write_text(marker, encoding="utf-8")


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def manifest_status(path: Path) -> str | None:
    return json.loads(path.read_text(encoding="utf-8")).get("status")


def clean_root_env(base: dict[str, str], home: Path) -> dict[str, str]:
    env = base.copy()
    env["HOME"] = str(home)
    for key in ("CODEX_HOME", "SOFTPOWERS_SKILLS_DIR", "AGENTS_SKILLS_DIR"):
        env.pop(key, None)
    return env


def create_historical_layer(
    source: Path,
    dest: Path,
    retired_name: str,
    *,
    backup_marker: str | None,
) -> Path:
    for name in SKILL_NAMES:
        shutil.copytree(source / name, dest / name)
    write_old_skill(dest / retired_name, "historical pack copy")

    backup: Path | None = None
    if backup_marker is not None:
        backup = dest / ".softpowers-backups" / "historical-test" / retired_name
        write_old_skill(backup, backup_marker)
    entries = [
        {
            "name": name,
            "target": str(dest / name),
            "backup": str(backup) if name == retired_name and backup is not None else None,
            "installed_sha256": directory_digest(dest / name),
        }
        for name in (*SKILL_NAMES, retired_name)
    ]
    manifest = dest / ".softpowers-manifests" / "softpowers-historical-test.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "pack": "softpowers-pack",
                "version": "historical-test",
                "status": "installed",
                "installed_at": "2026-08-17T00:00:00+00:00",
                "destination": str(dest),
                "previous_manifest": None,
                "skills": entries,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (dest / ".softpowers-current-manifest").write_text(str(manifest) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    source = root / "skills"

    router_source = (root / "scripts" / "build_skills.py").read_text(encoding="utf-8")
    assert_true(
        "## Goal authority" in router_source
        and "strong evidence for generalized infrastructure" in router_source
        and "applicable current authority" in router_source
        and "foundational work" in router_source,
        "router goal-authority contract missing",
    )
    execute_method = (root / "methods" / "execute.md").read_text(encoding="utf-8")
    assert_true(
        "programme order" in execute_method
        and "trust model" in execute_method
        and "present consumer" in execute_method,
        "execute goal-integrity stop conditions missing",
    )
    review_method = (root / "methods" / "review.md").read_text(encoding="utf-8")
    for verdict in ("advances", "research-only", "diverges", "authority unclear"):
        assert_true(verdict in review_method, f"review goal-integrity verdict missing: {verdict}")
    assert_true(
        "When a change could alter product meaning" in review_method
        and "Omit the verdict" in review_method,
        "review goal-integrity trigger is overbroad",
    )
    spec_chain_method = (root / "methods" / "spec-chain.md").read_text(encoding="utf-8")
    assert_true(
        "agent-authored" in spec_chain_method
        and "does not become approved authority" in spec_chain_method,
        "spec-chain derived-authority boundary missing",
    )
    for method_name, required_text in {
        "plan": "recording the delta does not approve it",
        "receive-review": "not authority by authorship or placement alone",
        "finish": "implementation deviations as evidence to review",
    }.items():
        method = (root / "methods" / f"{method_name}.md").read_text(encoding="utf-8")
        assert_true(required_text in method, f"{method_name} goal-authority boundary missing")

    expected_case_verdicts = {
        "owner-controlled-migration": "Goal-integrity verdict: research-only.",
        "programme-reorder-review": "Goal-integrity verdict: diverges.",
        "adopted-foundation-review": "Goal-integrity verdict: advances.",
    }
    all_verdicts = {
        "Goal-integrity verdict: advances.",
        "Goal-integrity verdict: research-only.",
        "Goal-integrity verdict: diverges.",
        "Goal-integrity verdict: authority unclear.",
    }
    for case_id, expected_verdict in expected_case_verdicts.items():
        case_path = root / "evals" / "cases" / case_id / "case.json"
        assert_true(case_path.is_file(), f"goal-integrity behavior case missing: {case_id}")
        case = json.loads(case_path.read_text(encoding="utf-8"))
        assertions = case.get("assertions", [])
        expected_assertions = [
            assertion
            for assertion in assertions
            if assertion.get("type") == "file_contains"
            and assertion.get("value") == expected_verdict
        ]
        assert_true(
            len(expected_assertions) == 1,
            f"goal-integrity verdict assertion is not exact: {case_id}",
        )
        verdict_path = expected_assertions[0].get("path")
        prohibited_verdicts = {
            assertion.get("value")
            for assertion in assertions
            if assertion.get("type") == "file_not_contains"
            and assertion.get("path") == verdict_path
        }
        missing_prohibitions = all_verdicts - {expected_verdict} - prohibited_verdicts
        assert_true(
            not missing_prohibitions,
            f"goal-integrity contradictory verdicts are not excluded: {case_id}: "
            f"{sorted(missing_prohibitions)}",
        )
        asserted_verdicts = {
            assertion.get("value")
            for assertion in case.get("assertions", [])
            if assertion.get("type") == "file_contains"
            and assertion.get("value") in all_verdicts
        }
        assert_true(
            asserted_verdicts == {expected_verdict},
            f"goal-integrity case contains contradictory positive verdicts: {case_id}",
        )

    sync_errors = check_generated()
    assert_true(not sync_errors, f"generated payload is stale: {sync_errors}")

    source_errors = validate_payload(source, manifest_path=PACK_MANIFEST, allow_other_skills=False)
    assert_true(not source_errors, f"source payload invalid: {source_errors}")

    pack_manifest = load_pack_manifest(PACK_MANIFEST)
    assert_true(
        pack_manifest["activation"]["implicit"] == list(IMPLICIT_SKILL_NAMES),
        "implicit activation contract is wrong",
    )
    assert_true(
        pack_manifest["activation"]["explicit_only"]
        == [name for name in SKILL_NAMES if name not in IMPLICIT_SKILL_NAMES],
        "leaf activation contract is wrong",
    )

    router_yaml = (source / ROUTER_NAME / "agents" / "openai.yaml").read_text(encoding="utf-8")
    assert_true("allow_implicit_invocation: true" in router_yaml, "router implicit policy missing")
    for name in SKILL_NAMES:
        leaf_yaml = (source / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
        expected = "true" if name in IMPLICIT_SKILL_NAMES else "false"
        assert_true(
            f"allow_implicit_invocation: {expected}" in leaf_yaml,
            f"{name} has the wrong implicit policy",
        )

    with tempfile.TemporaryDirectory(prefix="softpowers-selftest-") as raw:
        base = Path(raw)

        # A removed skill must be retired through its historical manifest before
        # the new pack installs, then remain independently owned afterward.
        historical_dest = base / "historical" / "skills"
        retired_name = "license-boundary"
        historical_manifest = create_historical_layer(
            source,
            historical_dest,
            retired_name,
            backup_marker="standalone copy",
        )
        pointer = historical_dest / ".softpowers-current-manifest"
        pointer_before = pointer.read_text(encoding="utf-8")
        router_before = (historical_dest / ROUTER_NAME / "SKILL.md").read_bytes()
        try:
            install_pack(source, historical_dest)
        except RuntimeError as exc:
            assert_true(
                "active historical Softpowers layer" in str(exc),
                "unexpected historical-layer install error",
            )
            assert_true("v0.1.0-rc3" in str(exc), "standalone migration guidance missing")
        else:
            raise AssertionError("install replaced a pack while it still managed a retired skill")
        assert_true(pointer.read_text(encoding="utf-8") == pointer_before, "blocked install changed pointer")
        assert_true(
            (historical_dest / ROUTER_NAME / "SKILL.md").read_bytes() == router_before,
            "blocked install changed active skills",
        )

        uninstall_pack(historical_dest)
        assert_true(manifest_status(historical_manifest) == "uninstalled", "historical layer stayed active")
        assert_true(
            (historical_dest / retired_name / "OLD_MARKER.txt").read_text(encoding="utf-8")
            == "standalone copy",
            "historical uninstall did not restore the independently owned skill",
        )
        migrated_manifest = install_pack(source, historical_dest)
        assert_true(
            (historical_dest / retired_name / "OLD_MARKER.txt").read_text(encoding="utf-8")
            == "standalone copy",
            "new install replaced the independently owned skill",
        )
        uninstall_pack(historical_dest, migrated_manifest)
        assert_true(
            (historical_dest / retired_name / "OLD_MARKER.txt").is_file(),
            "new uninstall removed the independently owned skill",
        )

        # A retired skill that belonged only to the old pack must disappear
        # after its historical layer is uninstalled and stay outside new layers.
        retired_eval_dest = base / "retired-soft-eval" / "skills"
        retired_eval_manifest = create_historical_layer(
            source,
            retired_eval_dest,
            "soft-eval",
            backup_marker=None,
        )
        eval_pointer = retired_eval_dest / ".softpowers-current-manifest"
        eval_pointer_before = eval_pointer.read_text(encoding="utf-8")
        try:
            install_pack(source, retired_eval_dest)
        except RuntimeError as exc:
            assert_true("soft-eval" in str(exc), "retired soft-eval was not identified")
        else:
            raise AssertionError("install replaced a layer that still managed soft-eval")
        assert_true(
            eval_pointer.read_text(encoding="utf-8") == eval_pointer_before,
            "blocked soft-eval migration changed the manifest pointer",
        )

        uninstall_pack(retired_eval_dest)
        assert_true(
            manifest_status(retired_eval_manifest) == "uninstalled",
            "retired soft-eval layer stayed active",
        )
        assert_true(
            not (retired_eval_dest / "soft-eval").exists(),
            "historical uninstall left manifest-owned soft-eval behind",
        )
        migrated_eval_manifest = install_pack(source, retired_eval_dest)
        assert_true(
            not (retired_eval_dest / "soft-eval").exists(),
            "new pack reclaimed retired soft-eval",
        )
        uninstall_pack(retired_eval_dest, migrated_eval_manifest)
        assert_true(
            not (retired_eval_dest / "soft-eval").exists(),
            "new uninstall recreated retired soft-eval",
        )

        # Coexistence + backup restoration.
        dest = base / "coexist" / "skills"
        write_old_skill(dest / "unrelated-skill", "leave me alone")
        write_old_skill(dest / "soft-debug", "restore me")

        manifest = install_pack(source, dest)
        assert_true((dest / "unrelated-skill" / "OLD_MARKER.txt").is_file(), "unrelated skill changed")
        assert_true(
            not validate_payload(dest, manifest_path=PACK_MANIFEST, allow_other_skills=True),
            "installed target invalid",
        )
        assert_true(manifest.is_file(), "manifest missing")
        for reference in REFERENCE_NAMES:
            assert_true(
                (dest / ROUTER_NAME / "references" / reference).is_file(),
                f"router reference missing after install: {reference}",
            )

        uninstall_pack(dest)
        assert_true((dest / "unrelated-skill" / "OLD_MARKER.txt").is_file(), "unrelated skill lost")
        assert_true(
            (dest / "soft-debug" / "OLD_MARKER.txt").read_text(encoding="utf-8") == "restore me",
            "replaced skill was not restored",
        )
        assert_true(not (dest / ROUTER_NAME).exists(), "new router remained after uninstall")

        # User edits after installation must survive uninstall as a snapshot.
        edited_dest = base / "edited" / "skills"
        install_pack(source, edited_dest)
        edited_file = edited_dest / "soft-debug" / "USER_EDIT.txt"
        edited_file.write_text("keep this", encoding="utf-8")
        _, preserved = uninstall_pack(edited_dest)
        assert_true(any(path.name == "soft-debug" for path in preserved), "edited skill not preserved")
        preserved_debug = next(path for path in preserved if path.name == "soft-debug")
        assert_true(
            (preserved_debug / "USER_EDIT.txt").read_text(encoding="utf-8") == "keep this",
            "edited content lost",
        )

        # Repeated installs form a reversible manifest stack.
        stacked_dest = base / "stacked" / "skills"
        first_manifest = install_pack(source, stacked_dest)
        second_manifest = install_pack(source, stacked_dest)
        assert_true(second_manifest != first_manifest, "stacked manifests collided")

        # Explicit non-LIFO uninstall must be rejected before any mutation.
        pointer = stacked_dest / ".softpowers-current-manifest"
        pointer_before = pointer.read_text(encoding="utf-8")
        active_digest_before = (stacked_dest / ROUTER_NAME / "SKILL.md").read_bytes()
        try:
            uninstall_pack(stacked_dest, first_manifest)
        except RuntimeError as exc:
            assert_true("Non-LIFO uninstall refused" in str(exc), "unexpected non-LIFO error")
        else:
            raise AssertionError("non-LIFO uninstall was not rejected")

        assert_true(pointer.read_text(encoding="utf-8") == pointer_before, "non-LIFO attempt changed pointer")
        assert_true(manifest_status(first_manifest) == "installed", "first manifest status changed")
        assert_true(manifest_status(second_manifest) == "installed", "second manifest status changed")
        assert_true(
            (stacked_dest / ROUTER_NAME / "SKILL.md").read_bytes() == active_digest_before,
            "non-LIFO attempt changed active skill",
        )

        uninstall_pack(stacked_dest)
        assert_true(
            pointer.read_text(encoding="utf-8").strip() == str(first_manifest),
            "previous manifest pointer not restored",
        )
        assert_true((stacked_dest / ROUTER_NAME / "SKILL.md").is_file(), "previous pack not restored")
        uninstall_pack(stacked_dest)
        assert_true(not (stacked_dest / ROUTER_NAME).exists(), "first pack remained after stacked uninstall")

        # Transaction rollback after partial replacement.
        rollback_dest = base / "rollback" / "skills"
        for name in SKILL_NAMES:
            write_old_skill(rollback_dest / name, f"old:{name}")

        try:
            install_pack(source, rollback_dest, fail_after=4)
        except RuntimeError as exc:
            assert_true("Injected self-test failure" in str(exc), "unexpected rollback error")
        else:
            raise AssertionError("injected install failure did not fail")

        for name in SKILL_NAMES:
            marker = rollback_dest / name / "OLD_MARKER.txt"
            assert_true(marker.is_file(), f"rollback did not restore {name}")

        # Digest validation must reject a modified reference without parsing YAML.
        tampered_source = base / "tampered-skills"
        shutil.copytree(source, tampered_source)
        tampered_file = tampered_source / ROUTER_NAME / "references" / "debug.md"
        tampered_file.write_bytes(tampered_file.read_bytes() + b"\n")
        tamper_errors = validate_payload(
            tampered_source,
            manifest_path=PACK_MANIFEST,
            allow_other_skills=False,
        )
        assert_true(any("mismatch" in error for error in tamper_errors), "tampered reference was accepted")

        # New installs follow the current ~/.agents/skills user root.
        new_home = base / "new-home"
        env = clean_root_env(os.environ, new_home)
        subprocess.run(
            [str(root / "install.sh")],
            cwd=root,
            env=env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        assert_true(
            (new_home / ".agents" / "skills" / ROUTER_NAME / "SKILL.md").is_file(),
            "fresh install did not use ~/.agents/skills",
        )
        subprocess.run(
            [str(root / "uninstall.sh")],
            cwd=root,
            env=env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Existing v0.1.x-style ~/.codex/skills installs are upgraded in place.
        legacy_home = base / "legacy-home"
        legacy_root = legacy_home / ".codex" / "skills"
        write_old_skill(legacy_root / ROUTER_NAME, "legacy router")
        legacy_env = clean_root_env(os.environ, legacy_home)
        subprocess.run(
            [str(root / "install.sh")],
            cwd=root,
            env=legacy_env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        assert_true(
            (legacy_root / ROUTER_NAME / "references" / "debug.md").is_file(),
            "legacy root was not upgraded in place",
        )
        assert_true(
            not (legacy_home / ".agents" / "skills" / ROUTER_NAME).exists(),
            "legacy upgrade unexpectedly installed a second copy",
        )
        subprocess.run(
            [str(root / "uninstall.sh")],
            cwd=root,
            env=legacy_env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        assert_true(
            (legacy_root / ROUTER_NAME / "OLD_MARKER.txt").read_text(encoding="utf-8") == "legacy router",
            "legacy router was not restored",
        )

        # Ambiguous dual roots must be rejected before any mutation.
        dual_home = base / "dual-home"
        for dual_root, marker in (
            (dual_home / ".agents" / "skills", "official"),
            (dual_home / ".codex" / "skills", "legacy"),
        ):
            write_old_skill(dual_root / ROUTER_NAME, marker)
            (dual_root / ROUTER_NAME / "SKILL.md").write_text(marker, encoding="utf-8")
        dual_env = clean_root_env(os.environ, dual_home)
        dual_result = subprocess.run(
            [str(root / "install.sh")],
            cwd=root,
            env=dual_env,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        assert_true(dual_result.returncode == 1, "dual-root ambiguity was not rejected")
        assert_true("both ~/.agents/skills and ~/.codex/skills" in dual_result.stderr, "wrong dual-root error")
        assert_true(
            (dual_home / ".agents" / "skills" / ROUTER_NAME / "OLD_MARKER.txt").read_text(encoding="utf-8") == "official",
            "dual-root rejection mutated official root",
        )
        assert_true(
            (dual_home / ".codex" / "skills" / ROUTER_NAME / "OLD_MARKER.txt").read_text(encoding="utf-8") == "legacy",
            "dual-root rejection mutated legacy root",
        )

        # User-facing shell wrappers must work when python3 has site-packages disabled.
        no_site_home = base / "no-site" / "codex"
        fake_bin = base / "no-site" / "bin"
        fake_bin.mkdir(parents=True, exist_ok=True)
        fake_python = fake_bin / "python3"
        fake_python.write_text(
            '#!/usr/bin/env bash\nexec "$SOFTPOWERS_REAL_PYTHON" -S "$@"\n',
            encoding="utf-8",
        )
        fake_python.chmod(0o755)

        no_site_env = os.environ.copy()
        no_site_env["CODEX_HOME"] = str(no_site_home)
        no_site_env["SOFTPOWERS_REAL_PYTHON"] = sys.executable
        no_site_env["PATH"] = str(fake_bin) + os.pathsep + no_site_env.get("PATH", "")
        subprocess.run(
            [str(root / "install.sh")],
            cwd=root,
            env=no_site_env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        assert_true(
            (no_site_home / "skills" / ROUTER_NAME / "references" / "debug.md").is_file(),
            "no-site install failed",
        )
        subprocess.run(
            [str(root / "uninstall.sh")],
            cwd=root,
            env=no_site_env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        assert_true(not (no_site_home / "skills" / ROUTER_NAME).exists(), "no-site uninstall failed")

    print(
        "Softpowers packaging self-test passed: bounded implicit activation metadata, generated-source "
        "sync, reference digests, historical-manifest migration, coexistence, default-root selection, legacy-root upgrade, "
        "dual-root rejection, manifest stacking, non-LIFO rejection, edit preservation, "
        "restore, rollback, and "
        "no-site-packages install/uninstall."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
