"""Release window scheduler."""


def next_window(now: int, windows: list[int]) -> int:
    """Return the first scheduled window at or after `now`."""
    for window in windows:
        if window >= now:
            return window
    return windows[-1]
