import random

class RandomAgent:
    def __init__(self, name):
        self.name = name

    def act(self, orderbook):
        side = random.choice(["buy", "sell"])
        volume = random.randint(1, 5)

        best_bid = orderbook.best_bid()
        best_ask = orderbook.best_ask()

        # If no market exists yet, start one
        if best_bid is None or best_ask is None:
            mid = 100
        else:
            mid = (best_bid + best_ask) // 2

        # random offset around mid price
        offset = random.randint(-5, 5)
        price = mid + offset

        orderbook.add_order(side, price, volume)
        print(f"{self.name}: placed {side} {volume} @ {price}")
