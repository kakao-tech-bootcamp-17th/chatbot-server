from flask import Flask, request
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)

KAKAO_LOCAL_SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"
OPENWEATHERMAP_API_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_coordinates(address, kakao_api_key):
    headers = {
        "Authorization": f"KakaoAK {kakao_api_key}"
    }
    params = {
        "query": address
    }
    response = requests.get(KAKAO_LOCAL_SEARCH_URL, headers=headers, params=params)
    

    if response.status_code == 200:
        result = response.json()
        if result['documents']:
            # Kakao API의 'x'는 경도(lon), 'y'는 위도(lat)
            lon = float(result['documents'][0]['x'])
            lat = float(result['documents'][0]['y'])
            print(f"Coordinates for {address}: lon={lon}, lat={lat}")  # 좌표 출력 추가
            return lat, lon  # lat와 lon의 순서를 맞춰서 반환
    else:
        print(f"Failed to get coordinates: {response.status_code} - {response.text}")
    return None, None


def get_weather(lat, lon, openweather_api_key):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": openweather_api_key,
        "units": "metric"  # 섭씨 온도 사용
    }
    response = requests.get(OPENWEATHERMAP_API_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get weather data: {response.status_code} - {response.text}")
        return None

@app.route("/weather", methods=['GET'])
def getWeather():
    try:
        openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
        
        location_name = request.args.get("location_name", None)
        lat = request.args.get("lat", None)
        lon = request.args.get("lon", None)
        
        #키워드로 위치 검색
        if location_name:
            kakao_api_key = os.getenv("KAKAO_APP_API_KEY")
            lat, lon = get_coordinates(location_name, kakao_api_key)
        
        if not lat or not lon:
            return {"error": "Invalid coordinates or location name provided"}, 400

        weather_info = get_weather(lat, lon, openweather_api_key)
        
        if weather_info is None:
            return {"error": "Unable to fetch weather information"}, 500
        
        return weather_info

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": "An internal server error occurred"}, 500

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)
