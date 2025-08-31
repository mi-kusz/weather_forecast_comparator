from datetime import date
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

from app.analysis.functions import filter_forecasts_by_latitude_and_longitude, filter_forecasts_by_forecast_date, \
    filter_forecasts_by_request_date, group_forecasts, get_comparable_features
from app.storage import load_forecasts_into_dataframe


def compare_forecasts_for_day(dataframe: pd.DataFrame,
                              latitude: float,
                              longitude: float,
                              forecast_date: date,
                              request_date: date,
                              sources: Optional[list[str]] = None,
                              features: Optional[list[str]] = None
                              ) -> None:
    # Use all sources if none is specified
    if sources is None:
        sources = list(dataframe["source"].unique())

    # Use all features if none are specified
    if features is None:
        features = get_comparable_features()

    # Filter by latitude, longitude, forecast_date and request_date
    dataframe = filter_forecasts_by_latitude_and_longitude(dataframe, latitude, longitude)
    dataframe = filter_forecasts_by_forecast_date(dataframe, forecast_date)
    dataframe = filter_forecasts_by_request_date(dataframe, request_date)

    # Group data by source and forecast_datetime
    dataframe = group_forecasts(dataframe, ["source", "forecast_datetime"])
    dataframe = dataframe.reset_index()

    # Drop date from forecast_datetime
    dataframe["forecast_datetime"] = dataframe["forecast_datetime"].dt.strftime("%H:%M")
    dataframe.rename(columns={"forecast_datetime": "forecast_time"}, inplace=True)

    current_feature_index: int = 0

    fig, ax = plt.subplots(figsize=(12, 6))

    def plot_single_feature() -> None:
        ax.clear()
        variable: str = features[current_feature_index]

        pivot_dataframe: pd.DataFrame = dataframe.pivot(
            index="forecast_time",
            columns="source",
            values=variable
        ).sort_index()

        for source in pivot_dataframe.columns:
            ax.plot(
                pivot_dataframe.index,
                pivot_dataframe[source].interpolate(method="linear"),
                label=source
            )

        variable_title: str = variable.replace("_", " ").title()

        ax.set_xlabel("Forecast time [UTC]")
        ax.set_ylabel(variable_title)
        ax.set_title(
            f"{variable_title} forecasts for {forecast_date} from {request_date}"
        )

        ax.legend()
        ax.grid()
        fig.tight_layout()
        fig.canvas.draw_idle()

    def on_key(event):
        nonlocal current_feature_index

        if event.key == "right":
            current_feature_index = (current_feature_index + 1) % len(features)
        elif event.key == "left":
            current_feature_index = (current_feature_index - 1) % len(features)
        else:
            return
        plot_single_feature()

    fig.canvas.mpl_connect("key_press_event", on_key)

    plot_single_feature()

    plt.show()


if __name__ == "__main__":
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 400)

    dataframe: pd.DataFrame = load_forecasts_into_dataframe("../../data/forecasts.csv")
    latitude: float = 52.23
    longitude: float = 21.01
    forecast_date: date = date(2025, 8, 31)
    request_date: date = date(2025, 8, 31)

    compare_forecasts_for_day(dataframe, latitude, longitude, forecast_date, request_date)
