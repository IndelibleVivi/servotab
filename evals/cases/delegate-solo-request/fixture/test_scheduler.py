import unittest

from scheduler import next_window


class NextWindowTests(unittest.TestCase):
    def test_window_starting_now_is_not_skipped(self):
        self.assertEqual(next_window(30, [10, 30, 60]), 30)

    def test_next_later_window_is_selected(self):
        self.assertEqual(next_window(31, [10, 30, 60]), 60)
