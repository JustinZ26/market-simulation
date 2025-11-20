import random

#Liquidity Provider
#This agent will place random order around 1% of the current price's midpoint

class RandomAgent:
    def __init__(self, name, trade_side = None):
        self.name = name
        self.trade_side = trade_side

    def act(self, orderbook, history):
        best_bid = orderbook.best_bid()
        best_ask = orderbook.best_ask()

        # If market empty: agent does nothing
        if best_bid is None and best_ask is None:
            return  

        # Pick a side
        side = self.trade_side or random.choice(["buy", "sell"])

        # volume = random.randint(1, 5)
        volume = 1
        
        # If one side missing, make a fallback mid (spread wide)
        if best_bid is None:
            mid = best_ask - (1/100 * best_ask)
        elif best_ask is None:
            mid = best_bid + (1/100 * best_bid)
        else:
            mid = (best_bid + best_ask) / 2 #changed from // to / hopefully this can fix the bias

        # offset = random.randint(1, 5)
        offset = random.uniform(0, mid*1/100) #offset 1 percent of mid value

        if side == "buy":
            price = mid - offset
            # if price >= best_ask:
            #     price = best_ask
        else:  # sell
            price = mid + offset

        if price < 1: #cant place order less than 1
            price = 1

        price = round(price, 2) #take only 2 number after decimal
        orderbook.add_order(side, price, volume)
        print(f"{self.name}: placed {side} {volume} @ {price}")
