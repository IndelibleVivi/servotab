from __future__ import annotations

import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile

from build_release import build, release_artifacts, sha256
from selftest import contract_copy

ROOT = Path(__file__).resolve().parents[1]


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = contract_copy(ROOT, Path(self.temp.name) / 'repo')
        self.output = Path(self.temp.name) / 'output'
        self.git('init', '-q')
        self.git('config', 'user.name', 'Release fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.autocrlf', 'false')
        self.commit()

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True).stdout

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture')

    def test_reproducible_archives_and_receipt(self):
        first = release_artifacts(self.root)
        self.assertEqual(first, release_artifacts(self.root))
        receipt = json.loads(first['release-receipt.json'])
        self.assertEqual(receipt['source_commit'], self.git('rev-parse', 'HEAD').decode().strip())
        self.assertEqual(receipt['package_file_count'], 69)
        with zipfile.ZipFile(io.BytesIO(first['servotab-0.6.1-plugin.zip'])) as archive:
            names = archive.namelist()
            self.assertEqual(len(names), 69)
            self.assertEqual(len(set(names)), 69)
            manifest = json.loads((self.root/'PACK_MANIFEST.json').read_text())
            for entry in manifest['files']:
                name = entry['path'].removeprefix('plugins/')
                self.assertEqual(sha256(archive.read(name)), entry['sha256'])
            self.assertTrue(all(name.startswith('servotab/') for name in names))
        for name, meta in receipt['assets'].items():
            self.assertEqual(meta['sha256'], sha256(first[name]))
        for line in first['SHA256SUMS'].decode().splitlines():
            digest, name = line.split('  ')
            self.assertEqual(digest, sha256(first[name]))

    def test_dirty_worktree_rejected_without_output(self):
        (self.root/'VERSION').write_text('0.6.2\n')
        with self.assertRaisesRegex(ValueError, 'clean'):
            build(self.root, self.output)
        self.assertFalse(self.output.exists())

    def test_staged_change_rejected(self):
        (self.root/'new.txt').write_text('changed')
        self.git('add', '.')
        with self.assertRaisesRegex(ValueError, 'clean'):
            release_artifacts(self.root)

    def test_untracked_change_rejected(self):
        (self.root/'new.txt').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'clean'):
            release_artifacts(self.root)

    def test_existing_output_preserved(self):
        self.output.mkdir();(self.output/'keep').write_text('keep')
        with self.assertRaises(FileExistsError):
            build(self.root, self.output)
        self.assertEqual((self.output/'keep').read_text(), 'keep')

    def test_check_detects_tamper_and_extra_files(self):
        build(self.root, self.output);build(self.root, self.output, check=True)
        path=self.output/'release-receipt.json';path.write_bytes(path.read_bytes()+b' ')
        with self.assertRaisesRegex(ValueError, 'mismatch'):
            build(self.root, self.output, check=True)
        (self.output/'extra').write_text('extra')
        with self.assertRaisesRegex(ValueError, 'exactly'):
            build(self.root, self.output, check=True)

    def test_manifest_drift_rejected(self):
        (self.root/'plugins/servotab/skills/design/SKILL.md').write_text('drift')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'validation'):
            build(self.root, self.output)
        self.assertFalse(self.output.exists())

    def test_unknown_payload_rejected(self):
        (self.root/'plugins/servotab/extra').write_text('extra')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'unexpected package'):
            release_artifacts(self.root)

    def test_source_symlink_rejected(self):
        (self.root/'link').symlink_to('VERSION');self.commit()
        with self.assertRaisesRegex(ValueError, 'regular files'):
            release_artifacts(self.root)


if __name__ == '__main__':
    unittest.main()
