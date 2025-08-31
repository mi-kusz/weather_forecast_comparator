from app.api_clients import fetch_wttr_forecast, fetch_open_meteo_forecast, fetch_met_no_forecast
from app.forecast_service import fetch_forecasts
from app.storage import save_forecasts

latitude = 50.049683
longitude = 19.944544
forecasts = fetch_forecasts(latitude, longitude, [fetch_wttr_forecast, fetch_open_meteo_forecast, fetch_met_no_forecast])
save_forecasts(forecasts, "../data/forecasts.csv")