class Message:
    def __init__(self, id, label_ids, payload, snippet, thread_id) -> None:
        self.id = id
        self.label_ids = label_ids
        self.payload = payload #TODO: figure out data structure
        self.snippet = snippet
        self.thread_id = thread_id