from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)

KAKAO_LOCAL_SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"
OPENWEATHERMAP_API_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_coordinates(address, kakao_api_key):
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
            return lat, lon
        else:
            raise ValueError(f"No coordinates found for address: {address}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise http_err
    except ValueError as val_err:
        print(f"Value error occurred: {val_err}")
        raise val_err
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise e


def get_weather(lat, lon, openweather_api_key):
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": openweather_api_key,
            "units": "metric"  # 섭씨 온도 사용
        }
        response = requests.get(OPENWEATHERMAP_API_URL, params=params)
        
        if response.status_code != 200:
            response.raise_for_status()  # HTTPError 발생

        return response.json()

    #예외 처리 구문
    except requests.exceptions.HTTPError as http_err:
        raise http_err
    except Exception as e:
        raise e

@app.route("/weather", methods=['GET'])
def getWeather():
    try:
        openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
        
        location_name = request.args.get("location_name", None)
        lat = request.args.get("lat", None)
        lon = request.args.get("lon", None)
        
        if location_name:
            kakao_api_key = os.getenv("KAKAO_APP_API_KEY")
            lat, lon = get_coordinates(location_name, kakao_api_key)
        
        if not lat or not lon:
            return jsonify({"error": "Invalid coordinates or location name provided"}), 400

        weather_info = get_weather(lat, lon, openweather_api_key)
        return jsonify(weather_info)
    
    #예외 처리 구문
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": str(http_err)}), 500
    except ValueError as val_err:
        return jsonify({"error": str(val_err)}), 400
    except Exception as e:
        return jsonify({"error"}), 500

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)
