import re

import datetime


TWO_DIGIT_REGEX = re.compile("(\\d{1,2})")
YEAR_FOUR_DIGIT_REGEX = re.compile("\\d{4}")
ISO_8601_RE = re.compile("(\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}[+,-]\\d{2}:\\d{2})")

ISO_8601_FORMAT = "%Y-%m-%dT%H:%M:%S%Z"  # 2012-03-29T10:05:45-06:00

SHORT_MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

LONG_MONTHS = [
    "January",
    "February",
    "Marh",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

SHORT_DAYS = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun",
]

LONG_DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

AM_PM = [
    "AM",
    "PM",
]

def check_known_formats(dt: str) -> str:
    iso8601 = ISO_8601_RE.findall(dt)
    if len(iso8601) == 1:
        return ISO_8601_FORMAT
    return None


def parse_date_str(dt: str) -> str:
    """
    Parse a given date string and return the format codes required to format such
    date as a string.
    """
    # Lots of work to do here to get an optimal and efficient solution.
    # I have no doubt there are buckets of edge cases that fail at the moment.

    # Look at replacing this with a bunch of pre-compiled regexes like (\d{1,2}):(\d{1,2}):(\d{1,2})
    # would need to profile this to see performance gain/regression though.

    if (known := check_known_formats(dt)):
        return known

    initial_value = dt

    year_results = YEAR_FOUR_DIGIT_REGEX.findall(dt)
    if len(year_results) == 1:
        dt = dt.replace(year_results[0], "%Y")

    for long_month in LONG_MONTHS:
        insensitive_long_month = re.compile(re.escape(long_month), re.IGNORECASE)
        if re.search(insensitive_long_month, dt):
            dt = insensitive_long_month.sub("%B", dt)
    for short_month in SHORT_MONTHS:
        insensitive_short_month = re.compile(re.escape(short_month), re.IGNORECASE)
        if re.search(insensitive_short_month, dt):
            dt = insensitive_short_month.sub("%b", dt)
    for long_day in LONG_DAYS:
        insensitive_long_day = re.compile(re.escape(long_day), re.IGNORECASE)
        if re.search(insensitive_long_day, dt):
            dt = insensitive_long_day.sub("%A", dt)
    for short_day in SHORT_DAYS:
        insensitive_short_day = re.compile(re.escape(short_day), re.IGNORECASE)
        if re.search(insensitive_short_day, dt):
            dt = insensitive_short_day.sub("%a", dt)
    for ampm in AM_PM:
        if ampm in dt:
            dt = dt.replace(ampm, "%p")

    two_digit_results = TWO_DIGIT_REGEX.findall(dt)
    if len(two_digit_results) == 3:
        if int(two_digit_results[0]) in range(0, 24) and int(two_digit_results[1]) in range(0, 60) and int(two_digit_results[2]) in range(0, 60):
            if int(two_digit_results[0]) in range(13, 24):
                dt = dt.replace(two_digit_results[0], "%H", 1)
            elif int(two_digit_results[0]) in range(1, 13):
                dt = dt.replace(two_digit_results[0], "%I", 1)
            else:
                dt = dt.replace(two_digit_results[0], "%H", 1)
            dt = dt.replace(two_digit_results[1], "%M", 1)
            dt = dt.replace(two_digit_results[2], "%S", 1)
    if len(two_digit_results) == 2:
        if int(two_digit_results[0]) in range(1, 13) and int(two_digit_results[1]) in range(1, 32):
            dt = dt.replace(two_digit_results[0], "%m", 1)
            dt = dt.replace(two_digit_results[1], "%d", 1)
        if int(two_digit_results[0]) in range(1, 32) and int(two_digit_results[1]) in range(1, 13):
            dt = dt.replace(two_digit_results[0], "%d", 1)
            dt = dt.replace(two_digit_results[1], "%m", 1)
    if len(two_digit_results) == 1:
        if int(two_digit_results[0]) in range(1, 32):
            dt = dt.replace(two_digit_results[0], "%d", 1)



    if initial_value == dt:
        return None
    return dt
