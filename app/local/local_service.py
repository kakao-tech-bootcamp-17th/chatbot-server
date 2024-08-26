import requests
from flask import current_app
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
        self.kakao_api_key = current_app.config.get("KAKAO_APP_API_KEY")
        if not self.kakao_api_key:
            raise ValueError("KAKAO_APP_API_KEY is not set in environment variables")

    def get_coordinates(self, address):
        headers = {
            "Authorization": f"KakaoAK {self.kakao_api_key}" #이부분 오타가 있었습니다.
        }
        params = {
            "query": address
        }
    
        response = requests.get(url=KAKAO_LOCAL_REQUEST_URL, headers=headers, params=params)
        response.raise_for_status()

        result = response.json()

        print(result)
        if not result['documents']:
            raise NotFoundException(f"{address}는 존재하지 않는 주소지입니다.")
        
        lon = float(result['documents'][0]['x'])
        lat = float(result['documents'][0]['y'])
    
        return lat, lon
    
    def search_places(self, keyword):
        headers = {
            "Authorization": f"KakaoAK {self.kakao_api_key}" #이부분 오타가 있었습니다.
        }
        params = {
            "query": keyword
        }

        response = requests.get(url=KAKAO_LOCAL_REQUEST_URL, headers=headers, params=params)
        response.raise_for_status()

        results = response.json()['documents']

        place_response_dtos = []
        for result in results:
            place_response_dtos.append(PlacesResponseDTO(result).to_dict())

        return place_response_dtos

        
        

  