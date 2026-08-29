def close_after_send(tab, *, accepted_batch: bool) -> None:
    """Close the tab owned by an accepted batch send."""
    if accepted_batch:
        tab.close()
