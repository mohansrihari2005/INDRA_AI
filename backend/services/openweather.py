import requests
import os
from functools import lru_cache
from datetime import datetime

OPENWEATHER_CURRENT = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"

API_KEY = os.getenv("OPENWEATHER_API_KEY", "")


@lru_cache(maxsize=128)
def get_current_weather(place: str):
    """
    Fetch current weather for a place using OpenWeather API.
    Returns dict with wind, rainfall, humidity, pressure, visibility, weather data.
    """
    if not API_KEY:
        return {
            "error": "OPENWEATHER_API_KEY not set",
            "wind_speed_kmh": 0,
            "wind_direction_deg": 0,
            "wind_gust_kmh": 0,
            "rainfall_1h_mm": 0,
            "humidity_pct": 0,
            "pressure_hpa": 0,
            "visibility_m": 0,
            "weather_description": "API key not configured",
            "temperature_c": 0,
            "feels_like_c": 0,
        }

    try:
        params = {"q": place, "appid": API_KEY, "units": "metric"}
        response = requests.get(OPENWEATHER_CURRENT, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        wind = data.get("wind", {})
        wind_speed_ms = wind.get("speed", 0)
        wind_speed_kmh = wind_speed_ms * 3.6

        wind_gust_ms = wind.get("gust", 0)
        wind_gust_kmh = wind_gust_ms * 3.6

        rain = data.get("rain", {})
        rainfall_1h_mm = rain.get("1h", 0)

        main = data.get("main", {})
        weather = data.get("weather", [{}])[0]

        return {
            "wind_speed_kmh": round(wind_speed_kmh, 2),
            "wind_direction_deg": wind.get("deg", 0),
            "wind_gust_kmh": round(wind_gust_kmh, 2),
            "rainfall_1h_mm": rainfall_1h_mm,
            "humidity_pct": main.get("humidity", 0),
            "pressure_hpa": main.get("pressure", 0),
            "visibility_m": data.get("visibility", 0),
            "weather_description": weather.get("description", "unknown"),
            "temperature_c": main.get("temp", 0),
            "feels_like_c": main.get("feels_like", 0),
        }

    except Exception as e:
        return {
            "error": str(e),
            "wind_speed_kmh": 0,
            "wind_direction_deg": 0,
            "wind_gust_kmh": 0,
            "rainfall_1h_mm": 0,
            "humidity_pct": 0,
            "pressure_hpa": 0,
            "visibility_m": 0,
            "weather_description": "Error fetching data",
            "temperature_c": 0,
            "feels_like_c": 0,
        }


def get_forecast(place: str):
    """
    Fetch 3-hour forecast for next 24h for a place.
    Returns list of { timestamp, rainfall_3h_mm, wind_speed_kmh }
    """
    if not API_KEY:
        return []

    try:
        params = {"q": place, "appid": API_KEY, "units": "metric"}
        response = requests.get(OPENWEATHER_FORECAST, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        forecast_list = data.get("list", [])
        result = []

        for i, item in enumerate(forecast_list[:8]):
            wind_speed_ms = item.get("wind", {}).get("speed", 0)
            wind_speed_kmh = wind_speed_ms * 3.6

            rain = item.get("rain", {})
            rainfall_3h_mm = rain.get("3h", 0)

            dt_txt = item.get("dt_txt", "")

            result.append(
                {
                    "timestamp": dt_txt,
                    "rainfall_3h_mm": rainfall_3h_mm,
                    "wind_speed_kmh": round(wind_speed_kmh, 2),
                }
            )

        return result

    except Exception as e:
        print(f"Error fetching forecast: {e}")
        return []
