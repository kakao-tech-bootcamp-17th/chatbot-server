import requests
from flask import current_app

OPEN_WEATHER_REQUEST_URL = "https://api.openweathermap.org/data/2.5/weather"

class OpenWeatherApi:
    _instance = None

    def __new__(cls,*args,**kwgs):
        if cls._instance is None:
            cls._instance = super(OpenWeatherApi,cls).__new__(cls)
        return cls._instance 

    def __init__(self):
        if not hasattr(self,'api_key'):
            self.open_weather_api_key = current_app.config.get("OPEN_WEATHER_API_KEY")
        if not self.open_weather_api_key:
            raise ValueError("OPEN_WEATHER_API_KEY is not set in environment variables")

    def get_weather_by_coordinate(self, lat, lon):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.open_weather_api_key,
            "units": "metric",  # 섭씨로 출력
        }
        response = requests.get(url=OPEN_WEATHER_REQUEST_URL, params=params)
        response.raise_for_status()
        return response.json()
