from flask import request
from app.weather.weather_service import WeatherService
from . import weather_bp
from app.exception.bad_reqeust_exception import BadRequestException

weather_service = WeatherService()

@weather_bp.route("/", methods=['GET'])
def get_weather_by_coordinate():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        raise BadRequestException("위도와 경도는 필수 값입니다.")
    
    return weather_service.get_weather_by_coordinate(lat, lon)

@weather_bp.route("/weather-by-address", methods=['GET']) 
def get_weather_by_address():
    address = request.args.get("address")
    if not address:
        raise BadRequestException("주소지는 필수 값입니다.")
    return weather_service.get_weather_by_address(address)
