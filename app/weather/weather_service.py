from app.external_api.open_weather_api import OpenWeatherApi
from app.local.service.local_service import LocalService
from app.exception.not_found_exception import NotFoundException

class WeatherService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WeatherService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'OpenWeatherApi'):
            self.open_weather_api = OpenWeatherApi()  #인스턴스변수 스네이크표기법으로 변경
        if not hasattr(self, 'LocalService'):
            self.local_service_api = LocalService()  

    def get_weather_by_coordinate(self, lat, lon):
        result = self.open_weather_api.get_weather_by_coordinate(lat, lon)

        if 'weather' not in result:
            raise NotFoundException(f"올바르지 않은 좌표: 위도 {lat}, 경도 {lon}")
        
        weather = {  # 온도, 날씨, 도시명을 딕셔너리로 매핑
            'temperature': result.get('main', {}).get('temp'),
            'description': result.get('weather', [{}])[0].get('description'),
            'city': result.get('name')
        }
        return weather 
    
    def get_weather_by_address(self, address):
        # LocalService를 사용하여 좌표를 얻음
        coordinates = self.local_service_api.geocode(address)

        # 좌표를 사용하여 날씨 정보를 얻음
        weather_info = self.get_weather_by_coordinate(coordinates["lat"], coordinates["lon"])

        return {
            "address": address,
            "coordinates": coordinates,
            "weather": weather_info
        }
