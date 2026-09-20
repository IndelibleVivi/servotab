"""Deterministic Git mechanism regressions for Servotab's worktree guidance.

These tests exercise Git itself in disposable synthetic repositories. They
establish the observable mechanisms the worktree lifecycle guidance relies on;
they are not evidence that a skill-following model behaves correctly.
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import uuid

STAMP = '2020-01-01T00:00:00Z'
REQUIRED_GIT = (2, 30, 0)
NEUTRAL = {
    'GIT_AUTHOR_NAME': 'Servotab fixture',
    'GIT_AUTHOR_EMAIL': 'fixture@example.invalid',
    'GIT_COMMITTER_NAME': 'Servotab fixture',
    'GIT_COMMITTER_EMAIL': 'fixture@example.invalid',
    'GIT_AUTHOR_DATE': STAMP,
    'GIT_COMMITTER_DATE': STAMP,
    'GIT_CONFIG_NOSYSTEM': '1',
    # Neutralize commit signing and line-ending translation without touching the
    # developer's global Git configuration.
    'GIT_CONFIG_COUNT': '4',
    'GIT_CONFIG_KEY_0': 'commit.gpgsign',
    'GIT_CONFIG_VALUE_0': 'false',
    'GIT_CONFIG_KEY_1': 'core.autocrlf',
    'GIT_CONFIG_VALUE_1': 'false',
    'GIT_CONFIG_KEY_2': 'core.filemode',
    'GIT_CONFIG_VALUE_2': 'false',
    # Point hooks at an unresolvable location instead of planting executable
    # stubs, so no user or project hook can run in the synthetic repository.
    'GIT_CONFIG_KEY_3': 'core.hooksPath',
    'GIT_CONFIG_VALUE_3': os.devnull,
}


def _git_version() -> tuple[int, ...]:
    raw = subprocess.run(['git', '--version'], capture_output=True, text=True).stdout
    for token in raw.split():
        parts = token.split('.')
        if parts[0].isdigit():
            return tuple(int(part) for part in parts if part.isdigit())
    return ()


GIT_VERSION = _git_version()


@unittest.skipUnless(GIT_VERSION >= REQUIRED_GIT, f'needs Git >= {REQUIRED_GIT}, found {GIT_VERSION}')
class WorktreeGitMechanismTests(unittest.TestCase):
    """One synthetic repository per test; all Git state stays under a temp dir."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='servotab-worktree-git-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        # A caller may itself be running in a worktree or custom index. Never
        # inherit Git redirection into these disposable repositories.
        self.env = {key: value for key, value in os.environ.items()
                    if not key.upper().startswith("GIT_")}
        self.env.update(NEUTRAL)
        self.env['GIT_CONFIG_GLOBAL'] = os.devnull
        self.git('init', '-q')
        self.write('a.txt', 'base\n')
        self.commit('base')

    # -- fixture helpers -------------------------------------------------

    def git(self, *args, cwd: Path | str | None = None) -> str:
        return self.assert_ok(self._git(*args, cwd=cwd or self.repo),
                              "git " + " ".join(args)).stdout

    def rev_in(self, worktree: Path) -> str:
        return self.git('rev-parse', 'HEAD', cwd=worktree).strip()

    def commit_in(self, worktree: Path, message: str) -> str:
        self.assert_ok(self._git('add', '-A', cwd=worktree), 'add in worktree')
        self.assert_ok(self._git('commit', '-qm', message, cwd=worktree), 'commit in worktree')
        return self.rev_in(worktree)

    def _git(self, *args, cwd: Path | str | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            ['git', *args],
            cwd=str(cwd or self.repo),
            env=self.env,
            capture_output=True,
            text=True,
        )

    def assert_ok(self, result: subprocess.CompletedProcess, label: str) -> subprocess.CompletedProcess:
        self.assertEqual(result.returncode, 0, f'{label} failed: {result.stderr.strip()}')
        return result

    def assert_fails(self, *args, cwd: Path | str | None = None) -> subprocess.CompletedProcess:
        result = self._git(*args, cwd=cwd)
        self.assertNotEqual(result.returncode, 0, f'git {" ".join(args)} unexpectedly succeeded')
        return result

    def write(self, relative: str, text: str) -> Path:
        # Exact UTF-8 bytes, so line endings are identical on every platform.
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode('utf-8'))
        return path

    def commit(self, message: str) -> str:
        self.git('add', '-A')
        self.git('commit', '-qm', message)
        return self.git('rev-parse', 'HEAD').strip()

    def unique_name(self, prefix: str) -> str:
        return f'{prefix}-{uuid.uuid4().hex[:12]}'

    def register(self, path: Path, unlock: bool = False) -> Path:
        """Tear down a linked worktree whether or not the test left it intact."""

        def cleanup() -> None:
            if unlock:
                self._git('worktree', 'unlock', str(path))
            self._git('worktree', 'remove', '--force', str(path))
            shutil.rmtree(path, ignore_errors=True)

        self.addCleanup(cleanup)
        return path

    def worktree_paths(self) -> list[Path]:
        prefix = 'worktree '
        return [
            Path(line[len(prefix):]).resolve()
            for line in self.git('worktree', 'list', '--porcelain').splitlines()
            if line.startswith(prefix)
        ]

    def assert_registered(self, path: Path) -> None:
        self.assertIn(path.resolve(), self.worktree_paths())

    # -- 1. ordinary removal tolerates clean status plus ignored state -----

    def test_clean_status_does_not_protect_ignored_local_state_from_removal(self):
        self.write('.gitignore', 'local-state.sqlite\n')
        self.commit('ignore local state')
        worktree = self.register(self.root / 'wt-ignored')
        branch = self.unique_name('parked')
        self.git('worktree', 'add', '-q', str(worktree), '-b', branch)
        (worktree / 'local-state.sqlite').write_bytes(b'binary-ish local state')

        self.assertEqual(self.git('status', '--porcelain=v1', '-uall', cwd=worktree), '')
        status = self.git('status', '--porcelain=v1', '--ignored', cwd=worktree).splitlines()
        self.assertIn('!! local-state.sqlite', status, 'ignored state must not count as a tracked change')
        self.assertTrue((worktree / 'local-state.sqlite').exists())

        # No --force: an ignored helper file must not block an otherwise clean removal.
        self.assert_ok(self._git('worktree', 'remove', str(worktree)), 'worktree remove')
        self.assertFalse(worktree.exists())
        self.assertNotIn(worktree.resolve(), self.worktree_paths())

    # -- 2. a named branch ref outlives its checkout and can restore one ---

    def test_unmerged_named_branch_tip_survives_removal_and_restores_checkout(self):
        worktree = self.register(self.root / 'wt-parked')
        branch = self.unique_name('wip')
        self.git('worktree', 'add', '-q', str(worktree), '-b', branch)
        (worktree / 'a.txt').write_bytes(b'base\nunmerged work\n')
        tip = self.commit_in(worktree, 'unmerged work')
        self.assertEqual(self._git('merge-base', '--is-ancestor', tip, 'HEAD').returncode, 1)

        self.assert_ok(self._git('worktree', 'remove', str(worktree)), 'worktree remove')
        self.assertFalse(worktree.exists())
        self.assertEqual(self.git('rev-parse', f'refs/heads/{branch}').strip(), tip)
        self.assertIn(f'refs/heads/{branch}', self.git('for-each-ref', '--format=%(refname)', '--contains', tip))

        # The surviving ref is enough to recreate a checkout from the repository.
        restored = self.register(self.root / 'wt-restored')
        self.git('worktree', 'add', '-q', str(restored), branch)
        self.assertEqual(self.rev_in(restored), tip)
        self.assertEqual((restored / 'a.txt').read_text(encoding='utf-8'), 'base\nunmerged work\n')

    # -- 3. a detached unique commit has no durable named ref --------------

    def test_detached_unique_commit_has_no_durable_named_ref_after_removal(self):
        worktree = self.register(self.root / 'wt-detached')
        self.git('worktree', 'add', '-q', '--detach', str(worktree))
        (worktree / 'a.txt').write_bytes(b'base\ndetached work\n')
        unique = self.commit_in(worktree, 'detached work')

        self.assert_ok(self._git('worktree', 'remove', str(worktree)), 'worktree remove')
        self.assertFalse(worktree.exists())

        # No branch, tag, or other ref reaches the commit. The object may still
        # exist until some later GC, so this asserts reachability, not absence.
        self.assertEqual(self.git('branch', '--contains', unique), '')
        self.assertEqual(self.git('tag', '--contains', unique), '')
        self.assertEqual(self.git('for-each-ref', '--format=%(refname)', '--contains', unique), '')

    # -- 4. squash integration with identical trees still fails ancestry --

    def test_squash_integration_with_identical_trees_fails_ancestry_and_branch_delete(self):
        worktree = self.register(self.root / 'wt-squash')
        branch = self.unique_name('feature')
        self.git('worktree', 'add', '-q', str(worktree), '-b', branch)
        (worktree / 'a.txt').write_bytes(b'base\nfeature line\n')
        feature_tip = self.commit_in(worktree, 'feature work')
        feature_tree = self.git('rev-parse', f'{feature_tip}^{{tree}}').strip()
        self.assert_ok(self._git('worktree', 'remove', str(worktree)), 'worktree remove')

        # Integrate the same content as one new commit on the main branch.
        self.write('a.txt', 'base\nfeature line\n')
        squash_tip = self.commit('squash feature')
        self.assertEqual(self.git('rev-parse', f'{squash_tip}^{{tree}}').strip(), feature_tree)

        ancestry = self._git('merge-base', '--is-ancestor', feature_tip, squash_tip)
        self.assertEqual(ancestry.returncode, 1, 'identical trees must not imply commit ancestry')
        deletion = self._git('branch', '-d', branch)
        self.assertNotEqual(deletion.returncode, 0)
        self.assertEqual(self.git('rev-parse', f'refs/heads/{branch}').strip(), feature_tip)

    # -- 5. ordinary worktree add checks out the revision, not dirty files -

    def test_worktree_add_at_head_excludes_dirty_and_untracked_prerequisites(self):
        self.write('src.txt', 'committed\n')
        head = self.commit('tracked source')
        self.write('src.txt', 'committed\nuncommitted edit\n')
        self.write('scratch.txt', 'untracked draft\n')

        worktree = self.register(self.root / 'wt-clean-baseline')
        self.git('worktree', 'add', '-q', '--detach', str(worktree))

        self.assertEqual(self.rev_in(worktree), head)
        self.assertEqual((worktree / 'src.txt').read_text(encoding='utf-8'), 'committed\n')
        self.assertFalse((worktree / 'scratch.txt').exists())
        self.assertEqual(self.git('status', '--porcelain', cwd=worktree), '')
        # The dirty prerequisites remain untouched in the source checkout.
        source_status = self.git('status', '--porcelain')
        self.assertIn('src.txt', source_status)
        self.assertIn('scratch.txt', source_status)

    # -- 6. a locked worktree resists ordinary removal and keeps its lock --

    def test_locked_worktree_resists_normal_removal_and_lock_survives(self):
        worktree = self.register(self.root / 'wt-locked', unlock=True)
        branch = self.unique_name('locked')
        self.git('worktree', 'add', '-q', str(worktree), '-b', branch)
        reason = 'held for an active task'
        self.git('worktree', 'lock', '--reason', reason, str(worktree))

        self.assert_fails('worktree', 'remove', str(worktree))
        self.assertTrue(worktree.exists())
        self.assert_registered(worktree)
        self.assertIn(f'locked {reason}', self.git('worktree', 'list', '--porcelain'))

        self.git('worktree', 'unlock', str(worktree))
        listing = self.git('worktree', 'list', '--porcelain').splitlines()
        self.assertFalse([line for line in listing if line.startswith('locked')])

    # -- 7. prune dry-run reports the record a repair or prune would touch -

    def test_prune_dry_run_keeps_missing_record_and_repair_readmits_moved_tree(self):
        missing = self.register(self.root / 'wt-missing')
        self.git('worktree', 'add', '-q', str(missing), '-b', self.unique_name('stale'))
        before = self.worktree_paths()
        shutil.rmtree(missing)
        self.assertFalse(missing.exists())
        self.assert_registered(missing)

        # prune reports on stderr; assert on both streams rather than one quirk.
        dry_run = self._git('worktree', 'prune', '--dry-run', '--verbose', '--expire', 'now')
        report = dry_run.stdout + dry_run.stderr
        self.assertIn('wt-missing', report, 'dry-run must name the record it would prune')
        self.assertEqual(self.worktree_paths(), before, 'dry-run must not remove anything')

        self.assert_ok(self._git('worktree', 'prune', '--verbose', '--expire', 'now'), 'worktree prune')
        self.assertNotIn(missing.resolve(), self.worktree_paths())

        # A moved (still present) worktree is repairable, not merely prunable.
        moved = self.register(self.root / 'wt-moved')
        self.git('worktree', 'add', '-q', str(moved), '-b', self.unique_name('moved'))
        relocated = self.root / 'wt-relocated'
        moved.rename(relocated)
        try:
            self.assert_ok(self._git('worktree', 'repair', str(relocated)), 'worktree repair')
            self.assert_registered(relocated)
            self.assertEqual(self.git('status', '--porcelain', cwd=relocated), '')
        finally:
            self._git('worktree', 'remove', '--force', str(relocated))
            shutil.rmtree(relocated, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
