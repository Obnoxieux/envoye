from dataclasses import dataclass

@dataclass
class Header:
    name: str
    value: str

@dataclass
class Payload:
    headers: list[Header]

@dataclass
class Message:
    id: str
    label_ids: list[str]
    payload: Payload
    snippet: str
    thread_id: str