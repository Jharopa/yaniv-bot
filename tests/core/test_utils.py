from datetime import datetime

from yaniv_bot.core.utils import snowflake_to_datetime


def test_snowflake_to_datetime():
    result: list(datetime) = [
        datetime(2015, 9, 9, 17, 35, 13, 0),
        datetime(2016, 1, 11, 2, 16, 53, 0),
        datetime(2017, 2, 3, 0, 13, 57, 0),
        datetime(2015, 9, 9, 18, 7, 1, 0),
    ]

    expected: list(datetime) = [
        snowflake_to_datetime(91224910776528896),
        snowflake_to_datetime(135929899696390144),
        snowflake_to_datetime(276867841540489228),
        snowflake_to_datetime(91232913776988160),
    ]

    assert result == expected
