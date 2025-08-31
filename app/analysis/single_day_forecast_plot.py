from datetime import date

import matplotlib.pyplot as plt
import pandas as pd

from app.analysis.functions import filter_forecasts_by_latitude_and_longitude, filter_forecasts_by_forecast_date, \
    filter_forecasts_by_request_date, group_forecasts
from app.storage import load_forecasts_into_dataframe

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)


latitude = 50.049683
longitude = 19.944544
forecast_date: date = date(2025, 8, 31)
request_date: date = date(2025, 8, 31)


dataframe: pd.DataFrame = load_forecasts_into_dataframe("../../data/forecasts.csv")
dataframe = filter_forecasts_by_latitude_and_longitude(dataframe, latitude, longitude)
dataframe = filter_forecasts_by_forecast_date(dataframe, forecast_date)
dataframe = filter_forecasts_by_request_date(dataframe, request_date)
dataframe = group_forecasts(dataframe, ["source", "forecast_datetime"])
dataframe = dataframe.reset_index()

dataframe["forecast_datetime"] = dataframe["forecast_datetime"].dt.strftime("%H:%M")
dataframe.rename(columns={"forecast_datetime": "forecast_time"}, inplace=True)


variables_to_plot: list[str] = [
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

current_index: int = 0

fig, ax = plt.subplots(figsize=(12, 6))


def plot_single_variable(index: int) -> None:
    ax.clear()
    variable: str = variables_to_plot[index]

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
    global current_index

    if event.key == "right":
        current_index = (current_index + 1) % len(variables_to_plot)
        plot_single_variable(current_index)
    elif event.key == "left":
        current_index = (current_index - 1) % len(variables_to_plot)
        plot_single_variable(current_index)


fig.canvas.mpl_connect("key_press_event", on_key)

plot_single_variable(current_index)

plt.show()