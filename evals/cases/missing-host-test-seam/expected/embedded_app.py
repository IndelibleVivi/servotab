from __future__ import annotations


def choose_export(capabilities: dict[str, object]) -> str:
    """Select the export route exposed by the embedded host."""
    capability = capabilities.get("chat_file")
    if isinstance(capability, dict):
        return "chat-file" if capability.get("state") == "available" else "portable"
    return "chat-file" if capability is True else "portable"
