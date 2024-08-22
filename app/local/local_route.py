from flask import Blueprint, request, jsonify
from app.local.local_service import LocalService
from . import local_bp

local_service = LocalService()

@local_bp.route("/", methods=['GET'])
def get_coordinates():
    try:
        address = request.args.get("address")
        if not address:
            return jsonify({"error": "address parameter is required"}), 400

        lat, lon = local_service.get_coordinates(address)
        return jsonify({"latitude": lat, "longitude": lon})
    except ValueError as val_err:
        return jsonify({"error": str(val_err)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500