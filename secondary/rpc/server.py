from concurrent import futures
import logging

import grpc

from proto import communication_pb2
from proto import communication_pb2_grpc


logger = logging.getLogger("rpc.server")


class NodeService(communication_pb2_grpc.NodeServiceServicer):
    def __init__(self, node_id, node):
        self.node_id = node_id
        self.node = node

    def SendMessage(self, request, context):
        message = request.message

        try:
            self.node.receive_message(message)
        except Exception as e:
            logger.error(f"Node ({self.node_id}) failed to process the message: {message}. Error: {e}")
            return communication_pb2.MessageResponse(
                message=str(e),
                status=communication_pb2.STATUS_ERROR,
            )

        return communication_pb2.MessageResponse(
            message=message,
            status=communication_pb2.STATUS_SUCCESS,
        )

def start_grpc_server(node_id: str, node, port: int = 50051):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=1)
    )

    communication_pb2_grpc.add_NodeServiceServicer_to_server(
        NodeService(node_id, node),
        server,
    )

    server.add_insecure_port(f"[::]:{port}")

    server.start()

    logger.info(f"gRPC server started on port {port} for node {node_id}")

    return server
