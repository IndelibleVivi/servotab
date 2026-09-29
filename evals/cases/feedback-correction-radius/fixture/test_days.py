import unittest

from days import audit_day, chart_day


class DayProjectionTests(unittest.TestCase):
    def test_chart_uses_the_supplied_offset_around_midnight(self):
        self.assertEqual(chart_day("2027-01-01T18:45:00Z", 330), "2027-01-02")

    def test_audit_day_remains_utc(self):
        self.assertEqual(audit_day("2027-01-01T18:45:00Z"), "2027-01-01")

    def test_naive_timestamps_remain_invalid(self):
        for projection, args in (
            (chart_day, ("2027-01-01T18:45:00", 330)),
            (audit_day, ("2027-01-01T18:45:00",)),
        ):
            with self.subTest(projection=projection.__name__):
                with self.assertRaises(ValueError):
                    projection(*args)


if __name__ == "__main__":
    unittest.main()
