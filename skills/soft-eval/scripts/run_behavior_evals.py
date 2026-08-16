#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from collections.abc import Iterator
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from unittest import mock


SCHEMA_VERSION = 1
CASE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
HEX_DIGEST_RE = re.compile(r"^[0-9a-f]{40,64}$")
REFERENCE_RE = re.compile(r"references[/\\]([A-Za-z0-9._-]+\.md)")
ASSERTION_TYPES = {
    "file_equals",
    "file_contains",
    "file_not_contains",
    "file_exists",
    "changed_files_exact",
    "command",
}
TRACE_ASSERTION_KEYS = {
    "max_command_executions",
    "max_plan_updates",
    "max_subagent_events",
    "reference_reads_include",
}


class EvalConfigError(ValueError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return f"{stamp}-{uuid.uuid4().hex[:8]}"


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{uuid.uuid4().hex}")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def atomic_write_json(path: Path, value: object) -> None:
    atomic_write_text(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@contextlib.contextmanager
def change_directory(path: Path) -> Iterator[None]:
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def fixture_tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        if path.is_symlink():
            kind = b"symlink"
            payload = os.readlink(path).encode("utf-8")
        elif path.is_file():
            kind = b"executable" if path.stat().st_mode & 0o111 else b"file"
            payload = path.read_bytes()
        else:
            continue
        digest.update(kind + b"\0" + relative + b"\0")
        digest.update(len(payload).to_bytes(8, "big") + payload)
    return digest.hexdigest()


def case_input_identity(case_dir: Path, case: dict[str, Any]) -> dict[str, str]:
    prompt = (case_dir / str(case["prompt_file"])).read_text(encoding="utf-8").strip()
    case_text = json.dumps(case, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return {
        "case_sha256": sha256_text(case_text),
        "fixture_tree": fixture_tree_digest(case_dir / "fixture"),
        "prompt_sha256": sha256_text(prompt),
    }


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise EvalConfigError(f"missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise EvalConfigError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EvalConfigError(f"JSON root must be an object: {path}")
    return value


def safe_relative(root: Path, relative_text: str) -> Path:
    relative = Path(relative_text)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        raise EvalConfigError(f"unsafe relative path: {relative_text!r}")
    resolved = (root / relative).resolve(strict=False)
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise EvalConfigError(f"path escapes root: {relative_text!r}") from exc
    return resolved


def discover_layout(script_path: Path | None = None) -> tuple[Path, Path]:
    script = (script_path or Path(__file__)).resolve()
    source_cases = script.parent / "cases"
    source_schemas = script.parent / "schemas"
    if source_cases.is_dir() and source_schemas.is_dir():
        return source_cases, source_schemas

    skill_root = script.parent.parent
    installed_cases = skill_root / "assets" / "cases"
    installed_schemas = skill_root / "assets" / "schemas"
    if installed_cases.is_dir() and installed_schemas.is_dir():
        return installed_cases, installed_schemas

    raise EvalConfigError(
        "could not locate eval cases and schemas beside the source or installed soft-eval skill"
    )


def default_output_root(script_path: Path | None = None) -> Path:
    script = (script_path or Path(__file__)).resolve()
    source_root = script.parent.parent
    if (source_root / "VERSION").is_file():
        return source_root / ".softpowers-evals"
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    return codex_home / "softpowers-evals"


def validate_assertion(assertion: object, label: str) -> None:
    if not isinstance(assertion, dict):
        raise EvalConfigError(f"{label}: assertion must be an object")
    assertion_type = assertion.get("type")
    if assertion_type not in ASSERTION_TYPES:
        raise EvalConfigError(f"{label}: unsupported assertion type {assertion_type!r}")

    if assertion_type in {"file_equals", "file_contains", "file_not_contains"}:
        expected_keys = {"type", "path", "value"}
        if set(assertion) != expected_keys:
            raise EvalConfigError(f"{label}: {assertion_type} requires exactly {sorted(expected_keys)}")
        if not isinstance(assertion["path"], str) or not isinstance(assertion["value"], str):
            raise EvalConfigError(f"{label}: path and value must be strings")
        safe_relative(Path("/case-root"), assertion["path"])
        return

    if assertion_type == "file_exists":
        if set(assertion) != {"type", "path"} or not isinstance(assertion.get("path"), str):
            raise EvalConfigError(f"{label}: file_exists requires string path")
        safe_relative(Path("/case-root"), assertion["path"])
        return

    if assertion_type == "changed_files_exact":
        if set(assertion) != {"type", "paths"}:
            raise EvalConfigError(f"{label}: changed_files_exact requires paths")
        paths = assertion.get("paths")
        if not isinstance(paths, list) or not all(isinstance(item, str) for item in paths):
            raise EvalConfigError(f"{label}: changed paths must be strings")
        if len(paths) != len(set(paths)):
            raise EvalConfigError(f"{label}: changed paths must be unique")
        for path in paths:
            safe_relative(Path("/case-root"), path)
        return

    allowed = {"type", "argv", "exit_code", "timeout_seconds"}
    extra = set(assertion) - allowed
    argv = assertion.get("argv")
    if extra or not isinstance(argv, list) or not argv or not all(isinstance(item, str) for item in argv):
        raise EvalConfigError(f"{label}: command requires a non-empty string argv and known fields")
    exit_code = assertion.get("exit_code", 0)
    timeout_seconds = assertion.get("timeout_seconds", 30)
    if not isinstance(exit_code, int):
        raise EvalConfigError(f"{label}: command exit_code must be an integer")
    if not isinstance(timeout_seconds, int) or not 1 <= timeout_seconds <= 300:
        raise EvalConfigError(f"{label}: command timeout_seconds must be 1..300")


def load_case(case_dir: Path) -> dict[str, Any]:
    case_path = case_dir / "case.json"
    case = read_json(case_path)
    required = {
        "schema_version",
        "case_id",
        "description",
        "prompt_file",
        "sandbox",
        "timeout_seconds",
        "assertions",
    }
    allowed = required | {"trace_assertions"}
    missing = required - set(case)
    extra = set(case) - allowed
    if missing or extra:
        raise EvalConfigError(
            f"{case_path}: case fields mismatch; missing={sorted(missing)}, extra={sorted(extra)}"
        )
    if case["schema_version"] != SCHEMA_VERSION:
        raise EvalConfigError(f"{case_path}: unsupported schema_version")
    case_id = case.get("case_id")
    if not isinstance(case_id, str) or not CASE_ID_RE.fullmatch(case_id):
        raise EvalConfigError(f"{case_path}: invalid case_id")
    if case_id != case_dir.name:
        raise EvalConfigError(f"{case_path}: case_id must match directory name")
    if not isinstance(case.get("description"), str) or not case["description"].strip():
        raise EvalConfigError(f"{case_path}: description must be non-empty")
    prompt_file = case.get("prompt_file")
    if not isinstance(prompt_file, str) or Path(prompt_file).name != prompt_file:
        raise EvalConfigError(f"{case_path}: prompt_file must be one filename")
    if not (case_dir / prompt_file).is_file():
        raise EvalConfigError(f"{case_path}: prompt file missing")
    if not (case_dir / "fixture").is_dir() or not (case_dir / "expected").is_dir():
        raise EvalConfigError(f"{case_path}: fixture/ and expected/ are required")
    if case.get("sandbox") not in {"read-only", "workspace-write"}:
        raise EvalConfigError(f"{case_path}: unsupported sandbox")
    timeout_seconds = case.get("timeout_seconds")
    if not isinstance(timeout_seconds, int) or not 30 <= timeout_seconds <= 3600:
        raise EvalConfigError(f"{case_path}: timeout_seconds must be 30..3600")
    assertions = case.get("assertions")
    if not isinstance(assertions, list) or not assertions:
        raise EvalConfigError(f"{case_path}: assertions must be non-empty")
    for index, assertion in enumerate(assertions):
        validate_assertion(assertion, f"{case_path}: assertions[{index}]")

    trace_assertions = case.get("trace_assertions", {})
    if not isinstance(trace_assertions, dict) or set(trace_assertions) - TRACE_ASSERTION_KEYS:
        raise EvalConfigError(f"{case_path}: invalid trace_assertions")
    for key in ("max_command_executions", "max_plan_updates", "max_subagent_events"):
        value = trace_assertions.get(key)
        if value is not None and (not isinstance(value, int) or value < 0):
            raise EvalConfigError(f"{case_path}: {key} must be a non-negative integer")
    references = trace_assertions.get("reference_reads_include", [])
    if not isinstance(references, list) or not all(isinstance(item, str) and item for item in references):
        raise EvalConfigError(f"{case_path}: reference_reads_include must be strings")
    if len(references) != len(set(references)):
        raise EvalConfigError(f"{case_path}: reference_reads_include must be unique")
    return case


def load_cases(cases_root: Path) -> dict[str, tuple[Path, dict[str, Any]]]:
    cases: dict[str, tuple[Path, dict[str, Any]]] = {}
    for case_dir in sorted(cases_root.iterdir()):
        if not case_dir.is_dir() or case_dir.name.startswith("."):
            continue
        case = load_case(case_dir)
        cases[str(case["case_id"])] = (case_dir, case)
    if not cases:
        raise EvalConfigError(f"no eval cases found in {cases_root}")
    return cases


def run_command(
    argv: list[str],
    *,
    cwd: Path,
    timeout: int = 30,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
    )


def initialize_fixture(fixture: Path, workspace: Path) -> None:
    if workspace.exists():
        shutil.rmtree(workspace)
    shutil.copytree(fixture, workspace)
    run_command(["git", "init", "-q"], cwd=workspace, check=True)
    run_command(["git", "config", "user.name", "Softpowers Eval"], cwd=workspace, check=True)
    run_command(
        ["git", "config", "user.email", "softpowers-eval@example.invalid"],
        cwd=workspace,
        check=True,
    )
    run_command(["git", "add", "--all"], cwd=workspace, check=True)
    run_command(
        ["git", "commit", "--no-gpg-sign", "-q", "-m", "fixture baseline"],
        cwd=workspace,
        check=True,
    )


def apply_expected(expected: Path, workspace: Path) -> None:
    for source in sorted(expected.rglob("*")):
        if not source.is_file():
            continue
        target = workspace / source.relative_to(expected)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def changed_files(workspace: Path) -> list[str]:
    result = run_command(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=workspace,
        check=True,
    )
    fields = result.stdout.split("\0")
    paths: list[str] = []
    index = 0
    while index < len(fields):
        entry = fields[index]
        if not entry:
            index += 1
            continue
        if len(entry) < 4 or entry[2] != " ":
            raise EvalConfigError("git status returned an invalid porcelain v1 record")
        status = entry[:2]
        paths.append(entry[3:])
        index += 2 if "R" in status or "C" in status else 1
    return sorted(set(paths))


def capture_diff(workspace: Path) -> str:
    run_command(["git", "add", "-N", "--all"], cwd=workspace, check=True)
    result = run_command(
        ["git", "diff", "--binary", "--no-ext-diff", "HEAD", "--"],
        cwd=workspace,
        check=True,
    )
    return result.stdout


def assertion_result(
    assertion_type: str,
    passed: bool,
    message: str,
    **details: object,
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "type": assertion_type,
        "passed": passed,
        "message": message,
    }
    if details:
        value["details"] = details
    return value


def evaluate_assertions(case: dict[str, Any], workspace: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for assertion in case["assertions"]:
        assertion_type = str(assertion["type"])
        if assertion_type == "changed_files_exact":
            actual = changed_files(workspace)
            expected = sorted(assertion["paths"])
            results.append(
                assertion_result(
                    assertion_type,
                    actual == expected,
                    "changed file set matches" if actual == expected else "changed file set differs",
                    expected=expected,
                    actual=actual,
                )
            )
            continue

        if assertion_type == "command":
            expected_code = int(assertion.get("exit_code", 0))
            try:
                completed = run_command(
                    list(assertion["argv"]),
                    cwd=workspace,
                    timeout=int(assertion.get("timeout_seconds", 30)),
                )
                actual_code: int | str = completed.returncode
                stdout = completed.stdout[-20000:]
                stderr = completed.stderr[-20000:]
                passed = completed.returncode == expected_code
                message = "command exit matched" if passed else "command exit differed"
            except subprocess.TimeoutExpired as exc:
                actual_code = "timeout"
                stdout = (exc.stdout or "")[-20000:] if isinstance(exc.stdout, str) else ""
                stderr = (exc.stderr or "")[-20000:] if isinstance(exc.stderr, str) else ""
                passed = False
                message = "command timed out"
            results.append(
                assertion_result(
                    assertion_type,
                    passed,
                    message,
                    argv=assertion["argv"],
                    expected_exit_code=expected_code,
                    actual_exit_code=actual_code,
                    stdout=stdout,
                    stderr=stderr,
                )
            )
            continue

        path = safe_relative(workspace, str(assertion["path"]))
        if assertion_type == "file_exists":
            passed = path.is_file()
            results.append(
                assertion_result(
                    assertion_type,
                    passed,
                    "file exists" if passed else "file missing",
                    path=assertion["path"],
                )
            )
            continue

        if not path.is_file():
            results.append(
                assertion_result(
                    assertion_type,
                    False,
                    "file missing",
                    path=assertion["path"],
                )
            )
            continue
        actual_text = path.read_text(encoding="utf-8")
        expected_text = str(assertion["value"])
        if assertion_type == "file_equals":
            passed = actual_text == expected_text
        elif assertion_type == "file_contains":
            passed = expected_text in actual_text
        else:
            passed = expected_text not in actual_text
        results.append(
            assertion_result(
                assertion_type,
                passed,
                "file assertion passed" if passed else "file assertion failed",
                path=assertion["path"],
                value=expected_text,
            )
        )
    return results


def parse_trace(trace_path: Path) -> dict[str, Any]:
    event_types: dict[str, int] = {}
    item_types: dict[str, int] = {}
    unknown_event_types: set[str] = set()
    unknown_item_types: set[str] = set()
    command_ids: set[str] = set()
    command_texts: list[str] = []
    plan_ids: set[str] = set()
    subagent_ids: set[str] = set()
    reference_reads: set[str] = set()
    final_messages: list[str] = []
    usage: dict[str, Any] = {}
    errors: list[str] = []
    malformed_lines = 0
    thread_started = False
    turn_completed = False

    known_item_types = {
        "agent_message",
        "reasoning",
        "command_execution",
        "file_change",
        "mcp_tool_call",
        "web_search",
        "plan_update",
        "todo_list",
    }

    if not trace_path.is_file():
        return {
            "event_types": {},
            "item_types": {},
            "unknown_event_types": [],
            "unknown_item_types": [],
            "command_executions": 0,
            "commands": [],
            "plan_updates": 0,
            "subagent_events": 0,
            "reference_reads": [],
            "final_message": "",
            "usage": {},
            "errors": ["trace file missing"],
            "malformed_lines": 0,
            "thread_started": False,
            "turn_completed": False,
        }

    for line_number, raw_line in enumerate(trace_path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError:
            malformed_lines += 1
            continue
        if not isinstance(event, dict):
            malformed_lines += 1
            continue
        event_type = str(event.get("type", "<missing>"))
        event_types[event_type] = event_types.get(event_type, 0) + 1
        if not (
            event_type.startswith("thread.")
            or event_type.startswith("turn.")
            or event_type.startswith("item.")
            or event_type == "error"
        ):
            unknown_event_types.add(event_type)
        if event_type == "thread.started":
            thread_started = True
        if event_type == "turn.completed":
            turn_completed = True
            if isinstance(event.get("usage"), dict):
                usage = dict(event["usage"])
        if event_type in {"turn.failed", "error"}:
            errors.append(json.dumps(event, ensure_ascii=False))

        item = event.get("item")
        if not isinstance(item, dict):
            continue
        item_type = str(item.get("type", "<missing>"))
        item_types[item_type] = item_types.get(item_type, 0) + 1
        if item_type not in known_item_types and not any(
            marker in item_type for marker in ("plan", "agent", "collab")
        ):
            unknown_item_types.add(item_type)
        item_id = str(item.get("id", f"line-{line_number}"))

        if item_type == "command_execution":
            command_ids.add(item_id)
            command = item.get("command")
            if isinstance(command, str) and command not in command_texts:
                command_texts.append(command)
                reference_reads.update(REFERENCE_RE.findall(command))
        if "plan" in item_type or item_type == "todo_list":
            plan_ids.add(item_id)
        if any(marker in item_type for marker in ("subagent", "collab")):
            subagent_ids.add(item_id)
        if item_type == "mcp_tool_call":
            name = " ".join(
                str(item.get(key, "")) for key in ("server", "tool", "name")
            ).lower()
            if any(marker in name for marker in ("spawn_agent", "subagent", "collaboration")):
                subagent_ids.add(item_id)
        if event_type == "item.completed" and item_type == "agent_message":
            text = item.get("text")
            if isinstance(text, str):
                final_messages.append(text)

    return {
        "event_types": dict(sorted(event_types.items())),
        "item_types": dict(sorted(item_types.items())),
        "unknown_event_types": sorted(unknown_event_types),
        "unknown_item_types": sorted(unknown_item_types),
        "command_executions": len(command_ids),
        "commands": command_texts,
        "plan_updates": len(plan_ids),
        "subagent_events": len(subagent_ids),
        "reference_reads": sorted(reference_reads),
        "final_message": final_messages[-1] if final_messages else "",
        "usage": usage,
        "errors": errors,
        "malformed_lines": malformed_lines,
        "thread_started": thread_started,
        "turn_completed": turn_completed,
    }


def evaluate_trace(case: dict[str, Any], summary: dict[str, Any]) -> list[dict[str, Any]]:
    results = [
        assertion_result(
            "trace_jsonl_valid",
            summary["malformed_lines"] == 0,
            "trace JSONL is valid" if summary["malformed_lines"] == 0 else "trace has malformed lines",
            malformed_lines=summary["malformed_lines"],
        ),
        assertion_result(
            "trace_completed",
            bool(summary["thread_started"] and summary["turn_completed"] and not summary["errors"]),
            "thread completed without trace errors"
            if summary["thread_started"] and summary["turn_completed"] and not summary["errors"]
            else "thread completion evidence is incomplete",
            thread_started=summary["thread_started"],
            turn_completed=summary["turn_completed"],
            errors=summary["errors"],
        ),
    ]
    expectations = case.get("trace_assertions", {})
    metrics = {
        "max_command_executions": "command_executions",
        "max_plan_updates": "plan_updates",
        "max_subagent_events": "subagent_events",
    }
    for expectation, metric in metrics.items():
        if expectation not in expectations:
            continue
        maximum = int(expectations[expectation])
        actual = int(summary[metric])
        results.append(
            assertion_result(
                expectation,
                actual <= maximum,
                f"{metric} within limit" if actual <= maximum else f"{metric} exceeded limit",
                maximum=maximum,
                actual=actual,
            )
        )
    actual_references = set(summary["reference_reads"])
    for expected in expectations.get("reference_reads_include", []):
        passed = expected in actual_references
        results.append(
            assertion_result(
                "reference_reads_include",
                passed,
                "required reference observed" if passed else "required reference not observed",
                expected=expected,
                actual=sorted(actual_references),
            )
        )
    return results


def runner_identity(script_path: Path, codex_version: str) -> dict[str, Any]:
    script = script_path.resolve()
    identity: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "codex": codex_version,
        "runner_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
    }
    source_root = script.parent.parent
    version_path = source_root / "VERSION"
    if version_path.is_file():
        identity["softpowers_version"] = version_path.read_text(encoding="utf-8").strip()
        try:
            commit = run_command(["git", "rev-parse", "HEAD"], cwd=source_root, check=True)
            identity["source_commit"] = commit.stdout.strip()
            status = run_command(
                ["git", "status", "--porcelain=v1", "--untracked-files=all"],
                cwd=source_root,
                check=True,
            )
            identity["source_dirty"] = bool(status.stdout)
        except (subprocess.SubprocessError, OSError):
            identity["source_commit"] = None
            identity["source_dirty"] = None
        identity["mode"] = "source"
        return identity

    skill_root = script.parent.parent
    skills_root = skill_root.parent
    pointer = skills_root / ".softpowers-current-manifest"
    if pointer.is_file():
        manifest_path = Path(pointer.read_text(encoding="utf-8").strip()).expanduser()
        try:
            manifest = read_json(manifest_path)
            identity["softpowers_version"] = manifest.get("version")
            identity["manifest"] = manifest_path.name
        except EvalConfigError:
            identity["softpowers_version"] = None
            identity["manifest"] = None
    else:
        identity["softpowers_version"] = None
        identity["manifest"] = None
    identity["mode"] = "installed"
    return identity


def next_attempt_dir(repeat_dir: Path) -> Path:
    indexes = []
    for path in repeat_dir.glob("attempt-*"):
        try:
            indexes.append(int(path.name.removeprefix("attempt-")))
        except ValueError:
            continue
    return repeat_dir / f"attempt-{(max(indexes, default=0) + 1):03d}"


def completed_attempt(repeat_dir: Path) -> dict[str, Any] | None:
    for path in sorted(repeat_dir.glob("attempt-*/metadata.json"), reverse=True):
        try:
            metadata = read_json(path)
        except EvalConfigError:
            continue
        if metadata.get("state") == "completed":
            return metadata
    return None


def validate_attempt_metadata(metadata: dict[str, Any]) -> None:
    expected = {
        "schema_version",
        "state",
        "outcome",
        "run_id",
        "case_id",
        "subject_id",
        "repeat",
        "started_at",
        "updated_at",
        "inputs",
        "runner",
        "execution",
        "artifacts",
    }
    if set(metadata) != expected:
        raise EvalConfigError(
            "attempt metadata fields mismatch; "
            f"missing={sorted(expected - set(metadata))}, extra={sorted(set(metadata) - expected)}"
        )
    if metadata.get("schema_version") != SCHEMA_VERSION:
        raise EvalConfigError("attempt metadata has unsupported schema_version")
    if metadata.get("state") not in {"running", "completed"}:
        raise EvalConfigError("attempt metadata has invalid state")
    if metadata.get("outcome") not in {"pending", "pass", "fail", "error", "timeout"}:
        raise EvalConfigError("attempt metadata has invalid outcome")
    if metadata["state"] == "running" and metadata["outcome"] != "pending":
        raise EvalConfigError("running attempt metadata must have pending outcome")
    if metadata["state"] == "completed" and metadata["outcome"] == "pending":
        raise EvalConfigError("completed attempt metadata cannot have pending outcome")
    for key in ("run_id", "case_id", "subject_id", "started_at", "updated_at"):
        if not isinstance(metadata.get(key), str) or not metadata[key]:
            raise EvalConfigError(f"attempt metadata {key} must be a non-empty string")
    if not isinstance(metadata.get("repeat"), int) or metadata["repeat"] < 1:
        raise EvalConfigError("attempt metadata repeat must be a positive integer")
    for key in ("runner", "execution", "artifacts"):
        if not isinstance(metadata.get(key), dict):
            raise EvalConfigError(f"attempt metadata {key} must be an object")
    inputs = metadata.get("inputs")
    if not isinstance(inputs, dict) or set(inputs) != {
        "case_sha256",
        "fixture_tree",
        "prompt_sha256",
    }:
        raise EvalConfigError("attempt metadata inputs contract is invalid")
    if not isinstance(inputs["fixture_tree"], str) or not HEX_DIGEST_RE.fullmatch(
        inputs["fixture_tree"]
    ):
        raise EvalConfigError("attempt metadata fixture_tree is invalid")
    for key in ("case_sha256", "prompt_sha256"):
        value = inputs[key]
        if not isinstance(value, str) or len(value) != 64 or not HEX_DIGEST_RE.fullmatch(value):
            raise EvalConfigError(f"attempt metadata {key} is invalid")


def execute_codex(
    *,
    codex_path: str,
    workspace: Path,
    prompt: str,
    sandbox: str,
    timeout_seconds: int,
    model: str | None,
    trace_path: Path,
    stderr_path: Path,
) -> dict[str, Any]:
    command = [
        codex_path,
        "exec",
        "--json",
        "--ephemeral",
        "--color",
        "never",
        "--sandbox",
        sandbox,
        "-C",
        str(workspace),
    ]
    if model:
        command.extend(["--model", model])
    command.append(prompt)

    started = time.monotonic()
    timed_out = False
    with trace_path.open("w", encoding="utf-8") as trace_handle, stderr_path.open(
        "w", encoding="utf-8"
    ) as stderr_handle:
        process = subprocess.Popen(
            command,
            cwd=workspace,
            stdout=trace_handle,
            stderr=stderr_handle,
            text=True,
        )
        try:
            return_code = process.wait(timeout=timeout_seconds)
        except KeyboardInterrupt:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)
            raise
        except subprocess.TimeoutExpired:
            timed_out = True
            process.terminate()
            try:
                return_code = process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                return_code = process.wait(timeout=10)
    return {
        "command": command,
        "return_code": return_code,
        "timed_out": timed_out,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def run_attempt(
    *,
    case_dir: Path,
    case: dict[str, Any],
    repeat: int,
    attempt_dir: Path,
    run_id: str,
    subject_id: str,
    model: str | None,
    codex_path: str,
    runner: dict[str, Any],
    inputs: dict[str, str],
    timeout_override: int | None,
    keep_workspace: bool,
) -> dict[str, Any]:
    attempt_dir.mkdir(parents=True, exist_ok=False)
    workspace = attempt_dir / "workspace"
    initialize_fixture(case_dir / "fixture", workspace)
    prompt = (case_dir / str(case["prompt_file"])).read_text(encoding="utf-8").strip()
    atomic_write_text(attempt_dir / "prompt.md", prompt + "\n")
    atomic_write_text(
        attempt_dir / "case.json",
        json.dumps(case, indent=2, ensure_ascii=False) + "\n",
    )

    artifacts = {
        "case": "case.json",
        "prompt": "prompt.md",
        "trace": "trace.jsonl",
        "stderr": "stderr.log",
        "final_output": "final-output.md",
        "diff": "diff.patch",
        "verification": "verification.json",
    }
    metadata: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "state": "running",
        "outcome": "pending",
        "run_id": run_id,
        "case_id": case["case_id"],
        "subject_id": subject_id,
        "repeat": repeat,
        "started_at": utc_now(),
        "updated_at": utc_now(),
        "inputs": inputs,
        "runner": runner,
        "execution": {
            "model": model,
            "sandbox": case["sandbox"],
            "timeout_seconds": timeout_override or case["timeout_seconds"],
            "command": [],
            "return_code": None,
            "timed_out": False,
            "elapsed_seconds": None,
        },
        "artifacts": artifacts,
    }
    validate_attempt_metadata(metadata)
    atomic_write_json(attempt_dir / "metadata.json", metadata)

    execution = execute_codex(
        codex_path=codex_path,
        workspace=workspace,
        prompt=prompt,
        sandbox=str(case["sandbox"]),
        timeout_seconds=timeout_override or int(case["timeout_seconds"]),
        model=model,
        trace_path=attempt_dir / "trace.jsonl",
        stderr_path=attempt_dir / "stderr.log",
    )
    trace_summary = parse_trace(attempt_dir / "trace.jsonl")
    atomic_write_text(attempt_dir / "final-output.md", trace_summary["final_message"] + "\n")

    file_results = evaluate_assertions(case, workspace)
    trace_results = evaluate_trace(case, trace_summary)
    final_changed_files = changed_files(workspace)
    atomic_write_text(attempt_dir / "diff.patch", capture_diff(workspace))
    verification = {
        "schema_version": SCHEMA_VERSION,
        "passed": all(item["passed"] for item in file_results + trace_results),
        "file_assertions": file_results,
        "trace_assertions": trace_results,
        "changed_files": final_changed_files,
        "trace_summary": trace_summary,
    }
    atomic_write_json(attempt_dir / "verification.json", verification)

    if execution["timed_out"]:
        outcome = "timeout"
    elif execution["return_code"] != 0:
        outcome = "error"
    elif verification["passed"]:
        outcome = "pass"
    else:
        outcome = "fail"

    metadata["state"] = "completed"
    metadata["outcome"] = outcome
    metadata["updated_at"] = utc_now()
    metadata["execution"] = {
        "model": model,
        "sandbox": case["sandbox"],
        "timeout_seconds": timeout_override or case["timeout_seconds"],
        **execution,
    }
    validate_attempt_metadata(metadata)
    atomic_write_json(attempt_dir / "metadata.json", metadata)

    if outcome == "pass" and not keep_workspace:
        shutil.rmtree(workspace)
    return metadata


def validate_schema_files(schemas_root: Path) -> None:
    for name in ("case.schema.json", "result.schema.json"):
        schema = read_json(schemas_root / name)
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise EvalConfigError(f"{name}: unexpected JSON Schema dialect")


def selftest(cases_root: Path, schemas_root: Path) -> int:
    validate_schema_files(schemas_root)
    cases = load_cases(cases_root)
    with tempfile.TemporaryDirectory(prefix="softpowers-eval-selftest-") as raw:
        base = Path(raw)
        for case_id, (case_dir, case) in cases.items():
            workspace = base / case_id
            initialize_fixture(case_dir / "fixture", workspace)
            before = evaluate_assertions(case, workspace)
            if all(item["passed"] for item in before):
                raise AssertionError(f"{case_id}: unresolved fixture unexpectedly passed")
            apply_expected(case_dir / "expected", workspace)
            after = evaluate_assertions(case, workspace)
            failed = [item for item in after if not item["passed"]]
            if failed:
                raise AssertionError(f"{case_id}: expected overlay failed assertions: {failed}")

        signed_workspace = base / "signed-fixture"
        with mock.patch.dict(
            os.environ,
            {
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "commit.gpgSign",
                "GIT_CONFIG_VALUE_0": "true",
            },
        ):
            initialize_fixture(cases["tiny-copy"][0] / "fixture", signed_workspace)

        rename_workspace = base / "rename-fixture"
        initialize_fixture(cases["tiny-copy"][0] / "fixture", rename_workspace)
        run_command(
            ["git", "mv", "app.txt", "renamed-app.txt"],
            cwd=rename_workspace,
            check=True,
        )
        if changed_files(rename_workspace) != ["renamed-app.txt"]:
            raise AssertionError("rename status parsing did not preserve the destination path")

        trace_path = base / "trace.jsonl"
        trace_path.write_text(
            "\n".join(
                [
                    json.dumps({"type": "thread.started", "thread_id": "thread-1"}),
                    json.dumps({"type": "turn.started"}),
                    json.dumps(
                        {
                            "type": "item.completed",
                            "item": {
                                "id": "command-1",
                                "type": "command_execution",
                                "command": "sed -n '1,80p' /tmp/references/spec-chain.md",
                            },
                        }
                    ),
                    json.dumps(
                        {
                            "type": "item.completed",
                            "item": {
                                "id": "message-1",
                                "type": "agent_message",
                                "text": "done",
                            },
                        }
                    ),
                    json.dumps({"type": "future.event", "payload": {"kept": True}}),
                    json.dumps(
                        {
                            "type": "turn.completed",
                            "usage": {"input_tokens": 10, "output_tokens": 2},
                        }
                    ),
                ]
            )
            + "\n{malformed-json\n",
            encoding="utf-8",
        )
        summary = parse_trace(trace_path)
        if summary["final_message"] != "done":
            raise AssertionError("trace parser lost the final agent message")
        if summary["reference_reads"] != ["spec-chain.md"]:
            raise AssertionError("trace parser lost a reference read")
        if summary["unknown_event_types"] != ["future.event"]:
            raise AssertionError("trace parser did not preserve an unknown event")
        if summary["malformed_lines"] != 1:
            raise AssertionError("trace parser did not retain malformed-line evidence")
        if summary["command_executions"] != 1 or not summary["turn_completed"]:
            raise AssertionError("trace parser metrics are incorrect")

        now = utc_now()
        sample_metadata: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "state": "completed",
            "outcome": "pass",
            "run_id": "resume-selftest",
            "case_id": "tiny-copy",
            "subject_id": "selftest",
            "repeat": 1,
            "started_at": now,
            "updated_at": now,
            "inputs": {
                "case_sha256": "a" * 64,
                "fixture_tree": "b" * 40,
                "prompt_sha256": "c" * 64,
            },
            "runner": {},
            "execution": {},
            "artifacts": {},
        }
        validate_attempt_metadata(sample_metadata)
        repeat_dir = base / "resume" / "repeat-001"
        incomplete = repeat_dir / "attempt-001"
        complete = repeat_dir / "attempt-002"
        incomplete.mkdir(parents=True)
        complete.mkdir(parents=True)
        running_metadata = dict(sample_metadata)
        running_metadata["state"] = "running"
        running_metadata["outcome"] = "pending"
        atomic_write_json(incomplete / "metadata.json", running_metadata)
        atomic_write_json(complete / "metadata.json", sample_metadata)
        if completed_attempt(repeat_dir) != sample_metadata:
            raise AssertionError("resume selection did not find the completed attempt")
        if next_attempt_dir(repeat_dir).name != "attempt-003":
            raise AssertionError("resume attempt numbering is not monotonic")

        fake_codex = base / "fake-codex"
        fake_codex.write_text(
            """#!/usr/bin/env python3
import json
import sys
from pathlib import Path

if "--version" in sys.argv:
    print("codex-cli fake-selftest")
    raise SystemExit(0)

workspace = Path(sys.argv[sys.argv.index("-C") + 1])
(workspace / "app.txt").write_text("empty_state=No saved items yet\\n", encoding="utf-8")
events = [
    {"type": "thread.started", "thread_id": "fake-thread"},
    {"type": "turn.started"},
    {
        "type": "item.completed",
        "item": {"id": "fake-message", "type": "agent_message", "text": "done"},
    },
    {"type": "turn.completed", "usage": {"input_tokens": 1, "output_tokens": 1}},
]
for event in events:
    print(json.dumps(event), flush=True)
""",
            encoding="utf-8",
        )
        fake_codex.chmod(0o755)
        isolated_cases_root = base / "cases"
        shutil.copytree(cases_root, isolated_cases_root)
        fake_args = argparse.Namespace(
            all=False,
            case=["tiny-copy"],
            repeat=1,
            subject_id="selftest-subject",
            model=None,
            codex_bin="./fake-codex",
            output_root=str(base / "fake-output"),
            run_id="selftest-run",
            resume=False,
            timeout_seconds=30,
            keep_workspace=False,
        )
        with change_directory(base), contextlib.redirect_stdout(io.StringIO()):
            if run_batch(fake_args, isolated_cases_root, schemas_root) != 0:
                raise AssertionError("fake Codex end-to-end run failed")
            fake_args.resume = True
            if run_batch(fake_args, isolated_cases_root, schemas_root) != 0:
                raise AssertionError("completed-attempt resume failed")

            def expect_resume_identity_mismatch(label: str) -> None:
                try:
                    run_batch(fake_args, isolated_cases_root, schemas_root)
                except EvalConfigError as exc:
                    if "resume identity mismatch" not in str(exc):
                        raise AssertionError(f"{label} mismatch failed for the wrong reason") from exc
                else:
                    raise AssertionError(f"resume accepted changed {label}")

            prompt_path = isolated_cases_root / "tiny-copy" / "prompt.md"
            original_prompt = prompt_path.read_text(encoding="utf-8")
            prompt_path.write_text(original_prompt + "\nChanged after interruption.\n", encoding="utf-8")
            expect_resume_identity_mismatch("prompt input")
            prompt_path.write_text(original_prompt, encoding="utf-8")

            fixture_marker = isolated_cases_root / "tiny-copy" / "fixture" / "identity-marker.txt"
            fixture_marker.write_text("changed\n", encoding="utf-8")
            expect_resume_identity_mismatch("fixture input")
            fixture_marker.unlink()

            fake_args.timeout_seconds = 31
            expect_resume_identity_mismatch("timeout configuration")
            fake_args.timeout_seconds = 30

            original_fake_codex = fake_codex.read_text(encoding="utf-8")
            fake_codex.write_text(
                original_fake_codex.replace("fake-selftest", "fake-selftest-updated"),
                encoding="utf-8",
            )
            fake_codex.chmod(0o755)
            expect_resume_identity_mismatch("Codex executable version")
            fake_codex.write_text(original_fake_codex, encoding="utf-8")
            fake_codex.chmod(0o755)

            fake_args.model = "different-model"
            expect_resume_identity_mismatch("model")

    print(
        f"Softpowers eval self-test passed: {len(cases)} cases, known-fail/known-pass "
        "assertions, schemas, Git fixtures, JSONL trace parsing, metadata, fake-Codex "
        "execution, and resume."
    )
    return 0


def codex_identity(codex_path: str) -> str:
    result = run_command([codex_path, "--version"], cwd=Path.cwd(), check=True)
    return result.stdout.strip()


def run_batch(args: argparse.Namespace, cases_root: Path, schemas_root: Path) -> int:
    validate_schema_files(schemas_root)
    cases = load_cases(cases_root)
    if args.all and args.case:
        raise EvalConfigError("use --all or --case, not both")
    if args.all:
        selected = list(cases)
    else:
        selected = list(dict.fromkeys(args.case or []))
    if not selected:
        raise EvalConfigError("select at least one --case or pass --all; live model runs are never implicit")
    unknown = sorted(set(selected) - set(cases))
    if unknown:
        raise EvalConfigError(f"unknown cases: {', '.join(unknown)}")
    if args.repeat < 1:
        raise EvalConfigError("--repeat must be at least 1")
    if args.timeout_seconds is not None and not 30 <= args.timeout_seconds <= 3600:
        raise EvalConfigError("--timeout-seconds must be 30..3600")

    discovered_codex_path = shutil.which(args.codex_bin)
    if not discovered_codex_path:
        raise EvalConfigError(f"Codex CLI not found: {args.codex_bin}")
    codex_path = os.path.abspath(os.path.expanduser(discovered_codex_path))
    codex_version = codex_identity(codex_path)
    run_id = args.run_id or default_run_id()
    if not RUN_ID_RE.fullmatch(run_id):
        raise EvalConfigError(
            "--run-id must be 1..128 characters using letters, digits, dot, underscore, or hyphen"
        )
    if not CASE_ID_RE.fullmatch(args.subject_id):
        raise EvalConfigError("--subject-id must use lowercase letters, digits, and hyphens")
    output_root = (
        Path(args.output_root).expanduser().resolve()
        if args.output_root
        else default_output_root().resolve()
    )
    run_dir = output_root / "runs" / run_id
    if run_dir.exists() and not args.resume:
        raise EvalConfigError(f"run already exists; use --resume or a new --run-id: {run_dir}")
    summary_path = run_dir / "summary.json"
    if args.resume and not summary_path.is_file():
        raise EvalConfigError(f"cannot resume without an existing summary: {summary_path}")

    input_identity = {
        case_id: case_input_identity(cases[case_id][0], cases[case_id][1])
        for case_id in selected
    }
    current_identity = {
        "inputs": input_identity,
        "runner": runner_identity(Path(__file__), codex_version),
        "execution": {
            "codex_path": codex_path,
            "codex_version": codex_version,
            "model": args.model,
            "timeout_override_seconds": args.timeout_seconds,
            "effective_timeout_seconds": {
                case_id: args.timeout_seconds or cases[case_id][1]["timeout_seconds"]
                for case_id in selected
            },
            "keep_workspace": args.keep_workspace,
        },
    }

    batch_summary: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "state": "running",
        "run_id": run_id,
        "subject_id": args.subject_id,
        "model": args.model,
        "cases": selected,
        "repeat": args.repeat,
        "identity": current_identity,
        "started_at": utc_now(),
        "updated_at": utc_now(),
        "attempts": [],
    }
    if args.resume:
        previous = read_json(summary_path)
        identity_fields = {
            "run_id": run_id,
            "subject_id": args.subject_id,
            "model": args.model,
            "cases": selected,
            "repeat": args.repeat,
            "identity": current_identity,
        }
        mismatches = {
            key: {"existing": previous.get(key), "requested": value}
            for key, value in identity_fields.items()
            if previous.get(key) != value
        }
        if mismatches:
            raise EvalConfigError(
                "resume identity mismatch: " + json.dumps(mismatches, ensure_ascii=False)
            )
        batch_summary["started_at"] = previous.get("started_at", batch_summary["started_at"])
    run_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(summary_path, batch_summary)

    try:
        for case_id in selected:
            case_dir, case = cases[case_id]
            for repeat in range(1, args.repeat + 1):
                repeat_dir = run_dir / case_id / args.subject_id / f"repeat-{repeat:03d}"
                if args.resume:
                    prior = completed_attempt(repeat_dir)
                    if prior is not None:
                        batch_summary["attempts"].append(prior)
                        print(
                            f"SKIP {case_id} repeat={repeat} outcome={prior.get('outcome')} "
                            "(completed attempt)"
                        )
                        continue
                attempt_dir = next_attempt_dir(repeat_dir)
                metadata = run_attempt(
                    case_dir=case_dir,
                    case=case,
                    repeat=repeat,
                    attempt_dir=attempt_dir,
                    run_id=run_id,
                    subject_id=args.subject_id,
                    model=args.model,
                    codex_path=codex_path,
                    runner=current_identity["runner"],
                    inputs=input_identity[case_id],
                    timeout_override=args.timeout_seconds,
                    keep_workspace=args.keep_workspace,
                )
                batch_summary["attempts"].append(metadata)
                batch_summary["updated_at"] = utc_now()
                atomic_write_json(summary_path, batch_summary)
                print(
                    f"{metadata['outcome'].upper()} {case_id} repeat={repeat} "
                    f"artifacts={attempt_dir}"
                )
    except KeyboardInterrupt:
        batch_summary["state"] = "interrupted"
        batch_summary["updated_at"] = utc_now()
        atomic_write_json(summary_path, batch_summary)
        print(f"Interrupted; resume with --run-id {run_id} --resume", file=sys.stderr)
        return 130

    batch_summary["state"] = "completed"
    batch_summary["updated_at"] = utc_now()
    atomic_write_json(summary_path, batch_summary)
    outcomes = [str(item.get("outcome")) for item in batch_summary["attempts"]]
    passed = outcomes and all(outcome == "pass" for outcome in outcomes)
    print(f"Run {run_id} completed: {outcomes.count('pass')}/{len(outcomes)} attempts passed.")
    return 0 if passed else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run reproducible Softpowers behavior canaries and save evidence artifacts."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="List available cases without invoking a model")
    subparsers.add_parser("selftest", help="Run deterministic known-fail/known-pass runner tests")

    run = subparsers.add_parser("run", help="Run selected cases through codex exec --json")
    run.add_argument("--case", action="append", help="Case id to run; repeat for multiple cases")
    run.add_argument("--all", action="store_true", help="Run every case")
    run.add_argument("--repeat", type=int, default=1, help="Number of fresh repeats per case")
    run.add_argument(
        "--subject-id",
        default="current-cli-environment",
        help="Exact lowercase identity label for the skills/configuration under test",
    )
    run.add_argument("--model", help="Exact Codex model id; omit only for environment smoke tests")
    run.add_argument("--codex-bin", default="codex", help="Codex CLI executable name or path")
    run.add_argument(
        "--output-root",
        help=(
            "Local artifact root; defaults to source .softpowers-evals or "
            "the installed Codex local-state directory"
        ),
    )
    run.add_argument("--run-id", help="Stable run id for resumption")
    run.add_argument("--resume", action="store_true", help="Resume incomplete case repeats")
    run.add_argument("--timeout-seconds", type=int, help="Override each case timeout")
    run.add_argument(
        "--keep-workspace",
        action="store_true",
        help="Keep passing disposable workspaces; failing workspaces are always preserved",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        cases_root, schemas_root = discover_layout()
        if args.command == "list":
            validate_schema_files(schemas_root)
            cases = load_cases(cases_root)
            for case_id, (_, case) in cases.items():
                print(f"{case_id}\t{case['description']}")
            return 0
        if args.command == "selftest":
            return selftest(cases_root, schemas_root)
        return run_batch(args, cases_root, schemas_root)
    except (EvalConfigError, AssertionError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
