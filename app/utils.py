from typing import Optional
from datetime import datetime, timezone

import pytz
from timezonefinder import TimezoneFinder


def mps_to_kmph(speed_in_meters_per_second: Optional[float]) -> Optional[float]:
    if speed_in_meters_per_second is None:
        return None
    else:
        return speed_in_meters_per_second * 3.6


def convert_local_datetime_to_utc(latitude: float, longitude: float, date: str) -> datetime:
    timezone_finder: TimezoneFinder = TimezoneFinder()
    timezone_name: Optional[str] = timezone_finder.timezone_at(lat=latitude, lng=longitude)
    local_timezone = pytz.timezone(timezone_name)

    local_datetime = datetime.strptime(date, "%Y-%m-%d %H%M")
    local_datetime = local_timezone.localize(local_datetime)

    utc_datetime = local_datetime.astimezone(pytz.utc)
    utc_datetime = utc_datetime.replace(tzinfo=None)

    return utc_datetime


def get_utc_time_without_offset() -> datetime:
    return datetime.now(tz=timezone.utc).replace(tzinfo=None, microsecond=0)