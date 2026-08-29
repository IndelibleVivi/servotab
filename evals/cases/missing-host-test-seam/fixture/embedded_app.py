from __future__ import annotations


def choose_export(capabilities: dict[str, object]) -> str:
    """Select the export route exposed by the embedded host."""
    return "chat-file" if capabilities.get("chat_file") else "portable"
