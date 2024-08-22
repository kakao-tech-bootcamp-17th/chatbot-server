from flask import Blueprint, request, jsonify
from app.local.api_client import LocalApiClient

local_bp = Blueprint('local', __name__)

class LocalService:
    def __init__(self, api_client=None):
        self.api_client = api_client if api_client else LocalApiClient()

    def get_coordinates(self, location_name):
        return self.api_client.get_coordinates(location_name)

local_service = LocalService()

@local_bp.route("/", methods=['GET'])
def get_coordinates():
    try:
        location_name = request.args.get("location_name")
        if not location_name:
            return jsonify({"error": "location_name parameter is required"}), 400

        lat, lon = local_service.get_coordinates(location_name)
        return jsonify({"latitude": lat, "longitude": lon})

    except ValueError as val_err:
        return jsonify({"error": str(val_err)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
