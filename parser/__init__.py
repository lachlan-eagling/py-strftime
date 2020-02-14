import re

import datetime


TWO_DIGIT_REGEX = re.compile("(\\d{1,2})\\D")
YEAR_FOUR_DIGIT_REGEX = re.compile("\\d{4}")

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


def parse_date_str(dt: str) -> str:
    """
    Parse a given date string and return the format codes required to format such
    date as a string.
    """
    # Lots of work to do here to get an optimal and efficient solution.
    # I have no doubt there are buckets of edge cases that fail at the moment.

    # Look at replacing this with a bunch of pre-compiled regexes like (\d{1,2}):(\d{1,2}):(\d{1,2})
    # would need to profile this to see performance gain/regression though.
    initial_value = dt
    for long_month in LONG_MONTHS:
        if long_month in dt:
            dt = dt.replace(long_month, "%B")
    for short_month in SHORT_MONTHS:
        if short_month in dt:
            dt = dt.replace(short_month, "%b")
    for long_day in LONG_DAYS:
        if long_day in dt:
            dt = dt.replace(long_day, "%A")
    for short_day in SHORT_DAYS:
        if short_day in dt:
            dt = dt.replace(short_day, "%a")
    for short_month in SHORT_MONTHS:
        if short_month in dt:
            dt = dt.replace(short_month, "%b")
    for ampm in AM_PM:
        if ampm in dt:
            dt = dt.replace(ampm, "%p")
    two_digit_results = TWO_DIGIT_REGEX.findall(dt)
    if len(two_digit_results) == 3:
        if int(two_digit_results[0]) in range(0, 23) and int(two_digit_results[1]) in range(0, 59) and int(two_digit_results[2]) in range(0, 59):
            if int(two_digit_results[0]) in range(13, 23):
                dt = dt.replace(two_digit_results[0], "%H")
            if int(two_digit_results[0]) in range(0, 12):
                dt = dt.replace(two_digit_results[0], "%I")
            dt = dt.replace(two_digit_results[1], "%M")
            dt = dt.replace(two_digit_results[2], "%S")
    if len(two_digit_results) == 2:
        if int(two_digit_results[0]) in range(1, 12) and int(two_digit_results[1]) in range(1, 31):
            dt = dt.replace(two_digit_results[0], "%m")
            dt = dt.replace(two_digit_results[1], "%d")
        if int(two_digit_results[0]) in range(1, 31) and int(two_digit_results[1]) in range(1, 12):
            dt = dt.replace(two_digit_results[0], "%d")
            dt = dt.replace(two_digit_results[1], "%m")
    if len(two_digit_results) == 1:
        if int(two_digit_results[0]) in range(1, 31):
            dt = dt.replace(two_digit_results[0], "%d")

    year_results = YEAR_FOUR_DIGIT_REGEX.findall(dt)
    if len(year_results) == 1:
        dt = dt.replace(year_results[0], "%Y")
    if initial_value == dt:
        return "Enter a valid date."
    return f".strftime('{dt}')"