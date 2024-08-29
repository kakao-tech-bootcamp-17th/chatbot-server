import requests
from flask import jsonify
from app.external_api.kakao_local_api import KakaoLocalApi
from app.exception.not_found_exception import NotFoundException
from .dto.place_response_dto import PlacesResponseDTO

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

        if not result['documents']:
            raise NotFoundException(f"{address}는 존재하지 않는 주소지입니다.")
        
        coordinate = { #위치정보를 딕셔너리로 매핑
            "lon": float(result['documents'][0]['x']),
            "lat": float(result['documents'][0]['y'])
        }
    
        return jsonify(coordinate)
    
    def search_places(self, keyword):
        results = self.kakao_local_api.search_places(keyword)

        places = []
        for result in results:
            place = {
                'place_name': result['place_name'],
                'phone': result['phone'],
                'place_url': result['place_url'],
                'distance': result['distance'],
            }
            places.append(place)


        return jsonify(places)

        
        

  