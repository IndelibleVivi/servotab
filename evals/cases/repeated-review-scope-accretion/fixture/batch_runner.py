from __future__ import annotations


def publish_committed(state: dict, actions) -> None:
    """Publish committed answers and advance their durable local state."""
    for result in state["results"]:
        if result["status"] != "committed":
            continue
        actions.send(result["answer"])
        result["status"] = "published"
