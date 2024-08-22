import requests
from flask import current_app

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
            "Authorization": f"KakaoAK {self.kakao_api_key}"
        }
        params = {
            "query": address
        }

        try:
            response = requests.get(url=KAKAO_LOCAL_REQUEST_URL, headers=headers, params=params)
            response.raise_for_status()

            result = response.json()

            if not result['documents']:
                raise ValueError(f"No coordinates found for address: {address}")
            
            lon = float(result['documents'][0]['x'])
            lat = float(result['documents'][0]['y'])
        
            return lat, lon
        
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise

