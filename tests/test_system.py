import unittest
from ecogrid.event_bus import EventBus

class TestEventBus(unittest.TestCase):
    def test_duplicate_event_is_ignored(self):
        bus = EventBus()
        received = []
        bus.subscribe("TestEvent", lambda event: received.append(event))
        event = {"event_id": "EVENT-001", "event_type": "TestEvent"}
        self.assertEqual(bus.publish(event)["status"], "processed")
        self.assertEqual(bus.publish(event)["status"], "ignored")
        self.assertEqual(len(received), 1)

if __name__ == "__main__":
    unittest.main()
