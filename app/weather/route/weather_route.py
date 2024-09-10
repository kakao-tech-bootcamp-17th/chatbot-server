from flask import request, jsonify
from app.weather.service.weather_service import WeatherService
from .. import weather_bp
from app.exception.bad_reqeust_exception import BadRequestException

weather_service = WeatherService()

@weather_bp.route("/coordinate", methods=['GET']) #TODO:임시로 사용하고 추후 제거할것 
def get_weather_by_coordinate():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        raise BadRequestException("위도와 경도는 필수 값입니다.")
    response = weather_service.get_weather_by_coordinate(lat, lon)
    return jsonify(response)

@weather_bp.route("/", methods=['GET'])   #일반적으로 사용될 것
def get_weather_by_address():
    location = request.args.get("location")
    if not location:
        raise BadRequestException("주소지는 필수 값입니다.")
    response = weather_service.get_weather_by_address(location)
    return jsonify(response)
