from typing import List
import requests
from flask import jsonify
from app.external_api.kakao_local_api import KakaoLocalApi
from app.exception.not_found_exception import NotFoundException
from ..dto.response.place_coordinate_response_dto import PlaceCoordinateResponseDto
from ..dto.response.place_info_response_dto import PlaceInfoResponseDto

KAKAO_LOCAL_REQUEST_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"

class LocalService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LocalService, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self,'kakao_local_api'):
            self.kakao_local_api = KakaoLocalApi()

    def geocode(self, address):
        result = self.kakao_local_api.geocode(address)
        print(result)

        if not result:
            raise NotFoundException(f"{address}는 존재하지 않는 주소지입니다.")
    
        return PlaceCoordinateResponseDto.from_data(result)
    
    def search_places(self, keyword) -> List[PlaceInfoResponseDto]:
        results = self.kakao_local_api.search_places(keyword)

        return [PlaceInfoResponseDto.from_data(result) for result in results]
        
        

  