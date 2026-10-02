"""Discriminating Plan fixture controls; no target-model or routing evidence."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from test_behavior_fixtures import check_commands, check_workspace, snapshot

ROOT = Path(__file__).resolve().parents[1] / "evals/cases"


class PlanFixtureTests(unittest.TestCase):
    def test_complete_export_oracle_rejects_lossy_collectors(self):
        root = ROOT / "plan-shared-assumption"
        case = json.loads((root / "case.json").read_text())
        correct = (root / "expected/exporter.py").read_text()
        variants = {
            "complete": correct,
            "first-page": (root / "fixture/exporter.py").read_text(),
            "deduplicate-title": correct.replace('row["id"]', 'row["title"]'),
            "keep-overlap": correct.replace('if row["id"] not in seen:', 'if True:'),
            "hardcoded-cursor": correct.replace('page, cursor = fetch_page(cursor)', 'page, cursor = fetch_page(None if cursor is None else "next:blue" if cursor == "next:blue" else "last:gold")'),
        }
        for name, code in variants.items():
            with self.subTest(variant=name), tempfile.TemporaryDirectory() as raw:
                work = Path(raw)
                shutil.copytree(root / "fixture", work, dirs_exist_ok=True)
                (work / "exporter.py").write_text(code)
                self.assertEqual(check_commands(case, work), [name == "complete"])

    def test_resume_scope_rejects_decoy_private_and_parallel_records(self):
        root = ROOT / "plan-resume-reconcile"
        case = json.loads((root / "case.json").read_text())
        for changed in ("docs/plans/recent-search.md", "PRIVATE.md", "docs/plans/active_plan.md"):
            with self.subTest(path=changed), tempfile.TemporaryDirectory() as raw:
                work = Path(raw)
                shutil.copytree(root / "fixture", work, dirs_exist_ok=True)
                before = snapshot(work)
                shutil.copytree(root / "expected", work, dirs_exist_ok=True)
                self.assertTrue(all(check_workspace(case, work, before)))
                (work / changed).write_text("An unauthorized competing record or edit.\n")
                self.assertIn(False, check_workspace(case, work, before))


if __name__ == "__main__":
    unittest.main()
