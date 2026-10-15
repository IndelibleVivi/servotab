"""Rejection and fail-closed regressions for the public-tree audit.

CI runs the audit on the real passing tree, so its rejection behavior needs
its own evidence. Each test drives the real ``scripts/audit_public_tree.py``
entry point inside a disposable synthetic Git repository under the runner's
temporary directory. Every marker below is assembled from pieces, the same way
the audit splits its own markers, so this file stays acceptable to the scanner
it exercises.
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from audit_public_tree import candidate_files, forbidden_path_reason

AUDIT_SCRIPT = Path(__file__).resolve().parent / "audit_public_tree.py"
GIT = shutil.which("git")

# Caller-independent Git environment: no system or global configuration, and
# no inherited Git redirection into the disposable repositories.
NEUTRAL_ENV = {
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_TERMINAL_PROMPT": "0",
}

# Wholly synthetic payloads. No real credential, user name, or machine path.
AWS_MARKER = b"AKIA" + b"0123456789ABCDEF"
GITHUB_MARKER = b"ghp" + b"_" + b"A" * 24
OPENAI_MARKER = b"sk" + b"-" + b"a" * 24
PRIVATE_KEY_MARKER = b"-----BEGIN " + b"OPENSSH PRIVATE KEY-----"
CREDENTIAL_MARKER = b"pass" + b"word" + b" = " + b"synthetic" + b"value012345"
MACOS_PATH_MARKER = b"/" + b"Users/synthetic-fixture"
UNIX_PATH_MARKER = b"/ho" + b"me/synthetic-fixture"
WINDOWS_PATH_MARKER = b"C:\\" + b"Users\\synthetic-fixture"

# relative path -> (synthetic bytes, reason label the audit must report)
REJECTED_MARKER_FILES = {
    "untracked/aws.txt": (AWS_MARKER, "AWS access key"),
    "untracked/github.txt": (GITHUB_MARKER, "GitHub token"),
    "untracked/openai.txt": (OPENAI_MARKER, "OpenAI-style secret key"),
    "untracked/id_rsa": (PRIVATE_KEY_MARKER, "private key header"),
    "untracked/config.ini": (CREDENTIAL_MARKER, "credential assignment"),
    "untracked/macos-path.txt": (MACOS_PATH_MARKER, "macOS user path"),
    "untracked/unix-path.txt": (UNIX_PATH_MARKER, "Unix home path"),
    "untracked/windows-path.txt": (WINDOWS_PATH_MARKER, "Windows user path"),
}

FORBIDDEN_PATHS = (
    ("notes/plan.md", "private namespace notes/"),
    (".local/state.json", "private namespace .local/"),
    ("docs/__pycache__/guide.pyc", "generated local directory"),
    (".venv/lib/site.py", "generated local directory"),
    (".pytest_cache/v/cache/lastfailed", "generated local directory"),
    (".DS_Store", "macOS metadata"),
    ("assets/._icon.svg", "macOS metadata"),
    (".env", "environment file"),
    (".env.production", "environment file"),
    ("docs/retired.private.md", "private-markdown convention"),
)


@unittest.skipUnless(GIT, "git is required for public-tree audit fixtures")
class PublicTreeAuditTests(unittest.TestCase):
    """One disposable repository per test; only index and worktree writes."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="servotab-public-tree-audit-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        self.env = {key: value for key, value in os.environ.items()
                    if not key.upper().startswith("GIT_")}
        self.env.update(NEUTRAL_ENV)
        # Stop Git from discovering a repository above the fixture directory.
        self.env["GIT_CEILING_DIRECTORIES"] = str(self.root.parent)
        self.git("init", "-q")
        self.install_audit_script()

    # -- fixture helpers -------------------------------------------------

    def git(self, *args) -> None:
        result = subprocess.run(["git", *args], cwd=str(self.root), env=self.env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"git {' '.join(args)}: {result.stderr}")

    def install_audit_script(self, root: Path | None = None) -> None:
        target = (root or self.root) / "scripts" / "audit_public_tree.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(AUDIT_SCRIPT, target)

    def write(self, relative: str, data: bytes, root: Path | None = None) -> Path:
        path = (root or self.root) / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def run_audit(self, root: Path | None = None) -> subprocess.CompletedProcess:
        where = root or self.root
        return subprocess.run(
            [sys.executable, str(where / "scripts" / "audit_public_tree.py")],
            cwd=str(where), env=self.env, capture_output=True, text=True,
        )

    # -- acceptance ------------------------------------------------------

    def test_clean_tree_with_ordinary_candidates_passes(self):
        self.write(".env.example", b"EXAMPLE=value\n")
        self.write(".gitignore", b"build/\n")
        self.write("docs/guide.md", b"ordinary staged text\n")
        self.write("scripts/helper.py", b"print('ordinary untracked text')\n")
        # Ignored payloads and deleted tracked entries are outside the audit's
        # scope; if either were read, this fixture would fail.
        self.write("build/ignored.txt", AWS_MARKER + b"\n")
        self.write("docs/removed.md", UNIX_PATH_MARKER + b"\n")
        # A binary candidate keeps its raw bytes but is exempt from the
        # local-path marker scan, while still being enumerated.
        self.write("assets/pixel.bin", b"\x00\x01" + UNIX_PATH_MARKER + b"\x00")
        self.git("add", ".env.example", ".gitignore", "docs/guide.md", "docs/removed.md")
        (self.root / "docs/removed.md").unlink()

        result = self.run_audit()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Public-tree audit passed", result.stdout)

    def test_forbidden_candidate_paths_rejected(self):
        self.write(".env.example", b"EXAMPLE=value\n")
        for relative, _ in FORBIDDEN_PATHS:
            self.write(relative, b"ordinary text\n")

        result = self.run_audit()

        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("Public-tree audit failed:", result.stderr)
        for relative, reason in FORBIDDEN_PATHS:
            with self.subTest(relative=relative):
                self.assertIn(f"- {relative}: {reason}", result.stderr)
        self.assertNotIn(".env.example", result.stderr)

    def test_untracked_synthetic_markers_rejected_with_reason_labels(self):
        for relative, (marker, _) in REJECTED_MARKER_FILES.items():
            self.write(relative, marker + b"\n")

        result = self.run_audit()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Public-tree audit failed:", result.stderr)
        self.assertNotIn("audit passed", result.stdout)
        for relative, (_, reason) in REJECTED_MARKER_FILES.items():
            with self.subTest(relative=relative):
                self.assertIn(f"- {relative}: {reason}", result.stderr)

    def test_candidate_symlink_rejected(self):
        self.write("real.txt", b"ordinary text\n")
        (self.root / "link.txt").symlink_to("real.txt")

        result = self.run_audit()

        self.assertEqual(result.returncode, 1)
        self.assertIn("- link.txt: tracked or candidate symlink", result.stderr)

    def test_git_enumeration_failure_fails_closed(self):
        broken = Path(self.temp.name) / "not-a-repository"
        broken.mkdir()
        self.install_audit_script(broken)
        self.write("leak.txt", AWS_MARKER + b"\n", root=broken)

        result = self.run_audit(broken)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("failed closed", result.stderr)
        self.assertNotIn("audit passed", result.stdout)

    def test_candidate_enumeration_keeps_staged_and_untracked(self):
        self.write(".gitignore", b"ignored.txt\n")
        self.write("staged.txt", b"staged ordinary text\n")
        self.write("untracked.txt", b"untracked ordinary text\n")
        self.write("ignored.txt", b"ignored ordinary text\n")
        self.write("deleted.txt", b"deleted ordinary text\n")
        self.git("add", ".gitignore", "staged.txt", "deleted.txt")
        (self.root / "deleted.txt").unlink()

        with mock.patch.dict(os.environ, self.env, clear=True):
            files = candidate_files(self.root)

        # Staged and untracked ordinary files stay; the deleted tracked entry
        # and the ignored file are excluded. The fixture's own untracked copy
        # of the audit script is an ordinary candidate too.
        self.assertEqual(
            files,
            [".gitignore", "scripts/audit_public_tree.py", "staged.txt", "untracked.txt"],
        )

    def test_forbidden_path_reason_boundaries(self):
        for allowed in (".env.example", "docs/notes.md",
                        "assets/skill-icons/design.svg", "README.md"):
            with self.subTest(allowed=allowed):
                self.assertIsNone(forbidden_path_reason(allowed))
        for rejected, reason in (
            ("notes/plan.md", "private namespace notes/"),
            ("scratch.private.md", "private-markdown convention"),
            (".env", "environment file"),
            (".env.example.local", "environment file"),
        ):
            with self.subTest(rejected=rejected):
                self.assertEqual(forbidden_path_reason(rejected), reason)


if __name__ == "__main__":
    unittest.main()
