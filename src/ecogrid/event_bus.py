class EventBus:
    """Simple in-memory event bus with duplicate-event protection."""

    def __init__(self):
        self.subscribers = {}
        self.processed_events = set()

    def subscribe(self, event_type, handler):
        self.subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event):
        event_id = event.get("event_id")
        if event_id in self.processed_events:
            return {"status": "ignored", "reason": "duplicate_event"}
        self.processed_events.add(event_id)
        for handler in self.subscribers.get(event.get("event_type"), []):
            handler(event)
        return {"status": "processed", "event_id": event_id}
