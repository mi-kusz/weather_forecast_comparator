from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class WeatherForecast:
    source: str # Data source
    forecast_datetime: datetime # Date and time of request
    temperature: float # Current air temperature (Celsius)
    wind_speed: Optional[float] = None # Current wind speed (kilometers per hour)
    precipitation: Optional[float] = None # Current (or in next hour) precipitation (millimeters)
    humidity: Optional[float] = None # Current humidity (percentage)
