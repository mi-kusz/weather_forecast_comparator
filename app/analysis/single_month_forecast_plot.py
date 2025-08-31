from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

from app.analysis.functions import filter_forecasts_by_latitude_and_longitude, get_comparable_features
from app.storage import load_forecasts_into_dataframe

def compare_forecasts_for_month(dataframe: pd.DataFrame,
                              latitude: float,
                              longitude: float,
                              forecast_year: int,
                              forecast_month: int,
                              sources: Optional[list[str]] = None,
                              features: Optional[list[str]] = None
                              ) -> None:
    # Use all sources if none is specified
    if sources is None:
        sources = list(dataframe["source"].unique())

    # Use all features if none are specified
    if features is None:
        features = get_comparable_features()

    # Filter by latitude, longitude, year and month
    dataframe = filter_forecasts_by_latitude_and_longitude(dataframe, latitude, longitude)
    dataframe = dataframe[
        (dataframe["forecast_datetime"].dt.year == forecast_year) &
        (dataframe["forecast_datetime"].dt.month == forecast_month)
        ]

    # Add forecast_day column for grouping
    dataframe["forecast_day"] = dataframe["forecast_datetime"].dt.day

    grouped_dataframes: dict[str, pd.DataFrame] = {}
    for feature in features:
        dt: pd.DataFrame = dataframe.groupby(["source", "forecast_day"]).agg(
            min_val=(feature, "min"),
            max_val=(feature, "max")
        ).reset_index()

        grouped_dataframes[feature] = dt

    current_feature_index: int = 0

    fig, ax = plt.subplots(figsize=(12, 6))
    plt.subplots_adjust(bottom=0.2)

    def plot_single_variable() -> None:
        ax.clear()
        variable: str = features[current_feature_index]
        dataframe: pd.DataFrame = grouped_dataframes[variable]

        for source in dataframe["source"].unique():
            source_dataframe: pd.DataFrame = dataframe[dataframe["source"] == source]

            ax.fill_between(
                source_dataframe["forecast_day"],
                source_dataframe["min_val"],
                source_dataframe["max_val"],
                alpha=0.3,
                label=source
            )

        variable_title: str = variable.replace("_", " ").title()

        ax.set_xlabel("Forecast day")
        ax.set_ylabel(f"{variable_title}")
        ax.set_title(f"{variable_title} forecasts for {forecast_year}-{forecast_month:02}")
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.legend()
        ax.grid()


    def on_key(event):
        nonlocal current_feature_index

        if event.key == "right":
            current_feature_index = (current_feature_index + 1) % len(features)
        elif event.key == "left":
            current_feature_index = (current_feature_index - 1) % len(features)

        else:
            return

        plot_single_variable()
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect("key_press_event", on_key)

    plot_single_variable()

    plt.show()


if __name__ == "__main__":
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 400)

    dataframe: pd.DataFrame = load_forecasts_into_dataframe("../../data/forecasts.csv")
    latitude: float = 52.23
    longitude: float = 21.01
    forecast_year: int = 2025
    forecast_month: int = 8

    compare_forecasts_for_month(dataframe, latitude, longitude, forecast_year, forecast_month)