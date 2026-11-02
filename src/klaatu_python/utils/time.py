import datetime
from collections.abc import Iterator
from datetime import date, timedelta
from math import ceil


def date_to_timestamp_ms(date: datetime.date, tzinfo: datetime.tzinfo = datetime.timezone.utc) -> int:
    epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    dt = datetime.datetime(date.year, date.month, date.day, tzinfo=tzinfo)

    return int((dt - epoch).total_seconds() * 1000)


def daterange(start_date: date, end_date: date) -> Iterator[date]:
    """
    Iterates the dates between `start_date` (inclusive) and `end_date`
    (exclusive).
    """
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(days=n)


def round_to_whole_hour(d: datetime.datetime | None = None) -> datetime.datetime:
    d = d or datetime.datetime.now()
    return datetime.datetime(year=d.year, month=d.month, day=d.day, hour=d.hour, tzinfo=d.tzinfo)


def round_up_timedelta(td: timedelta) -> timedelta:
    """
    If td > 30 min, round up to nearest hour. Otherwise, to nearest 10
    minute mark. Could be extended for higher time units, but nevermind now.
    """
    td_minutes = td.total_seconds() / 60
    if td_minutes > 30:
        return timedelta(hours=ceil(td_minutes / 60))
    if td_minutes >= 10:
        return timedelta(minutes=int(td_minutes / 10) * 10 + 10)
    return timedelta(minutes=10)
