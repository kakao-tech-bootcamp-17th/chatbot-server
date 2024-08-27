from app.external_api.kakao_local_coordinate_api import KakaoLocalCoorinateApi
from app.exception.not_found_exception import NotFoundException

KAKAO_LOCAL_REQUEST_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"

class LocalService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LocalService, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self,'KakaoLocalCoordinateApi'):
            self.KakaoLocalCoordinateApi = KakaoLocalCoorinateApi()

    def get_coordinates_info(self, address):
        result = self.KakaoLocalCoordinateApi.get_coordinates(address)

        if not result['documents']:
            raise NotFoundException(f"{address}는 존재하지 않는 주소지입니다.")
        
        lon = float(result['documents'][0]['x'])
        lat = float(result['documents'][0]['y'])
    
        return lat, lon
  