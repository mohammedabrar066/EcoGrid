class Marketplace:
    """Marketplace bounded context."""

    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.offers = []
        self.requirements = []
        self.trades = []
        self.event_bus.subscribe("EnergyAvailable", self.receive_energy)

    def add_offer(self, seller_id, energy_amount, price_per_unit):
        if energy_amount <= 0:
            raise ValueError("Energy amount must be positive")
        if price_per_unit <= 0:
            raise ValueError("Price must be positive")
        offer = {"seller_id": seller_id, "energy_amount": energy_amount,
                 "price_per_unit": price_per_unit}
        self.offers.append(offer)
        return offer

    def add_requirement(self, buyer_id, energy_amount):
        if energy_amount <= 0:
            raise ValueError("Energy requirement must be positive")
        requirement = {"buyer_id": buyer_id, "energy_amount": energy_amount}
        self.requirements.append(requirement)
        return requirement

    def receive_energy(self, event):
        if event["excess_energy"] > 0:
            self.add_offer(event["meter_id"], event["excess_energy"], 0.20)

    def match(self):
        completed_trades = []
        for offer in self.offers:
            for requirement in self.requirements:
                if offer["energy_amount"] <= 0 or requirement["energy_amount"] <= 0:
                    continue
                matched = min(offer["energy_amount"], requirement["energy_amount"])
                trade = {
                    "trade_id": f"TRADE-{len(self.trades) + 1}",
                    "seller_id": offer["seller_id"],
                    "buyer_id": requirement["buyer_id"],
                    "energy_amount": matched,
                    "price_per_unit": offer["price_per_unit"],
                    "total_amount": matched * offer["price_per_unit"],
                }
                self.trades.append(trade)
                completed_trades.append(trade)
                offer["energy_amount"] -= matched
                requirement["energy_amount"] -= matched
                self.event_bus.publish({
                    "event_id": trade["trade_id"],
                    "event_type": "TradeCompleted",
                    **trade,
                })
        return completed_trades
