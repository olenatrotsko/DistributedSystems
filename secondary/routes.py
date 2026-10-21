import logging

from flask import Blueprint, current_app, jsonify
from werkzeug.local import LocalProxy

logger = logging.getLogger("flask.server")

bp = Blueprint("messages", __name__, url_prefix="/messages")


node = LocalProxy(lambda: current_app.extensions["node"])

@bp.get("")
def list_messages():
    return jsonify({"list": node.list_messages()}), 200
