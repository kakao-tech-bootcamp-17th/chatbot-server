import requests
from flask import current_app

REQUEST_URL="https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"

from flask import current_app


"""
    네이버 지도 API를 사용하여 주행 경로를 가져오는 클래스입니다.
    API 문서: [네이버 지도 API 문서](https://api.ncloud-docs.com/docs/ai-naver-mapsdirections-driving#%EC%9D%91%EB%8B%B5-%EB%B0%94%EB%94%94)
    Attributes:
        naver_api_key (str): 네이버 지도 API 키입니다.
        naver_client_id (str): 네이버 지도 클라이언트 ID입니다.
    Methods:
        fetch_directions(start_pos, goal_pos): 시작 위치와 목표 위치를 기반으로 주행 경로를 가져옵니다.
"""

class NaverDirectionsApi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NaverDirectionsApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self,'api_key'):
            self.naver_api_key = current_app.config.get("NAVER_DIRECTIONS_API_KEY")
        if not hasattr(self, 'client_id'):
            self.naver_client_id = current_app.config.get("NAVER_DIRECTIONS_CLIENT_ID")
        if not self.naver_api_key:
            raise ValueError("NAVER_APP_API_KEY is not set in environment variables")
        if not self.naver_client_id:
            raise ValueError("NAVER_APP_CLIENT_ID is not set in environment variables")
        
    def fetch_directions(self, start_pos, goal_pos):
        headers = {
            "X-NCP-APIGW-API-KEY-ID": self.naver_client_id,
            "X-NCP-APIGW-API-KEY": self.naver_api_key
        }
    

        params = {
            "start": start_pos.get("lon") + "," + start_pos.get("lat"),
            "goal": goal_pos.get("lon") + "," + goal_pos.get("lat")
        }

        response = requests.get(url=REQUEST_URL, headers=headers, params=params)

        return response.json()
    