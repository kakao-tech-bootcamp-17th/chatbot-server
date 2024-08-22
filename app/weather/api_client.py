import os
import requests

class WeatherApiClient:
    def __init__(self):
        self.openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.openweather_api_key:
            raise ValueError("OPENWEATHER_API_KEY is not set in environment variables")

    def get_weather(self, lat, lon):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.openweather_api_key,
            "units": "metric"
        }
        try:
            response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise
