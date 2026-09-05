"""Exercise public fixture/expected overlays without invoking any target model."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BehaviorFixtureTests(unittest.TestCase):
    def exercise(self, name):
        case_root = ROOT / 'evals/cases' / name
        case = json.loads((case_root / 'case.json').read_text())
        with tempfile.TemporaryDirectory() as raw:
            work = Path(raw) / 'fixture'
            shutil.copytree(case_root / 'fixture', work)
            before = {p.relative_to(work): p.read_bytes() for p in work.rglob('*') if p.is_file()}
            def run(index=0):
                return subprocess.run(case['command_assertions'][index]['argv'], cwd=work,
                                      capture_output=True, timeout=20).returncode
            if name == 'weak-check':
                self.assertEqual(run(1), 0, 'the incomplete baseline unit test is intentionally green')
            self.assertNotEqual(run(), 0, 'baseline must fail the independent behavior check')
            shutil.copytree(case_root / 'expected', work, dirs_exist_ok=True)
            for cache in work.rglob('__pycache__'):
                shutil.rmtree(cache)
            self.assertTrue(all(run(i) == 0 for i in range(len(case['command_assertions']))))
            changed = {str(p.relative_to(work)) for p in work.rglob('*.py')
                       if before.get(p.relative_to(work)) != p.read_bytes()}
            self.assertEqual(changed, set(case['workspace_assertions'][0]['paths']))
            if name == 'weak-check':
                (work / 'policy.py').write_bytes(before[Path('policy.py')])
                for cache in work.rglob('__pycache__'):
                    shutil.rmtree(cache)
                self.assertNotEqual(run(1), 0, 'new regression must reject the old implementation')

    def test_local_reuse(self):
        self.exercise('local-reuse')

    def test_weak_check(self):
        self.exercise('weak-check')


if __name__ == '__main__':
    unittest.main()
