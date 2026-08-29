def match_receipt(receipt: dict, sessions: list[dict]) -> dict | None:
    """Legacy non-batch lookup retained for historical receipts."""
    return next(
        (
            session
            for session in sessions
            if session["turn_index"] == receipt["turn_index"]
        ),
        None,
    )
