from pathlib import Path
from typing import Union

import pandas as pd

from app.model import WeatherForecast
from app.utils import float_or_none


def save_forecasts(forecasts: Union[WeatherForecast, list[WeatherForecast]],
                   file_path: str
                   ) -> None:
    if not isinstance(forecasts, list):  # Convert single element to list with one element
        forecasts = [forecasts]

    path: Path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    dataframe: pd.DataFrame = pd.DataFrame([forecast.__dict__ for forecast in forecasts])

    if path.exists():
        dataframe.to_csv(path, mode="a", header=False, index=False)
    else:
        dataframe.to_csv(path, index=False)


def load_forecasts_into_dataframe(file_path: str) -> pd.DataFrame:
    dataframe: pd.DataFrame = pd.read_csv(file_path, parse_dates=["request_datetime", "forecast_datetime"])

    return dataframe


def load_forecasts_into_models(file_path: str) -> list[WeatherForecast]:
    dataframe: pd.DataFrame = load_forecasts_into_dataframe(file_path)

    forecasts: list[WeatherForecast] = [
        WeatherForecast(
            source=row["source"],
            request_datetime=row["request_datetime"].to_pydatetime(),
            forecast_datetime=row["forecast_datetime"].to_pydatetime(),
            latitude=float_or_none(row["latitude"]),
            longitude=float_or_none(row["longitude"]),
            temperature=float_or_none(row["temperature"]),
            wind_speed=float_or_none(row["wind_speed"]),
            wind_direction=float_or_none(row["wind_direction"]),
            precipitation=float_or_none(row["precipitation"]),
            humidity=float_or_none(row["humidity"]),
            cloud_cover=float_or_none(row["cloud_cover"]),
            air_pressure=float_or_none(row["air_pressure"]),
            uv_index=float_or_none(row["uv_index"]),
            dew_point=float_or_none(row["dew_point"]),
            visibility=float_or_none(row["visibility"]),
        )
        for _, row in dataframe.iterrows()
    ]

    return forecasts
