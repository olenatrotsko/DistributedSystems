
import logging
import os
import socket
from threading import Thread

from flask import Flask, jsonify

from rpc.server import start_grpc_server
from shared.storage import message_store
from shared.logging_config import setup_logging

setup_logging()

logger = logging.getLogger("flask.server")

app = Flask(__name__)

NODE_ID = os.getenv("NODE_ID", "unknown")


@app.route("/messages", methods=["GET"])
def list_messages():
    messages = message_store.list_messages()
    return jsonify({"list": messages}), 200


def run_grpc():
    server = start_grpc_server(node_id=NODE_ID)
    server.wait_for_termination()


if __name__ == "__main__":
    grpc_thread = Thread(target=run_grpc, daemon=True)
    grpc_thread.start()

    app.run(host="0.0.0.0", port=5000, use_reloader=False, debug=False)
