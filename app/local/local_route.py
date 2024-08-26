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

    lat, lon = local_service.get_coordinates(address)

    return jsonify({"latitude": lat, "longitude": lon})

@local_bp.route("/places", methods=['GET'])
def search_palces():
    keyword = request.args.get("keyword")
    if not keyword:
        raise BadRequestException("키워드 입력은 필수입니다.")
    
    place_response_dtos = local_service.search_places(keyword)

    return jsonify(place_response_dtos)
    