import unittest

from filing import archive_clip, undo_archive


class FilingTests(unittest.TestCase):
    def test_one_clip_round_trip(self):
        inbox = [{"id": "a", "text": "A small clipping"}]
        remaining, receipt = archive_clip(inbox, "a")
        self.assertEqual(remaining, [])
        self.assertEqual(undo_archive(remaining, receipt), inbox)


if __name__ == "__main__":
    unittest.main()
