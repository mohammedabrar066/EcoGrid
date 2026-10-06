# EcoGrid Architecture

Three bounded contexts:
1. Smart Meter Integration
2. Marketplace
3. Financial Settlement

Flow:
Smart Meter -> Smart Meter Integration -> Event Bus -> Marketplace -> TradeCompleted -> Financial Settlement

Contexts communicate through events and do not share internal databases.
