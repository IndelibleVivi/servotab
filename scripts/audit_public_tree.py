#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


SECRET_PATTERNS = (
    ("AWS access key", re.compile(rb"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(rb"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("OpenAI-style secret key", re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b")),
    (
        "private key header",
        re.compile(rb"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    ),
    (
        "credential assignment",
        re.compile(
            rb"(?i)\b(?:password|passwd|api[_-]?key|access[_-]?token)\s*[:=]\s*"
            rb"[\"']?[A-Za-z0-9_./+=-]{12,}"
        ),
    ),
)

LOCAL_PATH_MARKERS = (
    ("macOS user path", b"/" + b"Users/"),
    ("Unix home path", b"/ho" + b"me/"),
    ("Windows user path", b"C:\\" + b"Users\\"),
)


def candidate_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git ls-files failed: {message}")
    return sorted(
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    )


def forbidden_path_reason(relative: str) -> str | None:
    path = PurePosixPath(relative)
    parts = path.parts
    name = path.name

    if parts and parts[0] in {"notes", ".local"}:
        return f"private namespace {parts[0]}/"
    if any(part in {"__pycache__", ".venv", ".pytest_cache"} for part in parts):
        return "generated local directory"
    if name == ".DS_Store" or name.startswith("._"):
        return "macOS metadata"
    if name == ".env" or (name.startswith(".env.") and name != ".env.example"):
        return "environment file"
    if name.endswith(".private.md"):
        return "private-markdown convention"
    return None


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    issues: list[tuple[str, str]] = []

    try:
        files = candidate_files(root)
    except Exception as exc:
        print(f"Public-tree audit failed closed: {exc}", file=sys.stderr)
        return 1

    for relative in files:
        reason = forbidden_path_reason(relative)
        if reason:
            issues.append((relative, reason))
            continue

        path = root / relative
        if path.is_symlink():
            issues.append((relative, "tracked or candidate symlink"))
            continue
        if not path.is_file():
            issues.append((relative, "candidate path is not a regular file"))
            continue

        data = path.read_bytes()
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(data):
                issues.append((relative, label))
        if b"\0" not in data:
            for label, marker in LOCAL_PATH_MARKERS:
                if marker in data:
                    issues.append((relative, label))

    if issues:
        print("Public-tree audit failed:", file=sys.stderr)
        for relative, reason in sorted(set(issues)):
            print(f"- {relative}: {reason}", file=sys.stderr)
        return 1

    print(
        "Public-tree audit passed: "
        f"{len(files)} tracked/candidate files; no forbidden private namespaces, "
        "symlinks, local paths, secret patterns, environment files, or macOS junk."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
