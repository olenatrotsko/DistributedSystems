import logging

from flask import Blueprint, current_app, request, jsonify
from werkzeug.local import LocalProxy

logger = logging.getLogger("flask.server")

bp = Blueprint("messages", __name__, url_prefix="/messages")


master = LocalProxy(lambda: current_app.extensions["master"])

@bp.get("")
def list_messages():
    return jsonify({"list": master.list_messages()}), 200


@bp.post("")
def append_message():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400
    if "message" not in data:
        return jsonify({"error": "message is required"}), 400

    if master.append_message(data["message"]):
        return jsonify({"message": f"Message was appended successfully: {data['message']}"}), 201
    return jsonify({"error": "Communication with one or more nodes failed"}), 502
