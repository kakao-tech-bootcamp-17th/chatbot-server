from typing import List
import requests
from flask import jsonify
from app.external_api.kakao_local_api import KakaoLocalApi
from app.exception.not_found_exception import NotFoundException
from ..dto.response.place_coordinate_response_dto import ExtPlaceCoordinateResponseDto
from ..dto.response.place_info_response_dto import PlaceInfoResponseDto

class LocalService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LocalService, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self,'kakao_local_api'):
            self.kakao_local_api = KakaoLocalApi()

    def geocode(self, location):
        result = self.kakao_local_api.geocode(location)

        if not result:
            raise NotFoundException(f"{location}는 존재하지 않는 장소입니다.")
    
        return {'lon': result['x'], 'lat': result['y']}
    
    def search_places(self, keyword) -> List[PlaceInfoResponseDto]:
        results = self.kakao_local_api.search_places(keyword)

        return [PlaceInfoResponseDto.from_data(result) for result in results]
        
    def search_restaurants(self, keyword) -> List[PlaceInfoResponseDto]:
        results = self.kakao_local_api.search_restaurants(keyword)

        return [PlaceInfoResponseDto.from_data(result) for result in results]

  