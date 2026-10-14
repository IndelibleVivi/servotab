import unittest

from summaries import card_excerpt, export_text


class SummaryTests(unittest.TestCase):
    def test_card_signals_clipping(self):
        self.assertEqual(card_excerpt("A longer note", 6), "A lon…")

    def test_raw_export_is_exact(self):
        text = "  My note\nNext line  "
        self.assertEqual(export_text(text), text)

    def test_positive_limit(self):
        with self.assertRaises(ValueError):
            card_excerpt("text", 0)


if __name__ == "__main__":
    unittest.main()
