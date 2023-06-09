from dataclasses import dataclass

@dataclass
class Message:
    id: str
    label_ids: list[str]
    payload: list #TODO: figure out data structure
    snippet: str
    thread_id: str