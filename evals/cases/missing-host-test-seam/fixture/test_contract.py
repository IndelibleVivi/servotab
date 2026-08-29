from __future__ import annotations

import unittest

from embedded_app import choose_export


class ExportContractTest(unittest.TestCase):
    def test_legacy_available_capability(self) -> None:
        self.assertEqual(choose_export({"chat_file": True}), "chat-file")

    def test_legacy_missing_capability(self) -> None:
        self.assertEqual(choose_export({"chat_file": False}), "portable")


if __name__ == "__main__":
    unittest.main()
