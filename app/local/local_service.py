from flask import jsonify
from app.external_api.kakao_local_api import KakaoLocalApi
from app.weather.weather_service import WeatherService
from app.exception.not_found_exception import NotFoundException

class LocalService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LocalService, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self,'KakaoLocalApi'):
            self.KakaoLocalApi = KakaoLocalApi()
        if not hasattr(self, 'WeatherService'):
            self.WeatherService = WeatherService()

    def geocode(self, address):
        result = self.KakaoLocalApi.geocode(address)

        if not result['documents']:
            raise NotFoundException(f"{address}는 존재하지 않는 주소지입니다.")
        
        coordinate = { #위치정보를 딕셔너리로 매핑
            "lon": float(result['documents'][0]['x']),
            "lat": float(result['documents'][0]['y'])
        }
    
        return coordinate
    
    def get_weather_by_address(self, address): #임시 함수명 네이밍
        coordinates = self.geocode(address)
        weather_info = self.WeatherService.get_weather(coordinates["lat"], coordinates["lon"])
        return {
            "address": address,
            "coordinates": coordinates,
            "weather": weather_info
        }

  