from pathlib import Path
from typing import Union

import pandas as pd
from app.model import WeatherForecast


def save_forecasts(forecasts: Union[WeatherForecast, list[WeatherForecast]],
                  file_path: str = "../data/forecasts.csv"
                  ) -> None:
    if not isinstance(forecasts, list): # Convert single element to list with one element
        forecasts = [forecasts]

    path: Path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    dataframe: pd.DataFrame = pd.DataFrame([forecast.__dict__ for forecast in forecasts])

    if path.exists():
        dataframe.to_csv(path, mode="a", header=False, index=False)
    else:
        dataframe.to_csv(path, index=False)