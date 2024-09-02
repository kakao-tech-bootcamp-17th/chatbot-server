import requests
from flask import current_app
from app.exception.not_found_exception import NotFoundException

KAKAO_LOCAL_KEYWORD_URL = "https://dapi.kakao.com/v2/local/search/keyword.json" #키워드검색 URL

class KakaoLocalApi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(KakaoLocalApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self,'api_key'):
            self.kakao_api_key = current_app.config.get("KAKAO_APP_API_KEY")
        if not self.kakao_api_key:
            raise ValueError("KAKAO_APP_API_KEY is not set in environment variables")
        
    def geocode(self, location): #좌표변환
        headers = {
            "Authorization": f"KakaoAK {self.kakao_api_key}"
        }
        params = {
            "query": location,
            "size": 1,
        }
        response = requests.get(url=KAKAO_LOCAL_KEYWORD_URL, headers=headers, params=params)
        response.raise_for_status()    

        print(response.json())
        
        return response.json()['documents'][0]
    
    def search_places(self, keyword):
        headers = {
            "Authorization": f"KakaoAK {self.kakao_api_key}"
        }

        params = {
            "query": keyword,
        }

        response = requests.get(url=KAKAO_LOCAL_KEYWORD_URL, headers=headers, params=params)
        response.raise_for_status()

        return response.json()['documents']