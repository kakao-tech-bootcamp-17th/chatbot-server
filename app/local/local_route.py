from flask import request
from app.local.local_service import LocalService
from . import local_bp
from app.exception.bad_reqeust_exception import BadRequestException

local_service = LocalService()

@local_bp.route("/", methods=['GET'])
def geocode():
    address = request.args.get("address")
    if not address:
        raise BadRequestException("주소지는 필수 값입니다.")

    return local_service.geocode(address)

@local_bp.route("/test", methods=['GET']) #임시라우트네이밍
def get_weather_by_address():
    address = request.args.get("address")
    if not address:
        raise BadRequestException("주소지는 필수 값입니다.")

    # LocalService에서 새로 추가된 메서드 호출
    return local_service.get_weather_by_address(address)


