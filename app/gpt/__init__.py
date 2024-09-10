from flask import Blueprint

gpt_bp = Blueprint('gpt', __name__)

from app.gpt import chat_gpt_api