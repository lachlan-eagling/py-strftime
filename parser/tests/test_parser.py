from unittest import TestCase

from parser import parse_date_str

class TestParser(TestCase):
    def setUp(self, *args, **kwargs):
        return super().setUp(*args, **kwargs)

    def test_parser__ddmmyyyy_slash_delim(self):
        input_format = "21/01/2020"
        result = parse_date_str(input_format)
        self.assertEqual("%d/%m/%Y", result)

    def test_parser__mmddyyyy_slash_delim(self):
        input_format = "01/21/2020"
        result = parse_date_str(input_format)
        self.assertEqual("%m/%d/%Y", result)

    def test_parser__ddShortMonthyyyy_space_delim(self):
        input_format = "21 Feb 2020"
        result = parse_date_str(input_format)
        self.assertEqual("%d %b %Y", result)

    def test_parser__ddShortMoNtHyyyy_space_delim(self):
        input_format = "21 FeB 2020"
        result = parse_date_str(input_format)
        self.assertEqual("%d %b %Y", result)

    def test_parser__ddLongMonthyyyy_space_delim(self):
        input_format = "21 February 2020"
        result = parse_date_str(input_format)
        self.assertEqual("%d %B %Y", result)

    def test_parser__ddLongMoNtHyyyy_space_delim(self):
        input_format = "21 FeBrUaRy 2020"
        result = parse_date_str(input_format)
        self.assertEqual("%d %B %Y", result)

    def test_parser__shortDayddthLongMonthYYYY(self):
        input_format = "Mon 9th January 2020"
        result = parse_date_str(input_format)
        self.assertEqual("%a %dth %B %Y", result)

    def test_parser__shortDayddthShortMonthYYYY(self):
        input_format = "Mon 9th Jan 2020"
        result = parse_date_str(input_format)
        self.assertEqual("%a %dth %b %Y", result)

    def test_parser__shortDayddthShortMONTHYYYY(self):
        input_format = "Mon 9th JAN 2020"
        result = parse_date_str(input_format)
        self.assertEqual("%a %dth %b %Y", result)

    def test_parser__shortDAYddthShortMONTHYYYY(self):
        input_format = "MON 9th JAN 2020"
        result = parse_date_str(input_format)
        self.assertEqual("%a %dth %b %Y", result)

    def test_parser__hhmmsspm_colon_delim(self):
        input_format = "10:11:23 PM"
        result = parse_date_str(input_format)
        self.assertEqual("%I:%M:%S %p", result)

    def test_parser__hhmmsspm_colon_delim_24hr(self):
        input_format = "19:11:23 PM"
        result = parse_date_str(input_format)
        self.assertEqual("%H:%M:%S %p", result)

    def test_parser__iso8601(self):
        input_format = "2020-02-23T18:47:17+11:00"
        result = parse_date_str(input_format)
        self.assertEqual("%Y-%m-%dT%H:%M:%S%Z", result)

    def test_parser__YYYY_dash_mm_dash_dd(self):
        input_format = "2020-02-21"
        result = parse_date_str(input_format)
        self.assertEqual("%Y-%m-%d", result)
