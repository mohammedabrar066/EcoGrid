class SmartMeterIntegration:
    """Smart Meter Integration bounded context."""

    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.processed_meter_events = set()

    def process_reading(self, meter_id, generated_energy, consumed_energy, event_id):
        if generated_energy < 0:
            raise ValueError("Generated energy cannot be negative")
        if consumed_energy < 0:
            raise ValueError("Consumed energy cannot be negative")
        if event_id in self.processed_meter_events:
            return {"status": "ignored", "reason": "duplicate_meter_event"}

        self.processed_meter_events.add(event_id)
        excess_energy = max(generated_energy - consumed_energy, 0)
        event = {
            "event_id": event_id,
            "event_type": "EnergyAvailable",
            "meter_id": meter_id,
            "generated_energy": generated_energy,
            "consumed_energy": consumed_energy,
            "excess_energy": excess_energy,
        }
        self.event_bus.publish(event)
        return event
