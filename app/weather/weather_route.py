from flask import Blueprint, request, jsonify
from app.weather.weather_service import WeatherService
import requests
from . import weather_bp

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
