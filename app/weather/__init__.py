from flask import Blueprint

weather_bp = Blueprint('weather', __name__)

from app.weather.route import weather_route