from flask import request, jsonify
from app.weather.service.weather_service import WeatherService
from .. import weather_bp
from app.exception.bad_reqeust_exception import BadRequestException

weather_service = WeatherService()

@weather_bp.route("/", methods=['GET'])
def get_weather_by_address():
    location = request.args.get("location")
    if not location:
        raise BadRequestException("주소지는 필수 값입니다.")
    response = weather_service.get_weather_by_address(location)
    return jsonify(response)
