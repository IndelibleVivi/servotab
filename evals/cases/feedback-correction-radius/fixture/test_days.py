import unittest

from days import audit_day, chart_day, detail_day, share_day


class DayProjectionTests(unittest.TestCase):
    def test_every_user_view_uses_the_exact_minute_offset(self):
        timestamp = "2027-01-01T18:45:00Z"
        for projection in (chart_day, detail_day, share_day):
            with self.subTest(projection=projection.__name__):
                self.assertEqual(projection(timestamp, 330), "2027-01-02")

    def test_negative_offset_can_cross_to_the_previous_day(self):
        timestamp = "2027-01-01T04:15:00Z"
        for projection in (chart_day, detail_day, share_day):
            with self.subTest(projection=projection.__name__):
                self.assertEqual(projection(timestamp, -480), "2026-12-31")

    def test_audit_day_remains_utc(self):
        self.assertEqual(audit_day("2027-01-01T18:45:00Z"), "2027-01-01")

    def test_naive_timestamps_remain_invalid(self):
        for projection, args in (
            (chart_day, ("2027-01-01T18:45:00", 330)),
            (detail_day, ("2027-01-01T18:45:00", 330)),
            (share_day, ("2027-01-01T18:45:00", 330)),
            (audit_day, ("2027-01-01T18:45:00",)),
        ):
            with self.subTest(projection=projection.__name__):
                with self.assertRaises(ValueError):
                    projection(*args)


if __name__ == "__main__":
    unittest.main()
