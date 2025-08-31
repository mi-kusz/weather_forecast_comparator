import pandas as pd
from datetime import datetime, date

from app.utils import mean_angle


def filter_forecasts_by_latitude_and_longitude(dataframe: pd.DataFrame, latitude: float, longitude: float) -> pd.DataFrame:
    filtered_dataframe: pd.DataFrame = dataframe[
        (dataframe["latitude"] == latitude) &
        (dataframe["longitude"] == longitude)
    ]

    return filtered_dataframe


def filter_forecasts_by_forecast_datetime(dataframe: pd.DataFrame, forecast_datetime: datetime) -> pd.DataFrame:
    filtered_dataframe: pd.DataFrame = dataframe[dataframe["forecast_datetime"] == forecast_datetime]

    return filtered_dataframe


def filter_forecasts_by_forecast_date(dataframe: pd.DataFrame, forecast_date: date) -> pd.DataFrame:
    filtered_dataframe: pd.DataFrame = dataframe[dataframe["forecast_datetime"].dt.date == forecast_date]

    return filtered_dataframe


def filter_forecasts_by_request_date(dataframe: pd.DataFrame, request_date: date) -> pd.DataFrame:
    filtered_dataframe: pd.DataFrame = dataframe[dataframe["request_datetime"].dt.date == request_date]

    return filtered_dataframe


def group_forecasts(dataframe: pd.DataFrame, group_by_columns: list[str]) -> pd.DataFrame:
    grouped_dataframe: pd.DataFrame = dataframe.groupby(group_by_columns).agg({
        "temperature": "mean",
        "wind_speed": "mean",
        "wind_direction": lambda x: mean_angle(x),
        "precipitation": "mean",
        "humidity": "mean",
        "cloud_cover": "mean",
        "air_pressure": "mean",
        "uv_index": "mean",
        "dew_point": "mean",
        "visibility": "mean",
    })

    return grouped_dataframe