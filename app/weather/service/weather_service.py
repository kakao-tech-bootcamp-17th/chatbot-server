# service/weather_service.py
from app.external_api.open_weather_api import OpenWeatherApi
from app.local.service.local_service import LocalService
from app.exception.not_found_exception import NotFoundException
from app.weather.dto.response.weather_info_response_dto import WeatherInfoResponseDto

class WeatherService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WeatherService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'open_weather_api'):
            self.open_weather_api = OpenWeatherApi()
        if not hasattr(self, 'local_service_api'):
            self.local_service_api = LocalService()

    def fetch_weather(self, lat: str, lon: str):
        result = self.open_weather_api.fetch_weather(lat, lon)

        if 'weather' not in result:
            raise NotFoundException(f"올바르지 않은 좌표: 위도 {lat}, 경도 {lon}")
        
        return result
    
    def get_weather_by_address(self, address: str) -> WeatherInfoResponseDto:
        # LocalService를 사용하여 좌표 정보를 가져옴
        coordinate = self.local_service_api.geocode(address)

        # 날씨 정보 생성
        result = self.fetch_weather(lat=coordinate.lat, lon=coordinate.lon)
    
        # WeatherInfoByAddressDto.from_data()를 사용하여 객체 생성
        return WeatherInfoResponseDto.from_data(address, result)
