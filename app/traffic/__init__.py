from flask import Blueprint

traffic_bp = Blueprint('traffic', __name__)

from app.traffic.route import traffic_route