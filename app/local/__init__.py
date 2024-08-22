from flask import Blueprint

local_bp = Blueprint('local', __name__, url_prefix="/local")

from app.local import local_api
