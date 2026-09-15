import unittest

from reconciler import reconcile


class ReconcileTests(unittest.TestCase):
    def test_delivered_entries_are_not_retried(self):
        self.assertEqual(reconcile(["a", "b"], ["a", "b"]), [])

    def test_only_missing_entries_are_retried(self):
        self.assertEqual(reconcile(["a", "b", "c"], ["a", "c"]), ["b"])
