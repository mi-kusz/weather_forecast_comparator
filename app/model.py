from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class WeatherForecast:
    source: str  # Data source name
    request_datetime: datetime  # Date and time of a request (UTC)
    forecast_datetime: datetime  # Date and time of a forecast (UTC)

    latitude: float  # Latitude of the location
    longitude: float  # Longitude of the location

    temperature: Optional[float] = None  # Air temperature (Celsius)

    wind_speed: Optional[float] = None  # Wind speed (kilometers per hour)
    wind_direction: Optional[float] = None  # Wind direction (degrees, 0=N, 90=E, 180=S, 270=W)

    precipitation: Optional[float] = None  # Precipitation (millimeters)
    humidity: Optional[float] = None  # Humidity (percentage)

    cloud_cover: Optional[float] = None  # Cloud cover (percentage)
    air_pressure: Optional[float] = None  # Air pressure (hPa)
    uv_index: Optional[float] = None  # UV Index (index)
    dew_point: Optional[float] = None  # Dew point (Celsius)
    visibility: Optional[float] = None  # Visibility (meters)
