from datetime import datetime
from typing import Any, Optional

import requests
from requests import Response

from app.model import WeatherForecast
from app.utils import mps_to_kmph


def fetch_wttr_forecast(latitude: float, longitude: float) -> WeatherForecast:
    url: str = f"https://wttr.in/{latitude},{longitude}?format=j1"
    response: Response = requests.get(url)
    response.raise_for_status()

    data: dict[str, str] = response.json()["current_condition"][0]

    weather_forecast: WeatherForecast = WeatherForecast(
        source="wttr",
        forecast_datetime=datetime.now(),
        temperature=float(data["temp_C"]),
        wind_speed=float(data["windspeedKmph"]),
        precipitation=float(data["precipMM"]),
        humidity=float(data["humidity"])
    )

    return weather_forecast


def fetch_open_meteo_forecast(latitude: float, longitude: float) -> WeatherForecast:
    url: str = "https://api.open-meteo.com/v1/forecast"
    parameters: dict[str, Any] = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation,relative_humidity_2m",
        "current_weather": True
    }
    response: Response = requests.get(url, params=parameters)
    response.raise_for_status()

    json_response: Any = response.json()
    data: dict[str, Any] = json_response["current_weather"]

    precipitation: Optional[float] = None
    humidity: Optional[float] = None

    try:
        index: int = int(datetime.now().strftime("%H"))
        precipitation = json_response["hourly"]["precipitation"][index]
        humidity = json_response["hourly"]["relative_humidity_2m"][index]
    except (ValueError, IndexError):
        pass

    weather_forecast: WeatherForecast = WeatherForecast(
        source="open_meteo",
        forecast_datetime=datetime.now(),
        temperature=data["temperature"],
        wind_speed=data["windspeed"],
        precipitation=precipitation,
        humidity=humidity
    )

    return weather_forecast


def fetch_met_forecast(latitude: float, longitude: float) -> WeatherForecast:
    url: str = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
    headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0"
    }
    parameters: dict[str, float] = {
        "lat": latitude,
        "lon": longitude
    }
    response: Response = requests.get(url, headers=headers, params=parameters)
    response.raise_for_status()

    json_response: Any = response.json()["properties"]["timeseries"][0]["data"]

    data: dict[str, Any] = json_response["instant"]["details"]
    precipitation: Optional[float] = None

    try:
        precipitation = json_response["next_1_hours"]["details"]["precipitation_amount"]
    except KeyError:
        pass

    weather_forecast: WeatherForecast = WeatherForecast(
        source="met no",
        forecast_datetime=datetime.now(),
        temperature=data["air_temperature"],
        wind_speed=mps_to_kmph(data["wind_speed"]),
        precipitation=precipitation,
        humidity=data["relative_humidity"]
    )

    return weather_forecast