from __future__ import annotations


def host_capabilities(state: str) -> dict[str, object]:
    """Return the observable capability envelope used by the embedded app."""
    if state == "missing":
        return {}
    return {"chat_file": {"state": state}}
