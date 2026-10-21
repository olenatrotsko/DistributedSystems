import logging

from shared.ack import Ack

logger = logging.getLogger("secondary.node")

class SecondaryNode:
    def __init__(self, storage, node_id):
        self._storage = storage
        self._node_id = node_id

    def list_messages(self) -> list[str]:
        return self._storage.list()

    def receive_message(self, message: str) -> None:
        logger.info(f"Node ({self._node_id}) recieved message: {message}")
        self._storage.append(message)
        return Ack(True)
