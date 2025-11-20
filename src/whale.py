import random

class WhaleAgent:
    def __init__(self, name, side=None):
        self.name = name
        self.side = side  # optional: force always buy or always sell

    def act(self, orderbook, history):

        list_number = [1,2,3,4,5,6,7,8,9,10]
        #chance of act = 1%
        number = random.randint(1, 100)
        if number not in list_number: #random number, idk
            return

        # If the book is totally empty → nothing to do
        if orderbook.best_bid() is None and orderbook.best_ask() is None:
            print(f"{self.name}: No liquidity, cannot execute market order.")
            return
        # Choose side (fixed or random)
        side = self.side or random.choice(["buy", "sell"])
        # volume = random.randint(1, 5)
        volume = 200

        print(f"{self.name}: MARKET {side.upper()} {volume}")

        # EXECUTE REAL MARKET ORDER
        orderbook.execute_market_order(side, volume)
