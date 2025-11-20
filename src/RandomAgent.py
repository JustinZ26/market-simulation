import random

class RandomAgent:
    def __init__(self, name, trade_side = None):
        self.name = name
        self.trade_side = trade_side

    def act(self, orderbook):
        best_bid = orderbook.best_bid()
        best_ask = orderbook.best_ask()

        # If market empty: agent does nothing
        if best_bid is None and best_ask is None:
            return  

        # Pick a side
        side = self.trade_side or random.choice(["buy", "sell"])

        volume = random.randint(1, 5)
        
        # If one side missing, make a fallback mid (spread wide)
        if best_bid is None:
            mid = best_ask - 1
        elif best_ask is None:
            mid = best_bid + 1
        else:
            mid = (best_bid + best_ask) // 2

        offset = random.randint(1, 5)

        if side == "buy":
            price = mid - offset
            # if price >= best_ask:
            #     price = best_ask
        else:  # sell
            price = mid + offset

        if price < 1: #cant place order less than 1
            price = 1

        orderbook.add_order(side, price, volume)
        print(f"{self.name}: placed {side} {volume} @ {price}")
