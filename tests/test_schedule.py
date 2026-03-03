import unittest
from datetime import datetime

from nextfire.fields import parse
from nextfire.schedule import next_runs

START = datetime(2026, 3, 4, 10, 7)  # a Wednesday


class NextRunsTests(unittest.TestCase):
    def test_every_minute(self):
        runs = next_runs(parse("* * * * *"), START, 3)
        self.assertEqual(runs, [datetime(2026, 3, 4, 10, m) for m in (8, 9, 10)])

    def test_start_is_exclusive(self):
        self.assertEqual(next_runs(parse("7 10 * * *"), START, 1), [datetime(2026, 3, 5, 10, 7)])

    def test_daily_rolls_over(self):
        runs = next_runs(parse("30 6 * * *"), START, 2)
        self.assertEqual(runs, [datetime(2026, 3, 5, 6, 30), datetime(2026, 3, 6, 6, 30)])

    def test_weekdays_only(self):
        friday_noon = datetime(2026, 3, 6, 12, 0)
        runs = next_runs(parse("0 9 * * 1-5"), friday_noon, 2)
        self.assertEqual(runs, [datetime(2026, 3, 9, 9, 0), datetime(2026, 3, 10, 9, 0)])

    def test_month_boundary(self):
        runs = next_runs(parse("0 0 1 * *"), START, 2)
        self.assertEqual(runs, [datetime(2026, 4, 1), datetime(2026, 5, 1)])

    def test_leap_day(self):
        self.assertEqual(next_runs(parse("0 12 29 2 *"), START, 1), [datetime(2028, 2, 29, 12, 0)])

    def test_never(self):
        with self.assertRaises(ValueError):
            next_runs(parse("0 0 30 2 *"), START, 1)
