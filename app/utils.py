from typing import Optional


def mps_to_kmph(speed_in_meters_per_second: Optional[float]) -> Optional[float]:
    if speed_in_meters_per_second is None:
        return None
    else:
        return speed_in_meters_per_second * 3.6