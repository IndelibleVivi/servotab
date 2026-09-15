"""Synthetic receipt/review controls. No real attempt or reviewer is represented."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from check_behavior_acceptance import ROOT, assess, digest


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


class BehaviorAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)
        self.case_id = "spec-chain"
        self.make_receipt()

    def make_receipt(self):
        case_path = ROOT / "evals/cases" / self.case_id / "case.json"
        self.case = json.loads(case_path.read_text())
        requirements = self.case.get("human_review_requirements", [])
        attempt_case = dict(self.case)
        attempt_case.update({
            "source_schema_version": 2,
            "result_assertions": self.case.get("result_assertions", {}),
            "workspace_assertions": self.case.get("workspace_assertions", []),
            "command_assertions": [
                {"type": "command", **assertion}
                for assertion in self.case.get("command_assertions", [])
            ],
            "trace_assertions": self.case.get("trace_assertions", {}),
            "human_review_requirements": requirements,
            "tags": list(self.case.get("tags", [])),
            "claim_ids": list(self.case.get("claim_ids", [])),
        })
        write_json(self.work / "case.json", attempt_case)
        (self.work / "prompt.md").write_text(case_path.with_name("prompt.md").read_text())
        (self.work / "trace.jsonl").write_text('{"test_fixture": true}\n')
        (self.work / "stderr.log").write_text("")
        (self.work / "final-output.md").write_text("Synthetic unit-test output, not a model run.\n")
        (self.work / "diff.patch").write_text("Synthetic test diff.\n")
        write_json(self.work / "verification.json", dict(passed=True, human_review_requirements=requirements))
        write_json(self.work / "metadata.json", dict(state="completed", outcome="pass"))
        self.receipt = dict(schema_version=2, receipt_type="attempt", lab_id="servotab",
                            case_id=self.case_id, outcome="pass",
                            execution_boundary=dict(quiescent=True, orphan_descendants=False),
                            verification_summary=dict(passed=True, human_review=dict(
                                required=bool(requirements), requirements=requirements,
                                status="pending" if requirements else "not-required")),
                            artifacts={})
        self.receipt_path = self.work / "receipt.json"
        self.seal()

    def seal(self):
        from check_behavior_acceptance import REQUIRED_ARTIFACTS
        self.receipt["artifacts"] = {name: dict(sha256=digest(self.work / name), bytes=(self.work / name).stat().st_size)
                                     for name in REQUIRED_ARTIFACTS}
        write_json(self.receipt_path, self.receipt)

    def review(self, **changes):
        value = dict(schema_version=2, review_id="synthetic-control", created_at="2026-09-09",
                     receipt=dict(path=str(self.receipt_path), sha256=digest(self.receipt_path)),
                     method="human", independence="external-reviewer", judgment="supported",
                     rationale="Synthetic test judgment; no real reviewer or model run.",
                     requirement_outcomes={req: "supported" for req in self.case.get("human_review_requirements", [])})
        value.update(changes)
        path = self.work / "review.json"
        write_json(path, value)
        return path

    def test_deterministic_green_stays_pending_without_review(self):
        before = {p.name: p.read_bytes() for p in self.work.iterdir()}
        self.assertEqual(assess(self.receipt_path)["status"], "needs-review")
        self.assertEqual({p.name: p.read_bytes() for p in self.work.iterdir()}, before)

    def test_independent_supported_review_accepts(self):
        self.assertEqual(assess(self.receipt_path, self.review())["status"], "accepted")

    def test_real_fieldlab_case_defaults_are_part_of_attempt_identity(self):
        attempt_case = json.loads((self.work / "case.json").read_text())
        self.assertEqual(attempt_case["source_schema_version"], 2)
        self.assertEqual(attempt_case["result_assertions"], {})
        self.assertEqual(attempt_case["tags"], [])
        self.assertEqual(attempt_case["claim_ids"], [])

    def test_rejected_or_inconclusive_judgment_cannot_pass(self):
        for value, expected in (("not-supported", "rejected"), ("inconclusive", "needs-review")):
            with self.subTest(value=value):
                self.assertEqual(assess(self.receipt_path, self.review(judgment=value))["status"], expected)

    def test_one_failed_requirement_overrides_supported_summary(self):
        outcomes = {req: "supported" for req in self.case["human_review_requirements"]}
        outcomes[next(iter(outcomes))] = "not-supported"
        self.assertEqual(assess(self.receipt_path, self.review(requirement_outcomes=outcomes))["status"], "rejected")

    def test_missing_extra_or_free_text_requirement_outcomes_fail_closed(self):
        for outcomes in ({}, {"invented": "supported"},
                         {req: "looks good" for req in self.case["human_review_requirements"]}):
            with self.subTest(outcomes=outcomes), self.assertRaises(ValueError):
                assess(self.receipt_path, self.review(requirement_outcomes=outcomes))

    def test_self_review_does_not_close_independent_requirement(self):
        self.assertEqual(assess(self.receipt_path, self.review(independence="implementer-run"))["status"], "needs-review")

    def test_stale_review_digest_fails(self):
        review = self.review(receipt=dict(path=str(self.receipt_path), sha256="0" * 64))
        with self.assertRaisesRegex(ValueError, "different receipt"):
            assess(self.receipt_path, review)

    def test_failed_attempt_cannot_be_rescued_by_review(self):
        self.receipt["outcome"] = "fail"; self.seal()
        self.assertEqual(assess(self.receipt_path, self.review())["status"], "rejected")

    def test_missing_tampered_and_symlink_artifacts_fail(self):
        path = self.work / "final-output.md"
        original = path.read_bytes()
        path.write_text("Changed after receipt.\n")
        with self.assertRaisesRegex(ValueError, "identity mismatch"):
            assess(self.receipt_path)
        path.unlink()
        with self.assertRaises(ValueError):
            assess(self.receipt_path)
        target = self.work / "elsewhere"; target.write_bytes(original)
        path.symlink_to(target)
        with self.assertRaises(ValueError):
            assess(self.receipt_path)

    def test_omitted_or_rewritten_review_requirements_fail(self):
        self.receipt["verification_summary"]["human_review"]["requirements"] = []
        self.seal()
        with self.assertRaisesRegex(ValueError, "disagree"):
            assess(self.receipt_path)

    def test_stale_case_rejected_even_with_resealed_artifacts(self):
        self.case["description"] = "Old or substituted case."
        write_json(self.work / "case.json", self.case); self.seal()
        with self.assertRaisesRegex(ValueError, "current checked-out case"):
            assess(self.receipt_path)

    def test_unknown_case_observed_receipt_and_nonquiescent_fail(self):
        for key, value in (("case_id", "unknown"), ("receipt_type", "observed"),
                           ("execution_boundary", dict(quiescent=False, orphan_descendants=False))):
            original = self.receipt[key]; self.receipt[key] = value; self.seal()
            with self.subTest(key=key), self.assertRaises(ValueError):
                assess(self.receipt_path)
            self.receipt[key] = original

    def test_duplicate_keys_rejected(self):
        self.receipt_path.write_text('{"schema_version": 2, "schema_version": 2}')
        with self.assertRaisesRegex(ValueError, "duplicate"):
            assess(self.receipt_path)

    def test_pure_deterministic_case_does_not_acquire_mandatory_review(self):
        self.case_id = "tiny-copy"; self.make_receipt()
        self.assertEqual(assess(self.receipt_path)["status"], "accepted")

    def test_cli_exit_statuses_are_machine_usable(self):
        script = ROOT / "scripts/check_behavior_acceptance.py"
        for args, expected in (([], 2), (["--review", str(self.review())], 0)):
            result = subprocess.run([sys.executable, "-S", str(script), str(self.receipt_path), *args], capture_output=True, text=True)
            self.assertEqual(result.returncode, expected, result.stderr)
            self.assertIn("status", json.loads(result.stdout))

    def test_semantic_audit_outputs_require_review_then_honor_rejection(self):
        controls = json.loads((ROOT / "evals/adversarial-controls.json").read_text())
        for control in controls:
            if control["deterministic_reject"]:
                continue
            with self.subTest(case=control["case_id"]):
                self.case_id = control["case_id"]; self.make_receipt()
                (self.work / "diff.patch").write_text(json.dumps(control["overrides"]))
                self.seal()
                self.assertEqual(assess(self.receipt_path)["status"], "needs-review")
                # The stored reason is a synthetic reviewer control, not an LLM grader.
                review = self.review(judgment="not-supported", rationale=control["review_reject_reason"],
                                     requirement_outcomes={req: "not-supported" for req in self.case["human_review_requirements"]})
                self.assertEqual(assess(self.receipt_path, review)["status"], "rejected")
