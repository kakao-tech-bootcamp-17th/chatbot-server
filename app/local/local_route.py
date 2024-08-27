from flask import Blueprint, request, jsonify
from app.local.local_service import LocalService
from . import local_bp
from app.exception.bad_reqeust_exception import BadRequestException

local_service = LocalService()

@local_bp.route("/", methods=['GET'])
def get_coordinates():
    address = request.args.get("address")
    if not address:
        raise BadRequestException("주소지는 필수 값입니다.")

    lat, lon = local_service.get_coordinates_info(address)

    return jsonify({"latitude": lat, "longitude": lon})