class MarketMaker:
    def __init__(self, name, size=5):
        self.name = name
        self.size = size
        self.last_bid = None
        self.last_ask = None

    def act(self, orderbook):
        best_bid = orderbook.best_bid()
        best_ask = orderbook.best_ask()

        if best_bid is None or best_ask is None:
            return

        # improve the market by 1 tick
        new_bid = best_bid + 1
        new_ask = best_ask - 1

        if new_ask <= new_bid:
            # avoid crossing with itself
            new_ask = new_bid + 1

        # cancel old quotes
        if self.last_bid is not None:
            orderbook.remove_order("buy", self.last_bid, self.size)
        if self.last_ask is not None:
            orderbook.remove_order("sell", self.last_ask, self.size)

        # place improved quotes
        orderbook.add_order("buy", new_bid, self.size)
        orderbook.add_order("sell", new_ask, self.size)

        self.last_bid = new_bid
        self.last_ask = new_ask

        print(f"{self.name}: MM QUOTED {new_bid}/{new_ask}")
