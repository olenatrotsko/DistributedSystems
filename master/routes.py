import logging

from flask import Flask, request, jsonify


logger = logging.getLogger("flask.server")


def create_app(master) -> Flask:
    app = Flask(__name__)

    @app.get("/messages")
    def list_messages():
        return jsonify({"list": master.list_messages()}), 200

    @app.post("/messages")
    def append_message():
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Invalid or missing JSON"}), 400
        if "message" not in data:
            return jsonify({"error": "message is required"}), 400

        if master.append_message(data["message"]):
            return jsonify({"message": f"Message was appended successfully: {data['message']}"}), 201
        return jsonify({"error": "Communication with one or more nodes failed"}), 502

    return app


if __name__ == "__main__":
    from node import MasterNode
    from transport import GrpcTransport
    from rpc.manager import GRPCClientManager
    from shared.storage import MessageStorage
    from shared.logging_config import setup_logging

    setup_logging()

    nodes = {"secondary-1": "secondary-1:50051", "secondary-2": "secondary-2:50051"}

    grpc_client_manager = GRPCClientManager(nodes)
    transport = GrpcTransport(grpc_client_manager)
    storage = MessageStorage()

    master = MasterNode(transport, nodes, storage)

    create_app(master).run(host="0.0.0.0", port=5000, use_reloader=False)
