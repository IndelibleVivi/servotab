import unittest

from cursor_window import select_resume_cursor


class CursorWindowTests(unittest.TestCase):
    def test_missing_cursor_starts_at_current_window(self) -> None:
        self.assertEqual(select_resume_cursor(None, 100), 100)

    def test_cursor_inside_current_window_is_preserved(self) -> None:
        self.assertEqual(select_resume_cursor(140, 100), 140)

    def test_stale_cursor_cannot_cross_window_boundary(self) -> None:
        self.assertEqual(select_resume_cursor(80, 100), 100)


if __name__ == "__main__":
    unittest.main()
