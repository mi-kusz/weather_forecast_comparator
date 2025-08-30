from typing import Optional, Any
from datetime import datetime, timezone

import pandas as pd
import pytz
from timezonefinder import TimezoneFinder

import numpy as np


def mps_to_kmph(speed_in_meters_per_second: Optional[float]) -> Optional[float]:
    if speed_in_meters_per_second is None:
        return None
    else:
        return speed_in_meters_per_second * 3.6


def km_to_m(distance_in_kilometers: float) -> float:
    return 1000 * distance_in_kilometers


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


def mean_angle(angles: list[float]) -> float:
    angles = [a for a in angles if pd.notna(a)]

    if len(angles) == 0:
        return float('nan')

    angles_rad = np.deg2rad(angles)
    mean_sin = np.mean(np.sin(angles_rad))
    mean_cos = np.mean(np.cos(angles_rad))

    mean_angle_rad = np.arctan2(mean_sin, mean_cos)
    mean_angle_deg = float(np.rad2deg(mean_angle_rad)) % 360

    if mean_angle_deg >= 360:
        mean_angle_deg = 0.0

    return mean_angle_deg


def float_or_none(value: Any) -> Optional[Any]:
    if isinstance(value, float) and np.isnan(value):
        return None
    else:
        return float(value)