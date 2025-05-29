import unittest
from datetime import date, datetime, timedelta

from apz_toolkit.dates import (
    add_days_to_date,
    days_ago,
    days_between_dates,
    end_of_day,
    format_date,
    from_timestamp,
    get_current_date,
    get_current_datetime,
    get_day_and_month_name,
    get_weekday,
    is_leap_year,
    parse_date,
    start_of_day,
    subtract_days_from_date,
    to_timestamp,
)


class TestDateFunctions(unittest.TestCase):
    def test_get_current_datetime(self):
        self.assertIsInstance(get_current_datetime(), datetime)

    def test_get_current_date(self):
        self.assertEqual(get_current_date(), date.today())

    def test_format_date(self):
        date_obj = date(2023, 12, 25)
        self.assertEqual(format_date(date_obj), '25-12-2023')
        self.assertEqual(format_date(date_obj, '%Y/%m/%d'), '2023/12/25')

    def test_parse_date(self):
        date_string = '25-12-2023'
        self.assertEqual(parse_date(date_string), datetime(2023, 12, 25))
        self.assertEqual(parse_date(date_string, '%d-%m-%Y'), datetime(2023, 12, 25))

    def test_add_days_to_date(self):
        base_date = date(2023, 12, 25)
        self.assertEqual(add_days_to_date(base_date, 5), base_date + timedelta(days=5))

    def test_subtract_days_from_date(self):
        base_date = date(2023, 12, 25)
        self.assertEqual(subtract_days_from_date(base_date, 5), base_date - timedelta(days=5))

    def test_days_between_dates(self):
        start_date = date(2023, 12, 25)
        end_date = date(2023, 12, 30)
        self.assertEqual(days_between_dates(start_date, end_date), 5)

    def test_is_leap_year(self):
        self.assertTrue(is_leap_year(2020))
        self.assertFalse(is_leap_year(2021))
        self.assertTrue(is_leap_year(2000))
        self.assertFalse(is_leap_year(1900))

    def test_start_of_day(self):
        date_obj = date(2023, 12, 25)
        expected_datetime = datetime(2023, 12, 25, 0, 0, 0)
        self.assertEqual(start_of_day(date_obj), expected_datetime)

    def test_end_of_day(self):
        date_obj = date(2023, 12, 25)
        expected_datetime = datetime(2023, 12, 25, 23, 59, 59, 999999)
        self.assertEqual(end_of_day(date_obj), expected_datetime)

    def test_to_timestamp(self):
        date_obj = datetime(2023, 12, 25, 12, 0, 0)
        expected_timestamp = int(date_obj.timestamp())
        self.assertEqual(to_timestamp(date_obj), expected_timestamp)

    def test_from_timestamp(self):
        timestamp = 1700000000
        self.assertEqual(from_timestamp(timestamp), datetime.fromtimestamp(timestamp))

    def test_days_ago(self):
        today = date.today()
        self.assertEqual(days_ago(5), today - timedelta(days=5))

    def test_get_weekday(self):
        date_obj = date(2023, 12, 25)  # Monday
        self.assertEqual(get_weekday(date_obj), 0)

    def test_get_day_and_month_name(self):
        date_obj = date(2023, 12, 25)  # Monday, December
        self.assertEqual(get_day_and_month_name(date_obj), 'Monday, December')
