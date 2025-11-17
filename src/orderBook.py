class OrderBook:
    def __init__(self):
        self.bids = {}
        self.asks = {}

    def add_order(self, side, price, volume):
        if side == "buy":
            self.bids[price] = self.bids.get(price, 0) + volume
        if side == "sell":
            self.asks[price] = self.asks.get(price, 0) + volume

    def remove_order(self, side, price, volume):
        if side == "buy":
            if self.bids.get(price) == None: #if the level does'nt exist
                print(f"no order found at {price} bid level")
                return
            self.bids[price] -= volume #delete order
            if self.bids[price] <= 0:
                leftover = abs(self.bids[price])
                del self.bids[price]
                # return leftover #TODO we can directly execute order for the next level

        if side == "sell":
            if self.asks.get(price) == None: #if the level does'nt exist
                print(f"no order found at {price} ask level")
                return
            self.asks[price] -= volume #delete order
            if self.asks[price] <= 0:
                leftover = abs(self.asks[price])
                del self.asks[price]
                # return leftover #TODO we can directly execute order for the next level
    
    def best_bid(self):
        if len(self.bids) == 0: #empty
            return
        return max(self.bids.keys()) #return highest bid
    
    def best_ask(self):
        if len(self.asks) == 0: #empty
            return
        return min(self.asks.keys()) #return lowest ask

    def match(self):
        while True:
            bid_price = self.best_bid()
            ask_price = self.best_ask()

            if bid_price is None or ask_price is None or bid_price < ask_price:
                break #no match because no buyer / no seller / no deal

            bid_volume = self.bids[bid_price]
            ask_volume = self.asks[ask_price]

            trade_volume = min(bid_volume, ask_volume) #get the minimum volume to execute the order

            #remove order from both ask and bid orderbook
            self.remove_order("buy", bid_price, trade_volume)
            self.remove_order("sell", ask_price, trade_volume)

            print(f"executed trade at {ask_price} with {trade_volume} volumes.")




