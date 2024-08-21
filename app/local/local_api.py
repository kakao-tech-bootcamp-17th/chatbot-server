from flask import Blueprint, jsonify, request
from .local_service import LocalService

local_api = Blueprint('local_api', __name__, url_prefix="/local")

local_service = LocalService()

@local_api.route('/coordinate', methods=['GET'])
def find_coordinate():
    address = request.args.get('address')
    if not address:
        return jsonify({"error": "Address parameter is required"}), 400
    

    data = local_service.find_coordinate(address)

    return jsonify(data)
