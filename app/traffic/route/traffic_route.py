from .. import traffic_bp
from flask import jsonify, request
from app.traffic.service.traffic_service import TrafficService

traffic_service = TrafficService()

@traffic_bp.route("/", methods=['GET'])
def find_direction():
    start_location = request.args.get("start")
    goal_location = request.args.get("goal")

    response = traffic_service.find_direction(start_location, goal_location)

    return jsonify(response)