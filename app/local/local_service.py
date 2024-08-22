from app.local.loacal_api import KakaoLocalApiClient

class LocalService:
    def __init__(self, api_client=None):
        self.api_client = api_client if api_client else KakaoLocalApiClient()

    def get_coordinates(self, location_name):
        return self.api_client.get_coordinates(location_name)
