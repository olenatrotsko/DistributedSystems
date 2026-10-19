import threading


class MessageStorage:
    def __init__(self):
        self.messages = []
        self.lock = threading.Lock()

    def append(self, message: str):
        with self.lock:
            self.messages.append(message)

    def list(self):
        with self.lock:
            return self.messages
