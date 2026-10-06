from ecogrid.event_bus import EventBus
from ecogrid.smart_meter.smart_meter import SmartMeterIntegration
from ecogrid.marketplace.marketplace import Marketplace
from ecogrid.settlement.settlement import FinancialSettlement

def main():
    print("=" * 60)
    print("EcoGrid Energy Trading Platform")
    print("=" * 60)

    bus = EventBus()
    smart_meter = SmartMeterIntegration(bus)
    marketplace = Marketplace(bus)
    settlement = FinancialSettlement(bus)

    event = smart_meter.process_reading(
        "METER-001", 10, 4, "METER-EVENT-001"
    )
    print("\nValidated energy event:", event)

    marketplace.add_requirement("BUYER-001", 5)
    trades = marketplace.match()

    for trade in trades:
        print("\nTrade completed:", trade)
        print("Settlement:", settlement.get_settlement(trade["trade_id"]))

    print("\nEcoGrid processing completed successfully.")

if __name__ == "__main__":
    main()
