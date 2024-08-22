from flask import Blueprint, request, jsonify
from app.weather.api_client import WeatherApiClient
import requests

weather_bp = Blueprint('weather', __name__)

class WeatherService:
    def __init__(self, weather_api_client=None):
        self.weather_api_client = weather_api_client if weather_api_client else WeatherApiClient()

    def get_weather_info(self, lat, lon):
        return self.weather_api_client.get_weather(lat, lon)

weather_service = WeatherService()

@weather_bp.route("/", methods=['GET'])
def get_weather():
    try:
        lat = request.args.get("lat")
        lon = request.args.get("lon")

        if not lat or not lon:
            return jsonify({"error": "lat and lon parameters are required"}), 400

        weather_info = weather_service.get_weather_info(lat, lon)
        return jsonify(weather_info)

    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": str(http_err)}), 500
    except ValueError as val_err:
        return jsonify({"error": str(val_err)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
