from flask import Blueprint

chat_ai_bp = Blueprint('chat_ai', __name__)

from . import routes