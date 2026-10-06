import unittest
from ecogrid.event_bus import EventBus
from ecogrid.smart_meter.smart_meter import SmartMeterIntegration

class TestSmartMeter(unittest.TestCase):
    def test_excess_energy(self):
        meter = SmartMeterIntegration(EventBus())
        result = meter.process_reading("METER-1", 10, 6, "EVENT-1")
        self.assertEqual(result["excess_energy"], 4)

    def test_negative_energy_rejected(self):
        meter = SmartMeterIntegration(EventBus())
        with self.assertRaises(ValueError):
            meter.process_reading("METER-1", -1, 2, "EVENT-2")

if __name__ == "__main__":
    unittest.main()
