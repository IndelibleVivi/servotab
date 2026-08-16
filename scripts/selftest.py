#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from build_skills import check as check_generated, pinned_projection_status
from common import IMPLICIT_SKILL_NAMES, REFERENCE_NAMES, ROUTER_NAME, SKILL_NAMES
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


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    source = root / "skills"

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

    eval_env = os.environ.copy()
    eval_env["PYTHONDONTWRITEBYTECODE"] = "1"
    eval_result = subprocess.run(
        [sys.executable, "-S", str(root / "evals" / "run_behavior_evals.py"), "selftest"],
        cwd=root,
        env=eval_env,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert_true(
        eval_result.returncode == 0,
        f"behavior eval self-test failed: {eval_result.stdout}{eval_result.stderr}",
    )

    with tempfile.TemporaryDirectory(prefix="softpowers-selftest-") as raw:
        base = Path(raw)

        # The standalone specialist is usable offline but pinned against source drift.
        projection_root = base / "projection-root"
        (projection_root / "sources").mkdir(parents=True)
        shutil.copy2(
            root / "sources" / "license-boundary.json",
            projection_root / "sources" / "license-boundary.json",
        )
        shutil.copytree(
            source / "license-boundary",
            projection_root / "skills" / "license-boundary",
        )
        _, projection_errors = pinned_projection_status(
            root=projection_root,
            skills_dir=projection_root / "skills",
        )
        assert_true(not projection_errors, f"clean pinned projection failed: {projection_errors}")
        projected_skill = projection_root / "skills" / "license-boundary" / "SKILL.md"
        projected_payload = projected_skill.read_bytes()
        projected_skill.write_bytes(b"X" + projected_payload[1:])
        _, projection_errors = pinned_projection_status(
            root=projection_root,
            skills_dir=projection_root / "skills",
        )
        assert_true(
            any("sha256 mismatch" in error for error in projection_errors),
            "pinned projection drift was accepted",
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
        "sync, pinned-projection and reference digests, coexistence, default-root selection, legacy-root upgrade, "
        "dual-root rejection, manifest stacking, non-LIFO rejection, edit preservation, "
        "restore, rollback, and "
        "no-site-packages install/uninstall."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
