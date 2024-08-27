from app.external_api.kakao_local_api import KakaoLocalApi
from app.exception.not_found_exception import NotFoundException

class LocalService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LocalService, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self,'KakaoLocalCoordinateApi'):
            self.KakaoLocalCoordinateApi = KakaoLocalApi()

    def get_coordinates_info(self, address):
        result = self.KakaoLocalCoordinateApi.get_coordinates(address)

        if not result['documents']:
            raise NotFoundException(f"{address}는 존재하지 않는 주소지입니다.")
        
        response_data = { #위치정보를 딕셔너리로 매핑
            "lon": float(result['documents'][0]['x']),
            "lat": float(result['documents'][0]['y'])
        }
    
        return response_data
  