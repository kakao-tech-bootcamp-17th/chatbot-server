import os
import requests

class LocalApiClient:
    def __init__(self):
        self.kakao_api_key = os.getenv("KAKAO_APP_API_KEY")
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
            response = requests.get("https://dapi.kakao.com/v2/local/search/keyword.json", headers=headers, params=params)
            response.raise_for_status()

            result = response.json()
            if result['documents']:
                lon = float(result['documents'][0]['x'])
                lat = float(result['documents'][0]['y'])
                return lat, lon
            else:
                raise ValueError(f"No coordinates found for address: {address}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise
