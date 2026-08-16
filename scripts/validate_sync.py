#!/usr/bin/env python3
from __future__ import annotations

from build_skills import check


def main() -> int:
    errors = check()
    if errors:
        print("Softpowers source/generated sync failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Canonical methods, router references, and generated leaves are in sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
