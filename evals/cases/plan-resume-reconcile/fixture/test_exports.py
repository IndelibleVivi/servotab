import csv
import io
import json
import subprocess
import sys
import unittest

class ExportTests(unittest.TestCase):
    def run_cli(self, kind):
        return subprocess.check_output([sys.executable, "exporter.py", kind], text=True)
    def test_complete_cli(self):
        data = json.loads(self.run_cli("json"))
        self.assertEqual([r["id"] for r in data], ["a", "b", "c", "d"])
        self.assertEqual(list(csv.DictReader(io.StringIO(self.run_cli("csv")))), data)
        self.assertEqual(self.run_cli("count").strip(), "4")
    def test_empty_and_changed_pages(self):
        import exporter
        old = exporter.fetch_page
        try:
            for pages, expected in [
                ({None: ([], None)}, []),
                ({None: ([{"id": "z", "title": "Z"}], "opaque/end"),
                  "opaque/end": ([{"id": "y", "title": "Y"}], None)}, ["z", "y"]),
            ]:
                exporter.fetch_page = lambda cursor=None: pages[cursor]
                self.assertEqual([r["id"] for r in exporter.collect()], expected)
        finally:
            exporter.fetch_page = old
if __name__ == "__main__":
    unittest.main()
