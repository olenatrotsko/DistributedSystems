
import logging

import grpc

from proto import communication_pb2
from proto import communication_pb2_grpc

logger = logging.getLogger(__name__)


class GRPCClient:
    def __init__(self, address: str):
        self.channel = grpc.insecure_channel(address)
        self.stub = communication_pb2_grpc.NodeServiceStub(
            self.channel
        )

    def send_message(self, message: str):
        response = self.stub.SendMessage(
            communication_pb2.MessageRequest(
                message=message,
            ),
            timeout=30,
        )
        return response

    def close(self):
        self.channel.close()
