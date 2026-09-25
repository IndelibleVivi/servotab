"""No-model controls for diagnostic fixtures; never target-agent evidence."""
from __future__ import annotations

import contextlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

CASES = Path(__file__).resolve().parents[1] / "evals/cases"
CASE = CASES / "cross-boundary-diagnosis"


@contextlib.contextmanager
def workspace(*, repaired=False):
    with tempfile.TemporaryDirectory() as raw:
        work = Path(raw)
        shutil.copytree(CASE / "fixture", work, dirs_exist_ok=True)
        if repaired:
            shutil.copytree(CASE / "expected", work, dirs_exist_ok=True)
        yield work


def execute(work, argv):
    return subprocess.run(argv, cwd=work, capture_output=True, text=True,
                          env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                          timeout=30)


def probe(work, *args):
    result = execute(work, ["python3", "probe.py", *args])
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


class DiagnosticFixtureTests(unittest.TestCase):
    def test_green_bypass_and_shared_boundary_red(self):
        with workspace() as work:
            local = probe(work, "--requests", "8")
            client = probe(work, "--origin", "client", "--requests", "8")
            self.assertEqual((local["admission_dropped"], local["delivered"]), (0, 8))
            self.assertNotIn("admission", local["path"])
            self.assertIn("admission", client["path"])
            self.assertEqual((client["admission_dropped"], client["delivered"]), (4, 4))

    def test_comparable_red_green_and_residual_symptom(self):
        results = []
        for repaired in (False, True):
            with workspace(repaired=repaired) as work:
                results.append(probe(work, "--origin", "client", "--requests", "8"))
                if repaired:
                    noisy = probe(work, "--origin", "client", "--requests", "8", "--access", "noisy")
                    self.assertEqual((noisy["admission_dropped"], noisy["delivered"], noisy["late"]), (0, 8, 4))
        self.assertEqual([r["admission_dropped"] for r in results], [4, 0])
        self.assertEqual([r["delivered"] for r in results], [4, 8])
        for field in ("entry", "path", "requests", "relay_active", "relay_tag", "access"):
            self.assertEqual(results[0][field], results[1][field])

    def test_candidate_regression_fails_old_behavior_and_passes_repair(self):
        for repaired in (False, True):
            with self.subTest(repaired=repaired), workspace(repaired=repaired) as work:
                shutil.copyfile(CASE / "expected/test_gateway.py", work / "test_gateway.py")
                result = execute(work, ["python3", "-m", "unittest", "-q", "test_gateway"])
                self.assertEqual(result.returncode, 0 if repaired else 1, result.stderr)
                self.assertIn("Ran 2 tests", result.stderr)
                if not repaired:
                    self.assertIn("FAIL:", result.stderr)
                    self.assertNotIn("ERROR:", result.stderr)

    def test_result_oracle_rejects_plausible_wrong_repairs(self):
        case = json.loads((CASE / "case.json").read_text())
        oracle = case["command_assertions"][0]["argv"]
        variants = {
            "unchanged": (CASE / "fixture/gateway.py").read_text(),
            "disable_all_admission": "def admit(**kwargs): return True\n",
            "stale_tag_exemption": "def admit(*,origin,relay_active,relay_tag,slot): return origin=='local' or relay_tag or slot<=4\n",
            "missing_tag_match": "def admit(*,origin,relay_active,relay_tag,slot): return origin=='local' or relay_active or slot<=4\n",
            "suppress_all_work": "def admit(**kwargs): return False\n",
            "valid": (CASE / "expected/gateway.py").read_text(),
        }
        for name, code in variants.items():
            with self.subTest(variant=name), workspace(repaired=True) as work:
                (work / "gateway.py").write_text(code)
                result = execute(work, oracle)
                self.assertEqual(result.returncode == 0, name == "valid", result.stderr)

    def test_repair_preserves_non_exempt_paths(self):
        with workspace(repaired=True) as work:
            for args in (("--tag", "off"), ("--relay", "off")):
                result = probe(work, "--origin", "client", "--requests", "8", *args)
                self.assertEqual((result["admission_dropped"], result["delivered"]), (4, 4))

    def test_cases_declare_semantic_review_and_keep_reference_outputs_out_of_fixture(self):
        for name in ("cross-boundary-diagnosis", "host-specific-diagnosis", "diagnosis-progress"):
            with self.subTest(case=name):
                root = CASES / name
                case = json.loads((root / "case.json").read_text())
                self.assertEqual(case["case_id"], name)
                self.assertTrue(case["human_review_requirements"])
                self.assertTrue((root / case["prompt_file"]).is_file())
                report = "INCIDENT.md" if name == "cross-boundary-diagnosis" else "INVESTIGATION.md"
                self.assertFalse((root / "fixture" / report).exists())
                self.assertTrue((root / "expected" / report).is_file())
                # Declarations and fixture separation do not discharge semantic review.


if __name__ == "__main__":
    unittest.main()
