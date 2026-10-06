import unittest
from ecogrid.event_bus import EventBus
from ecogrid.marketplace.marketplace import Marketplace

class TestMarketplace(unittest.TestCase):
    def test_matching(self):
        marketplace = Marketplace(EventBus())
        marketplace.add_offer("SELLER-1", 10, 0.20)
        marketplace.add_requirement("BUYER-1", 5)
        trades = marketplace.match()
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0]["energy_amount"], 5)

if __name__ == "__main__":
    unittest.main()
