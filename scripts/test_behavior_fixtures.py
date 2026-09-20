"""No-model controls for Servotab-owned fixture assertions, not a Field Lab runner.

These tests replay result oracles only. They do not fabricate target traces,
receipts, human judgments, or evidence of improved model behavior.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals/cases"


def snapshot(work: Path) -> dict[str, bytes]:
    return {p.relative_to(work).as_posix(): p.read_bytes() for p in work.rglob("*")
            if p.is_file() and "__pycache__" not in p.parts and ".git" not in p.parts}


def check_workspace(case: dict, work: Path, before: dict[str, bytes]) -> list[bool]:
    after = snapshot(work)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    results = []
    for assertion in case.get("workspace_assertions", []):
        kind = assertion["type"]
        if kind == "changed_files_exact":
            results.append(changed == sorted(assertion["paths"]))
            continue
        path = work / assertion["path"]
        text = path.read_text(encoding="utf-8") if path.is_file() else None
        value = assertion.get("value")
        if kind == "file_exists":
            passed = path.is_file()
        elif kind == "file_equals":
            passed = text == value
        elif kind == "file_contains":
            passed = text is not None and value in text
        elif kind == "file_not_contains":
            passed = text is not None and value not in text
        else:
            raise AssertionError(f"Unsupported fixture assertion: {kind}")
        results.append(passed)
    return results


def check_commands(case: dict, work: Path) -> list[bool]:
    results = []
    for assertion in case.get("command_assertions", []):
        result = subprocess.run(assertion["argv"], cwd=work, capture_output=True,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                                timeout=assertion.get("timeout_seconds", 30))
        results.append(result.returncode == assertion.get("exit_code", 0))
    return results


class BehaviorFixtureTests(unittest.TestCase):
    def test_all_baseline_and_expected_controls(self):
        for path in sorted(CASES.glob("*/case.json")):
            with self.subTest(case=path.parent.name), tempfile.TemporaryDirectory() as raw:
                case = json.loads(path.read_text())
                work = Path(raw) / "workspace"
                shutil.copytree(path.parent / "fixture", work)
                before = snapshot(work)
                baseline = check_workspace(case, work, before) + check_commands(case, work)
                self.assertIn(False, baseline, "unresolved fixture must fail a real assertion")
                shutil.copytree(path.parent / "expected", work, dirs_exist_ok=True)
                self.assertTrue(all(check_workspace(case, work, before)))
                self.assertTrue(all(check_commands(case, work)))

    def test_adversarial_decision_controls(self):
        controls = json.loads((ROOT / "evals/adversarial-controls.json").read_text())
        self.assertEqual(len(controls), 8)
        for control in controls:
            name = control["case_id"]
            with self.subTest(case=name), tempfile.TemporaryDirectory() as raw:
                case_root = CASES / name
                case = json.loads((case_root / "case.json").read_text())
                work = Path(raw) / "workspace"
                shutil.copytree(case_root / "fixture", work)
                before = snapshot(work)
                shutil.copytree(case_root / "expected", work, dirs_exist_ok=True)
                for relative, text in control["overrides"].items():
                    (work / relative).write_text(text)
                passes = all(check_workspace(case, work, before) + check_commands(case, work))
                self.assertEqual(passes, not control["deterministic_reject"])
                if passes:
                    # A required human judgment is deliberately NOT an automatic pass.
                    # This checks declaration only; Field Lab owns receipt/review semantics.
                    self.assertTrue(case.get("human_review_requirements"))
                    self.assertTrue(control["review_reject_reason"])

    def test_scope_check_rejects_each_authority_edit_and_extra_file(self):
        root = CASES / "repeated-review-scope-accretion"
        case = json.loads((root / "case.json").read_text())
        for name in ("ACCEPTED_CONTRACT.md", "ROUND_HISTORY.md", "THIRD_REVIEW.md", "service.py"):
            with self.subTest(file=name), tempfile.TemporaryDirectory() as raw:
                work = Path(raw) / "workspace"
                shutil.copytree(root / "fixture", work)
                before = snapshot(work)
                shutil.copytree(root / "expected", work, dirs_exist_ok=True)
                (work / name).write_text("unauthorized change\n")
                self.assertIn(False, check_workspace(case, work, before))

    def test_complete_delivery_rejects_plans_and_partial_implementations(self):
        root = CASES / "complete-notes"
        case = json.loads((root / "case.json").read_text())
        for variant in ("plan_only", "add_only", "no_migration", "no_backup", "nonzero_list"):
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as raw:
                work = Path(raw) / "workspace"
                shutil.copytree(root / "fixture", work)
                before = snapshot(work)
                if variant == "plan_only":
                    (work / "IMPLEMENTATION_PLAN.md").write_text("All requirements will be implemented later.")
                    self.assertIn(False, check_workspace(case, work, before))
                    continue
                shutil.copytree(root / "expected", work, dirs_exist_ok=True)
                if variant == "add_only":
                    (work / "notes.py").write_bytes((root / "fixture/notes.py").read_bytes())
                else:
                    code = (work / "notes.py").read_text()
                    if variant == "no_migration":
                        code = code.replace("if not store.exists() and legacy.exists():", "if False:")
                    elif variant == "no_backup":
                        code = code.replace("if not backup.exists():", "if False:")
                    else:
                        code += "\nif __name__ == '__main__' and sys.argv[1:] == ['list']: raise SystemExit(2)\n"
                    (work / "notes.py").write_text(code)
                self.assertEqual(check_commands({"command_assertions": case["command_assertions"][:1]}, work), [False])

    def test_candidate_regression_requires_failure_not_broken_or_empty_suite(self):
        root = CASES / "weak-check"
        case = json.loads((root / "case.json").read_text())
        assertion = {"command_assertions": [case["command_assertions"][-1]]}
        variants = {
            "original": (root / "fixture/test_policy.py").read_text(),
            "comment_only": (root / "fixture/test_policy.py").read_text() + "\n# Regression covered.\n",
            "empty": "import unittest\n",
            "syntax_error": "this is not valid Python!\n",
            "import_error": "import nonexistent_fixture_module\n",
            "always_fails": "import unittest\nclass T(unittest.TestCase):\n def test_x(self): self.fail()\n",
            "skipped": "import unittest\n@unittest.skip('later')\nclass T(unittest.TestCase):\n def test_x(self): self.fail()\n",
            "valid": (root / "expected/test_policy.py").read_text(),
            "alternate_valid": "import unittest\nfrom policy import can_publish\nclass T(unittest.TestCase):\n def test_truth_table(self):\n  for approved in (False, True):\n   for blocked in (False, True):\n    self.assertEqual(can_publish(approved, blocked), approved and not blocked)\n",
        }
        for name, text in variants.items():
            with self.subTest(variant=name), tempfile.TemporaryDirectory() as raw:
                work = Path(raw)
                shutil.copytree(root / "expected", work, dirs_exist_ok=True)
                (work / "test_policy.py").write_text(text)
                before = snapshot(work)
                self.assertEqual(check_commands(assertion, work), [name in {"valid", "alternate_valid"}])
                self.assertEqual(snapshot(work), before, "counterfactual checks must not mutate the candidate")


if __name__ == "__main__":
    unittest.main()
