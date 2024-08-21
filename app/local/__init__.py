from flask import Blueprint

local_bp = Blueprint('local', __name__)

from app.local import local_bp 
