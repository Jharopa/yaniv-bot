from datetime import datetime


def snowflake_to_datetime(snowflake) -> datetime:
    return datetime.utcfromtimestamp(int(((snowflake >> 22) + 1420070400000) / 1000))
