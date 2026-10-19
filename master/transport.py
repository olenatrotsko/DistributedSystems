from dataclasses import dataclass
import logging
import grpc
from proto import communication_pb2

logger = logging.getLogger("master.transport")

@dataclass
class Ack:
    status: bool
    message: str = ""


class GrpcTransport:
    def __init__(self, grpc_manager):
        self._grpc = grpc_manager

    def send(self, node, message) -> Ack:
        logger.info(f"Sending message to node ({node}): {message}")
        try:
            response = self._grpc.send_message(node, message)
        except grpc.RpcError as exc:
            reason = exc.details() or str(exc)
            logger.error(f"gRPC communication with node ({node}) failed: {reason}")
            return Ack(False, reason)

        if response.status == communication_pb2.STATUS_SUCCESS:
            logger.info(f"Node ({node}) accepted the message")
            return Ack(True, response.message)

        logger.error(f"Node ({node}) rejected the message: {response.message}")
        return Ack(False, response.message)
