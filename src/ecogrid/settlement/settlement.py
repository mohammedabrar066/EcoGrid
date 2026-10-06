class FinancialSettlement:
    """Financial Settlement bounded context."""

    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.settlements = {}
        self.processed_trade_ids = set()
        self.event_bus.subscribe("TradeCompleted", self.process_trade)

    def process_trade(self, event):
        trade_id = event["trade_id"]
        if trade_id in self.processed_trade_ids:
            return {"status": "ignored", "reason": "duplicate_trade"}
        self.processed_trade_ids.add(trade_id)
        settlement = {
            "trade_id": trade_id,
            "buyer_id": event["buyer_id"],
            "seller_id": event["seller_id"],
            "energy_amount": event["energy_amount"],
            "amount": event["total_amount"],
            "status": "SETTLED",
        }
        self.settlements[trade_id] = settlement
        return settlement

    def get_settlement(self, trade_id):
        return self.settlements.get(trade_id)
