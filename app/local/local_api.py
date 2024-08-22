from flask import Blueprint, jsonify, request
from .local_service import LocalService
from . import local_bp

local_service = LocalService()

@local_bp.route('/coordinate', methods=['GET'])
def find_coordinate():
    address = request.args.get('address')
    if not address:
        return jsonify({"error": "Address parameter is required"}), 400
    

    data = local_service.find_coordinate(address)

    return jsonify(data)