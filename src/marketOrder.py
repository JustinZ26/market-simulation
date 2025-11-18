import random

class MarketOrderAgent:
    def __init__(self, name, side=None):
        self.name = name
        self.side = side  # optional: force always buy or always sell

    def act(self, orderbook):
        # If the book is totally empty → nothing to do
        if orderbook.best_bid() is None and orderbook.best_ask() is None:
            print(f"{self.name}: No liquidity, cannot execute market order.")
            return

        # Choose side (fixed or random)
        side = self.side or random.choice(["buy", "sell"])
        volume = random.randint(1, 5)

        print(f"{self.name}: MARKET {side.upper()} {volume}")

        # EXECUTE REAL MARKET ORDER
        orderbook.execute_market_order(side, volume)
