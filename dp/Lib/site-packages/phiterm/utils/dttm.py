import datetime
from typing import Optional


def dttm_str_to_dttm(
    dttm_str: str, dttm_format: Optional[str] = None
) -> Optional[datetime.datetime]:
    """Convert a datestamp string to a Date object"""
    if dttm_str and dttm_str != "":
        dttm_formats = []
        if dttm_format:
            dttm_formats.append(dttm_format)
        else:
            dttm_formats.extend(
                [
                    "%Y-%m-%d",
                    "%Y-%m-%dT%H",
                    "%Y-%m-%d %H",
                    "%Y-%m-%dT%H:%M",
                    "%Y-%m-%d %H:%M",
                ]
            )
        for dttm_format in dttm_formats:
            try:
                datetime_object = datetime.datetime.strptime(dttm_str, dttm_format)
                return datetime_object
            except Exception:
                pass
    return None


def dttm_to_dttm_str(
    dttm: datetime.datetime, dttm_format: str = "%Y-%m-%dT%H:%M:%S"
) -> Optional[str]:
    """Convert a datetime object to formatted string"""

    if dttm and isinstance(dttm, datetime.datetime):
        try:
            dttm_str = datetime.datetime.strftime(dttm, dttm_format)
            return dttm_str
        except Exception as e:
            return None
    else:
        return None


def current_datetime_utc() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def yesterday_datetime() -> datetime.datetime:
    return datetime.datetime.now() - datetime.timedelta(days=1)
