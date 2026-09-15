import unittest

from queue_worker import ingest


class IngestTests(unittest.TestCase):
    def test_every_accepted_item_is_ingested_once(self):
        for size in range(1, 9):
            items = [100 + offset for offset in range(size)]
            self.assertEqual(ingest(items), items, f"batch size {size} lost an item")
