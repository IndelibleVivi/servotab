from __future__ import annotations

import unittest

from embedded_app import choose_export
from host_surrogate import host_capabilities


class HostSurrogateTest(unittest.TestCase):
    def test_available_uses_chat_file(self) -> None:
        self.assertEqual(choose_export(host_capabilities("available")), "chat-file")

    def test_denied_uses_portable(self) -> None:
        self.assertEqual(choose_export(host_capabilities("denied")), "portable")

    def test_missing_uses_portable(self) -> None:
        self.assertEqual(choose_export(host_capabilities("missing")), "portable")


if __name__ == "__main__":
    unittest.main()
