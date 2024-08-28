from flask import Blueprint, request, jsonify
from app.local.local_service import LocalService
from . import local_bp
from app.exception.bad_reqeust_exception import BadRequestException

local_service = LocalService()

@local_bp.route("/", methods=['GET'])
def get_coordinate():
    address = request.args.get("address")
    if not address:
        raise BadRequestException("주소지는 필수 값입니다.")

    coordinate = local_service.get_coordinate(address)

    return jsonify(coordinate) #임시 JSON 반환