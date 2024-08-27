from app.external_api.open_weather_api import OpenWeatherApi
from app.exception.not_found_exception import NotFoundException

class WeatherService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WeatherService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'OpenWeatherApi'):
            self.OpenWeatherApi = OpenWeatherApi()

    def get_weather_info(self, lat, lon):
        result = self.OpenWeatherApi.get_weather(lat, lon)

        if 'weather' not in result:
            raise NotFoundException(f"올바르지 않은 좌표: 위도 {lat}, 경도 {lon}")
        return result
