from datetime import date
from itertools import combinations
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

from app.analysis.functions import filter_forecasts_by_forecast_date_range, \
    filter_forecasts_by_latitude_and_longitude, get_group_by_aggregator
from app.storage import load_forecasts_into_dataframe


def compare_forecast_sources(dataframe: pd.DataFrame,
                             latitude: float,
                             longitude: float,
                             date_range_start: date,
                             date_range_end: date,
                             sources_to_compare: Optional[list[str]] = None,
                             features_to_compare: Optional[list[str]] = None
                             ) -> None:
    # Use all sources if none or single is specified
    if sources_to_compare is None or len(sources_to_compare) < 2:
        sources_to_compare = list(dataframe["source"].unique())

    # Use all features if none are specified
    if features_to_compare is None:
        features_to_compare = [
            "temperature",
            "wind_speed",
            "precipitation",
            "humidity",
            "air_pressure",
            "cloud_cover",
            "uv_index",
            "dew_point",
            "visibility"
        ]

    # Filter by latitude, longitude and date range
    dataframe = filter_forecasts_by_latitude_and_longitude(dataframe, latitude, longitude)
    dataframe = filter_forecasts_by_forecast_date_range(dataframe, date_range_start, date_range_end)

    # Drop time from "forecast datetime" field
    dataframe["forecast_datetime"] = dataframe["forecast_datetime"].dt.date
    dataframe.rename(columns={"forecast_datetime": "forecast_date"}, inplace=True)

    # Group data by source and forecast date (calculate means)
    dataframe = dataframe.groupby(["source", "forecast_date"]).agg(get_group_by_aggregator())
    dataframe = dataframe.reset_index()

    pivot_dataframe: pd.DataFrame = dataframe.pivot(index="forecast_date", columns="source", values=features_to_compare).sort_index()

    source_pairs: list[tuple[str, str]] = list(combinations(sources_to_compare, 2))
    current_source_pair_index: int = 0
    current_feature_index: int = 0

    fig, ax = plt.subplots(figsize=(12, 6))

    def plot_feature() -> None:
        ax.clear()
        source_a, source_b = source_pairs[current_source_pair_index]
        feature: str = features_to_compare[current_feature_index]

        for source in (source_a, source_b):
            y = pivot_dataframe[(feature, source)].interpolate(method="linear")
            ax.plot(pivot_dataframe.index, y, label=source)

        feature_title: str = feature.replace("_", " ").title()

        ax.set_xlabel("Forecast date")
        ax.set_ylabel(feature_title)
        ax.set_title(f"{feature_title} comparison: {source_a} vs {source_b}")
        fig.autofmt_xdate(rotation=45)
        ax.legend()
        ax.grid()
        fig.canvas.draw()

    def on_key(event):
        nonlocal current_source_pair_index, current_feature_index

        match event.key:
            case "right":
                current_source_pair_index = (current_source_pair_index + 1) % len(source_pairs)
            case "left":
                current_source_pair_index = (current_source_pair_index - 1) % len(source_pairs)
            case "up":
                current_feature_index = (current_feature_index + 1) % len(features_to_compare)
            case "down":
                current_feature_index = (current_feature_index - 1) % len(features_to_compare)
            case _:
                return

        plot_feature()


    fig.canvas.mpl_connect("key_press_event", on_key)
    plot_feature()
    plt.show()



if __name__ == "__main__":
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 400)

    dataframe: pd.DataFrame = load_forecasts_into_dataframe("../../data/forecasts.csv")
    latitude: float = 52.23
    longitude: float = 21.01
    date_start: date = date(2025, 8, 29)
    date_end: date = date(2025, 9, 1)

    compare_forecast_sources(dataframe, latitude, longitude, date_start, date_end)