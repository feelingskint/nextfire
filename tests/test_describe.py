import unittest

from nextfire.describe import describe
from nextfire.fields import parse


def d(expr):
    return describe(parse(expr))


class DescribeTests(unittest.TestCase):
    def test_every_minute(self):
        self.assertEqual(d("* * * * *"), "Every minute")

    def test_every_fifteen_minutes(self):
        self.assertEqual(d("*/15 * * * *"), "Every 15 minutes")

    def test_hourly(self):
        self.assertEqual(d("0 * * * *"), "Every hour")

    def test_every_two_hours(self):
        self.assertEqual(d("30 */2 * * *"), "Every 2 hours at minute 30")

    def test_fixed_time(self):
        self.assertEqual(d("30 6 * * *"), "At 06:30")

    def test_named_weekdays(self):
        self.assertEqual(d("0 9 * * mon,wed,fri"), "At 09:00, on Monday, Wednesday and Friday")

    def test_weekend(self):
        self.assertEqual(d("0 10 * * sat,sun"), "At 10:00, on Saturday and Sunday")

    def test_day_and_month(self):
        self.assertEqual(d("0 0 1 jan,jul *"), "At 00:00, on day 1 of the month, in January and July")

    def test_six_times(self):
        self.assertEqual(d("0,30 9,13,17 * * *"), "At 09:00, 09:30, 13:00, 13:30, 17:00 and 17:30")

    def test_many_times(self):
        self.assertEqual(d("0,30 8,12,18,20 * * *"), "At minute 0 and 30 past hour 8, 12, 18 and 20")
