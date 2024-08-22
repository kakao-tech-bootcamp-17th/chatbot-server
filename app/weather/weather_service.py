from app.weather.api_client import OpenWeatherApiClient


class WeatherService:
    def __init__(self, weather_api_client=None):
        self.weather_api_client = weather_api_client if weather_api_client else OpenWeatherApiClient()

    def get_weather_info(self, lat, lon):
        return self.weather_api_client.get_weather(lat, lon)
