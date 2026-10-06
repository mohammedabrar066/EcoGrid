import unittest
from ecogrid.event_bus import EventBus
from ecogrid.settlement.settlement import FinancialSettlement

class TestSettlement(unittest.TestCase):
    def test_idempotent_settlement(self):
        settlement = FinancialSettlement(EventBus())
        event = {
            "event_id": "TRADE-1", "event_type": "TradeCompleted",
            "trade_id": "TRADE-1", "buyer_id": "BUYER-1",
            "seller_id": "SELLER-1", "energy_amount": 5,
            "total_amount": 1.0,
        }
        first = settlement.process_trade(event)
        second = settlement.process_trade(event)
        self.assertEqual(first["status"], "SETTLED")
        self.assertEqual(second["status"], "ignored")
        self.assertEqual(len(settlement.settlements), 1)

if __name__ == "__main__":
    unittest.main()
