import requests
from flask import current_app

OPENWEATHER_REQUEST_URL = "https://api.openweathermap.org/data/2.5/weather"

class WeatherApi:
    def __init__(self):
        self.api_key = current_app.config.get("OPEN_WEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY is not set in environment variables")

    def fetch_weather_data(self, lat, lon):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"  # 섭씨로 출력
        }
        response = requests.get(url=OPENWEATHER_REQUEST_URL, params=params)
        response.raise_for_status()
        return response.json()
