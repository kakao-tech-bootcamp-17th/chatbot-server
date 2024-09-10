import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
    KMA_API_KEY = os.getenv("KMA_API_KEY")
    KAKAO_APP_API_KEY = os.getenv("KAKAO_APP_API_KEY")
    TRAFFIC_INFO_API_KEY = os.getenv("TRAFFIC_INFO_API_KEY")
    PUBLIC_TRASPORTION_API_KEY = os.getenv("PUBLIC_TRASPORTION_API_KEY")
    NAVER_DIRECTIONS_API_KEY = os.getenv("NAVER_DIRECTIONS_API_KEY")
    NAVER_DIRECTIONS_CLIENT_ID = os.getenv("NAVER_DIRECTIONS_CLIENT_ID")
    OPEN_AI_API_KEY=os.getenv("OPEN_AI_API_KEY")