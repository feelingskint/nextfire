import unittest

from nextfire.fields import HOUR, MINUTE, MONTH, WEEKDAY, CronSyntaxError, parse, parse_field


class ParseFieldTests(unittest.TestCase):
    def test_star(self):
        self.assertEqual(parse_field("*", HOUR), frozenset(range(24)))

    def test_single_value(self):
        self.assertEqual(parse_field("5", MINUTE), {5})

    def test_list(self):
        self.assertEqual(parse_field("1,2,30", MINUTE), {1, 2, 30})

    def test_star_step(self):
        self.assertEqual(parse_field("*/15", MINUTE), {0, 15, 30, 45})

    def test_range(self):
        self.assertIn(9, parse_field("9-17", HOUR))

    def test_sunday_as_seven(self):
        self.assertEqual(parse_field("7", WEEKDAY), {0})

    def test_month_names(self):
        self.assertEqual(parse_field("jan,MAR", MONTH), {1, 3})

    def test_weekday_names(self):
        self.assertEqual(parse_field("Mon", WEEKDAY), {1})

    def test_out_of_range(self):
        with self.assertRaises(CronSyntaxError):
            parse_field("60", MINUTE)

    def test_backwards_range(self):
        with self.assertRaises(CronSyntaxError):
            parse_field("5-1", MINUTE)


class ParseTests(unittest.TestCase):
    def test_five_fields_required(self):
        with self.assertRaises(CronSyntaxError):
            parse("* * * *")

    def test_alias(self):
        cron = parse("@daily")
        self.assertEqual((cron.minutes, cron.hours), ({0}, {0}))

    def test_unknown_alias(self):
        with self.assertRaises(CronSyntaxError):
            parse("@sometimes")

    def test_star_day_flags(self):
        cron = parse("0 0 * * 1")
        self.assertTrue(cron.any_day)
        self.assertFalse(cron.any_weekday)
