from app.external_api.naver_directions_api import NaverDirectionsApi
from app.local.service.local_service import LocalService
from app.traffic.dto.response.traffic_info_response_dto import TrafficInfoResponseDto

class TrafficService:
    _instance = None

    def __new__(cls, *args, **kwargs):
            if not cls._instance:
                cls._instance = super(TrafficService, cls).__new__(cls, *args, **kwargs)
            return cls._instance
        
    def __init__(self):
        if not hasattr(self,'naver_directions_api'):
            self.naver_directions_api = NaverDirectionsApi()        
        if not hasattr(self, 'local_service'):
            self.local_service = LocalService()

    def find_direction(self, start_location, goal_location):
        start_pos = self.local_service.geocode(start_location)
        goal_pos = self.local_service.geocode(goal_location)

        result = self.naver_directions_api.fetch_directions(start_pos, goal_pos)

        summary = result['route']['traoptimal'][0]['summary']

        return TrafficInfoResponseDto.from_data(summary, start_location, goal_location)

        

        