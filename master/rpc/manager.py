import logging

from .client import GRPCClient

logger = logging.getLogger("rpc.client")


class GRPCClientManager:
    def __init__(self, nodes: dict[str, str]):
        self.clients = {
            node_id: GRPCClient(address)
            for node_id, address in nodes.items()
        }
        logger.info("Establishing connection with:", self.clients)

    def get_client(self, node_id: str) -> GRPCClient:
        return self.clients[node_id]

    def send_message(self, node_id: str, message: str):
        return self.get_client(node_id).send_message(message)

    def close(self):
        for client in self.clients.values():
            client.close()
