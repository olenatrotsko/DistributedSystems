import time

class MockedTransport:
    def __init__(self):
        self._nodes = {}
        self._delays = {}

    def register(self, name, node):
        self._nodes[name] = node

    def set_delay(self, name, seconds):
        self._delays[name] = seconds

    def remove_delay(self, name):
        self._delays.pop(name, None)

    def send(self, name, message):
        time.sleep(self._delays.get(name, 0))
        return self._nodes[name].receive_message(message)
