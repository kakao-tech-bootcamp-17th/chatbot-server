from flask import request, jsonify
from app.local.service.local_service import LocalService
from .. import local_bp
from app.exception.bad_reqeust_exception import BadRequestException

local_service = LocalService()

@local_bp.route("/", methods=['GET'])
def geocode():
    address = request.args.get("address")
    if not address:
        raise BadRequestException("주소지는 필수 값입니다.")

    response = local_service.geocode(address)

    return jsonify(response)

@local_bp.route("/places", methods=['GET'])
def search_places():
    keyword = request.args.get("keyword")
    if not keyword:
        raise BadRequestException("키워드 입력은 필수입니다.")
    
    response = local_service.search_places(keyword)

    return jsonify(response)
    