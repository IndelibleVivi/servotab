import unittest
from policy import can_publish

class PolicyTests(unittest.TestCase):
    def test_approved(self):
        self.assertTrue(can_publish(True, False))
    def test_unapproved(self):
        self.assertFalse(can_publish(False, False))
    def test_blocked(self):
        for approved in (True, False):
            with self.subTest(approved=approved):
                self.assertFalse(can_publish(approved, True))
