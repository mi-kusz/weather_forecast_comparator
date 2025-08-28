from datetime import datetime
from typing import Any

import requests
from requests import Response

from app.model import WeatherForecast
from app.utils import mps_to_kmph


def fetch_wttr_forecast(latitude: float, longitude: float) -> list[WeatherForecast]:
    url: str = f"https://wttr.in/{latitude},{longitude}?format=j1&num_of_days=7"
    response: Response = requests.get(url)
    response.raise_for_status()

    days: list = response.json()["weather"]
    request_datetime=datetime.now()

    result: list[WeatherForecast] = []

    for day in days:
        for hour in day["hourly"]:
            forecast_datetime: datetime = datetime.strptime(
                f"{day['date']} {hour['time'].zfill(4)}", "%Y-%m-%d %H%M"
            )

            weather_forecast: WeatherForecast = WeatherForecast(
                source="wttr",
                request_datetime=request_datetime,
                forecast_datetime=forecast_datetime,
                temperature=float(hour["tempC"]),
                wind_speed=float(hour["windspeedKmph"]),
                wind_direction=float(hour["winddirDegree"]),
                precipitation=float(hour["precipMM"]),
                humidity=float(hour["humidity"]),
                air_pressure=float(hour["pressure"])
            )

            result.append(weather_forecast)

    return result


def fetch_open_meteo_forecast(latitude: float, longitude: float) -> list[WeatherForecast]:
    url: str = "https://api.open-meteo.com/v1/forecast"
    parameters: dict[str, Any] = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation,relative_humidity_2m,windspeed_10m,winddirection_10m,cloudcover,surface_pressure,dew_point_2m",
        "forecast_days": 7,
        "timezone": "auto"
    }
    response: Response = requests.get(url, params=parameters)
    response.raise_for_status()

    data: dict[str, Any] = response.json()["hourly"]
    times: dict[str, Any] = data["time"]
    request_datetime = datetime.now()

    result: list[WeatherForecast] = []

    for i, iso_datetime in enumerate(times):
        weather_forecast: WeatherForecast = WeatherForecast(
            source="open_meteo",
            request_datetime=request_datetime,
            forecast_datetime=datetime.fromisoformat(iso_datetime),
            temperature=data["temperature_2m"][i],
            wind_speed=data["windspeed_10m"][i],
            wind_direction=data["winddirection_10m"][i],
            precipitation=data["precipitation"][i],
            humidity=data["relative_humidity_2m"][i],
            cloud_cover=data["cloudcover"][i],
            air_pressure=data["surface_pressure"][i],
            dew_point=data["dew_point_2m"][i]
        )

        result.append(weather_forecast)

    return result


def fetch_met_no_forecast(latitude: float, longitude: float) -> list[WeatherForecast]:
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

    data: list = response.json()["properties"]["timeseries"]
    request_datetime = datetime.now()

    result: list[WeatherForecast] = []

    for entry in data:
        forecast_datetime: datetime = datetime.fromisoformat(entry["time"])
        details = entry["data"]["instant"]["details"]

        precipitation = None
        if "next_1_hours" in entry["data"]:
            precipitation = entry["data"]["next_1_hours"]["details"]["precipitation_amount"]

        weather_forecast: WeatherForecast = WeatherForecast(
            source="met_no",
            request_datetime=request_datetime,
            forecast_datetime=forecast_datetime,
            temperature=details.get("air_temperature"),
            wind_speed=mps_to_kmph(details.get("wind_speed")),
            wind_direction=details.get("wind_from_direction"),
            precipitation=precipitation,
            humidity=details.get("relative_humidity"),
            air_pressure=details.get("air_pressure_at_sea_level"),
            dew_point=details.get("dew_point_temperature"),
            cloud_cover=details.get("cloud_area_fraction"),
            visibility=details.get("visibility")
        )

        result.append(weather_forecast)

    return result
