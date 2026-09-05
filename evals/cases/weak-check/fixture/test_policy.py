import unittest
from policy import can_publish

class PolicyTests(unittest.TestCase):
    def test_approved(self):
        self.assertTrue(can_publish(True, False))
    def test_unapproved(self):
        self.assertFalse(can_publish(False, False))
