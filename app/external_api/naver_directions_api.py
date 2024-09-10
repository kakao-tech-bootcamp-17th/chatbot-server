import requests
from flask import current_app

REQUEST_URL="https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"

from flask import current_app

class NaverDirectionsApi:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NaverDirectionsApi, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self,'api_key'):
            self.naver_api_key = current_app.config.get("NAVER_APP_API_KEY")
        if not hasattr(self, 'client_id'):
            self.naver_client_id = current_app.config.get("NAVER_APP_CLIENT_ID")
        if not self.naver_api_key:
            raise ValueError("NAVER_APP_API_KEY is not set in environment variables")
        
    def directions(self, start, goal, option):
        headers = {
            "X-NCP-APIGW-API-KEY-ID": self.naver_client_id,
            "X-NCP-APIGW-API-KEY": self.naver_api_key
        }

        params = {
            "start": start,
            "goal": goal,
            "option": option
        }

        response = requests.get(url=REQUEST_URL, headers=headers, params=params)

        return response['route'].json()
    