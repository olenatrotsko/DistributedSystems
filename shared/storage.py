import threading


class MessageStorage:
    def __init__(self):
        self.messages = []
        self.lock = threading.Lock()

    def append_message(self, message: str):
        with self.lock:
            self.messages.append(message)

    def list_messages(self):
        with self.lock:
            return self.messages

message_store = MessageStorage()
