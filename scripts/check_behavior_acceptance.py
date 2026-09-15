#!/usr/bin/env python3
"""Read-only Servotab acceptance of a Field Lab v2 attempt and separate review.

No runner, model, installer, grader or receipt writer. A deterministic Field Lab
pass is provisional when the case declares semantic review requirements.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ARTIFACTS = {"case.json", "prompt.md", "trace.jsonl", "stderr.log",
                      "final-output.md", "diff.patch", "verification.json", "metadata.json"}
EXIT = {"accepted": 0, "rejected": 1, "needs-review": 2, "invalid-evidence": 3}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_json(path: Path) -> dict:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 2_000_000:
        raise ValueError(f"expected bounded regular JSON file: {path.name}")
    data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path.name}")
    return data


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(65536), b""):
            value.update(chunk)
    return value.hexdigest()


def fieldlab_attempt_case(case: dict) -> dict:
    """Project one raw v2 case into the record shape stored by Field Lab."""
    normalized = dict(case)
    normalized.update({
        "source_schema_version": 2,
        "result_assertions": case.get("result_assertions", {}),
        "workspace_assertions": case.get("workspace_assertions", []),
        "command_assertions": [
            {"type": "command", **assertion}
            for assertion in case.get("command_assertions", [])
        ],
        "trace_assertions": case.get("trace_assertions", {}),
        "human_review_requirements": case.get("human_review_requirements", []),
        "tags": list(case.get("tags", [])),
        "claim_ids": list(case.get("claim_ids", [])),
    })
    return normalized


def assess(receipt_path: Path, review_path: Path | None = None) -> dict:
    receipt = read_json(receipt_path)
    if (receipt.get("schema_version") != 2 or receipt.get("receipt_type") != "attempt"
            or receipt.get("lab_id") != "servotab"):
        raise ValueError("expected a Servotab Field Lab v2 attempt receipt")
    case_id = receipt.get("case_id")
    case_paths = {p.parent.name: p for p in (ROOT / "evals/cases").glob("*/case.json")}
    if case_id not in case_paths:
        raise ValueError("unknown Servotab case")
    case = read_json(case_paths[case_id])
    result = {"case_id": case_id, "receipt_sha256": digest(receipt_path),
              "scope": "This pinned case only; no general effectiveness or host-acceptance claim."}
    def verdict(status, reason):
        return {**result, "status": status, "reason": reason}
    if receipt.get("outcome") != "pass":
        return verdict("rejected", "The attempt did not pass deterministic verification.")
    boundary = receipt.get("execution_boundary", {})
    if boundary.get("quiescent") is not True or boundary.get("orphan_descendants") is not False:
        raise ValueError("execution quiescence is not established")
    artifacts = receipt.get("artifacts", {})
    if set(artifacts) != REQUIRED_ARTIFACTS:
        raise ValueError("missing or unexpected attempt artifact set")
    root = receipt_path.parent
    for name, identity in artifacts.items():
        path = root / name
        if (path.is_symlink() or not path.is_file()
                or identity.get("bytes") != path.stat().st_size
                or identity.get("sha256") != digest(path)):
            raise ValueError(f"artifact identity mismatch: {name}")
    if read_json(root / "case.json") != fieldlab_attempt_case(case):
        raise ValueError("attempt case differs from the current checked-out case; use its pinned revision")
    if (root / "prompt.md").read_text().strip() != (case_paths[case_id].parent / case["prompt_file"]).read_text().strip():
        raise ValueError("attempt prompt differs from the checked-out case")
    verification = read_json(root / "verification.json")
    metadata = read_json(root / "metadata.json")
    if metadata.get("state") != "completed" or metadata.get("outcome") != "pass":
        raise ValueError("attempt metadata disagrees with the receipt")
    requirements = case.get("human_review_requirements", [])
    human = receipt.get("verification_summary", {}).get("human_review", {})
    if (verification.get("passed") is not True
            or receipt.get("verification_summary", {}).get("passed") is not True
            or verification.get("human_review_requirements", []) != requirements
            or human.get("required") is not bool(requirements)
            or human.get("requirements") != requirements):
        raise ValueError("verification summary or review requirements disagree")
    if review_path is None:
        if requirements:
            return verdict("needs-review", "Deterministic pass only; declared semantic requirements remain unreviewed.")
        return verdict("accepted", "The case's declared deterministic checks passed; no semantic review was declared.")
    review = read_json(review_path)
    if (review.get("schema_version") != 2 or review.get("method") != "human"
            or not review.get("review_id") or not review.get("created_at")
            or review.get("receipt", {}).get("sha256") != result["receipt_sha256"]):
        raise ValueError("review is malformed or bound to a different receipt")
    if review.get("independence") not in {"separate-agent", "external-reviewer"}:
        return verdict("needs-review", "This subject requires review independent of the implementer.")
    outcomes = review.get("requirement_outcomes", {})
    if (not isinstance(review.get("rationale"), str) or not review["rationale"].strip()
            or not isinstance(outcomes, dict) or set(outcomes) != set(requirements)
            or any(value not in {"supported", "not-supported", "inconclusive"} for value in outcomes.values())):
        raise ValueError("review must give a rationale and an explicit outcome for every exact requirement")
    judgment = review.get("judgment")
    if judgment not in {"supported", "not-supported", "inconclusive"}:
        raise ValueError("invalid review judgment")
    if judgment == "not-supported" or "not-supported" in outcomes.values():
        return verdict("rejected", "The independent review rejects at least one required behavior.")
    if judgment == "inconclusive" or "inconclusive" in outcomes.values():
        return verdict("needs-review", "The independent review leaves a requirement unresolved.")
    return verdict("accepted", "Deterministic evidence and the receipt-bound independent review support this case.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--review", type=Path)
    args = parser.parse_args()
    try:
        result = assess(args.receipt, args.review)
    except (ValueError, OSError, TypeError, KeyError, AttributeError) as error:
        result = {"status": "invalid-evidence", "reason": str(error)}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return EXIT[result["status"]]


if __name__ == "__main__":
    sys.exit(main())
