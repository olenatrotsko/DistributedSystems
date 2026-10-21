from concurrent.futures import ThreadPoolExecutor

class MasterNode:
    def __init__(self, transport, nodes, storage):
        self._transport = transport
        self._nodes = nodes
        self._storage = storage

    def list_messages(self) -> list[str]:
        return self._storage.list()

    def append_message(self, message: str) -> bool:
        self._storage.append(message)

        with ThreadPoolExecutor(max_workers=len(self._nodes)) as executor:
            futures = [
                executor.submit(self._transport.send, node, message)
                for node in self._nodes
            ]

            results = [future.result() for future in futures]

        if all(result.status for result in results):
            return True

        return False
