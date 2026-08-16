def select_resume_cursor(saved_cursor: int | None, window_start: int) -> int:
    """Choose the first cursor that is valid inside the current consistency window."""
    if saved_cursor is None or saved_cursor < window_start:
        return window_start
    return saved_cursor
