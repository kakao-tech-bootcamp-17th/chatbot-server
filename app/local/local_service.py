from flask import current_app
import requests

KAKAO_LOCAL_SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"

class LocalService:
    def __init__(self):
        pass
        
    def find_coordinate(self, address):
        kakao_api_key = current_app.config.get("KAKAO_APP_API_KEY")
        if kakao_api_key is None:
            return "KAKAO_APP_API_KEY not found", 500
        
        try:
            headers = {
                "Authorization": f"KakaoAK {kakao_api_key}"
            }
            params = {
                "query": address
            }
            response = requests.get(KAKAO_LOCAL_SEARCH_URL, headers=headers, params=params)
            response.raise_for_status()  # 상태 코드가 200이 아닌 경우 HTTPError 발생

            result = response.json()
            if result['documents']:
                lon = float(result['documents'][0]['x'])
                lat = float(result['documents'][0]['y'])
                return {"latitude": lat, "longitude": lon}  # JSON 형식으로 반환
            else:
                raise ValueError(f"No coordinates found for address: {address}")

        except requests.exceptions.HTTPError as http_err:
            raise http_err
        except ValueError as val_err:
            raise val_err
        except Exception as e:
            raise e
