from concurrent.futures import Future, as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Callable

from requests import RequestException

from app.model import WeatherForecast


def fetch_forecasts(latitude: float,
                    longitude: float,
                    fetch_functions: list[Callable[[float, float], list[WeatherForecast]]]
                    ) -> list[WeatherForecast]:
    all_forecasts: list[WeatherForecast] = []

    with ThreadPoolExecutor(max_workers=len(fetch_functions)) as executor:
        futures: list[Future] = [executor.submit(fetch_function, latitude, longitude) for fetch_function in fetch_functions]

        for future in as_completed(futures):
            try:
                hourly_forecasts: list[WeatherForecast] = future.result()
                all_forecasts.extend(hourly_forecasts)
            except RequestException as e:
                print(f"Problem with HTTP request: {e}")
            except (KeyError, TypeError, AttributeError) as e:
                print(f"Problem with received JSON: {e}")
            except IndexError as e:
                print(f"Problem with incomplete data: {e}")

    return all_forecasts