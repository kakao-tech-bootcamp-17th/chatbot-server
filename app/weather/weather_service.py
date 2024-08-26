import requests
from flask import current_app
from app.exception.not_found_exception import NotFoundException

OPENWEATHER_REQUEST_URL = "https://api.openweathermap.org/data/2.5/weather"

class WeatherService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WeatherService, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.openweather_api_key = current_app.config.get("OPEN_WEATHER_API_KEY") #config로 API키 가져오기
        if not self.openweather_api_key:
            raise ValueError("OPENWEATHER_API_KEY is not set in environment variables")

    def get_weather(self, lat, lon):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.openweather_api_key,
            "units": "metric" #섭씨로 출력
        }
        
        response = requests.get(url=OPENWEATHER_REQUEST_URL, params=params)
        response.raise_for_status()

        result = response.json()

        if 'weather' not in result:
            raise NotFoundException(f"올바르지 않은 좌표: 위도 {lat}, 경도 {lon}")

        return result

