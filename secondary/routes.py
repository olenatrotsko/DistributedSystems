import logging
import os

from flask import Flask, jsonify

from rpc.server import start_grpc_server


logger = logging.getLogger("flask.server")

app = Flask(__name__)


def create_app(node) -> Flask:
    app = Flask(__name__)

    @app.get("/messages")
    def list_messages():
        return jsonify({"list": node.list_messages()}), 200

    return app


if __name__ == "__main__":
    from node import SecondaryNode
    from shared.storage import MessageStorage
    from shared.logging_config import setup_logging

    setup_logging()

    node_id = os.getenv("NODE_ID", "unknown")

    storage = MessageStorage()

    node = SecondaryNode(storage, node_id)
    server = start_grpc_server(node_id, node)

    create_app(node).run(host="0.0.0.0", port=5000, use_reloader=False)
