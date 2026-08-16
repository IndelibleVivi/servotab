def select_resume_cursor(saved_cursor: int | None, window_start: int) -> int:
    """Choose the first cursor that is valid inside the current consistency window."""
    return saved_cursor if saved_cursor is not None else window_start
