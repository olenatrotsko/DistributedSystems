from concurrent.futures import ThreadPoolExecutor
import logging

from flask import Flask, request, jsonify
import grpc

from rpc.manager import GRPCClientManager
from shared.storage import message_store
from shared.logging_config import setup_logging
from proto import communication_pb2

setup_logging()

logger = logging.getLogger("flask.server")

app = Flask(__name__)

NODES = {
    "secondary-1": "secondary-1:50051",
    "secondary-2": "secondary-2:50051",
}

grpc_manager = GRPCClientManager(NODES)


def send_to_node(node, msg):
    try:
        logger.info(f"Sending message to node ({node}): {msg}")
        response = grpc_manager.send_message(node, msg)

        if response.status == communication_pb2.STATUS_SUCCESS:
            logger.info(f"Node ({node}) accepted the message")
        else:
            logger.error(f"Node ({node}) rejected the message: {response.message}")
        return {
            "node": node,
            "status": response.status,
            "message": response.message,
        }
    except grpc.RpcError as exc:
        logger.exception(f"gRPC communication failed with node {node}", )
        return {
            "node": node,
            "status": False,
            "message": exc.details() or str(exc),
        }


@app.route("/messages", methods=["GET"])
def list_messages():
    messages = message_store.list_messages()
    return jsonify({"list": messages}), 200


@app.route("/messages", methods=["POST"])
def append_message():
    data = request.get_json()

    if not data or "msg" not in data:
        return jsonify({"error": "Msg is required"}), 400

    msg = data["msg"]

    message_store.append_message(msg)

    with ThreadPoolExecutor(max_workers=len(NODES) or 1) as executor:
        futures = [
            executor.submit(send_to_node, node, msg)
            for node in NODES
        ]

        results = [future.result() for future in futures]

    if all(result["status"] == communication_pb2.STATUS_SUCCESS for result in results):
        return jsonify({"message": f"Message was appended successfully: {msg}"}), 201

    return jsonify({"error": f"Communication with one or more nodes failed"}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
