# service/weather_service.py
from app.external_api.open_weather_api import OpenWeatherApi
from app.local.service.local_service import LocalService
from app.exception.not_found_exception import NotFoundException
from app.weather.dto.response.weather_info_response_dto import WeatherInfoResponseDto
from app.local.dto.response.place_coordinate_response_dto  import PlaceCoordinateResponseDto
from app.weather.dto.response.weather_info_by_address_dto import WeatherInfoByAddressDto

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

    def get_weather_by_coordinate(self, lat: str, lon: str) -> WeatherInfoResponseDto:
        result = self.open_weather_api.get_weather_by_coordinate(lat, lon)
        
        if 'weather' not in result:
            raise NotFoundException(f"올바르지 않은 좌표: 위도 {lat}, 경도 {lon}")
        
        return WeatherInfoResponseDto.from_data(result)
    
    def get_weather_by_address(self, address: str) -> WeatherInfoByAddressDto:
        # LocalService를 사용하여 좌표 정보를 가져옴
        coordinate = self.local_service_api.geocode(address)
        lat = coordinate.lat
        lon = coordinate.lon
        # 날씨 정보 생성
        weather_info = self.get_weather_by_coordinate(lat,lon)
        
        # WeatherInfoByAddressDto 생성 및 반환
        return WeatherInfoByAddressDto(address,coordinate,weather_info)      
