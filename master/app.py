from flask import Flask

from routes import bp as messages_bp


def create_app(master) -> Flask:
    app = Flask(__name__)
    app.extensions["master"] = master
    app.register_blueprint(messages_bp)
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
