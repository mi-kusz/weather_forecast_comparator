import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

from app.analysis.functions import filter_forecasts_by_latitude_and_longitude
from app.storage import load_forecasts_into_dataframe

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)


latitude = 50.049683
longitude = 19.944544

forecast_year = 2025
forecast_month = 9

dataframe: pd.DataFrame = load_forecasts_into_dataframe("../../data/forecasts.csv")
dataframe = filter_forecasts_by_latitude_and_longitude(dataframe, latitude, longitude)

dataframe["forecast_day"] = dataframe["forecast_datetime"].dt.day

dataframe = dataframe[
    (dataframe["forecast_datetime"].dt.year == forecast_year) &
    (dataframe["forecast_datetime"].dt.month == forecast_month)
]

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

grouped_dataframes: dict[str, pd.DataFrame] = {}
for variable in variables_to_plot:
    dt: pd.DataFrame = dataframe.groupby(["source", "forecast_day"]).agg(
        min_val=(variable, "min"),
        max_val=(variable, "max")
    ).reset_index()

    grouped_dataframes[variable] = dt


current_index: int = 0

fig, ax = plt.subplots(figsize=(12, 6))

plt.subplots_adjust(bottom=0.2)


def plot_single_variable(index: int) -> None:
    ax.clear()
    variable: str = variables_to_plot[index]
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
    global current_index

    if event.key == "right":
        current_index = (current_index + 1) % len(variables_to_plot)
        plot_single_variable(current_index)
        fig.canvas.draw_idle()
    elif event.key == "left":
        current_index = (current_index - 1) % len(variables_to_plot)
        plot_single_variable(current_index)
        fig.canvas.draw_idle()


fig.canvas.mpl_connect("key_press_event", on_key)

plot_single_variable(current_index)

plt.show()
