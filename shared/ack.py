from dataclasses import dataclass


@dataclass
class Ack:
    status: bool
    message: str = ""
