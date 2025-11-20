class OrderBook:
    def __init__(self):
        self.bids = {}
        self.asks = {}

    def add_order(self, side, price, volume):
        if side == "buy":
            self.bids[price] = self.bids.get(price, 0) + volume
        if side == "sell":
            self.asks[price] = self.asks.get(price, 0) + volume

    def execute_market_order(self, side, volume):
        """
        Executes a true market order.
        - BUY market order consumes from the ASK side.
        - SELL market order consumes from the BID side.
        """
        if side == "buy":
            book = self.asks  # market BUY hits the ask side
            get_best = self.best_ask
            opp_side = "sell"

        elif side == "sell":
            book = self.bids  # market SELL hits the bid side
            get_best = self.best_bid
            opp_side = "buy"

        else:
            return

        remaining = volume

        while remaining > 0:
            best_price = get_best()

            # No liquidity -> stop
            if best_price is None:
                print(f"Market order partially filled. {remaining} volume unfilled.")
                break

            level_volume = book[best_price]

            if remaining >= level_volume:
                # consume entire level
                self.remove_order(opp_side, best_price, level_volume)
                print(f"Market {side.upper()} consumed {level_volume}@{best_price}")
                remaining -= level_volume
            else:
                # consume only part of the level
                self.remove_order(opp_side, best_price, remaining)
                print(f"Market {side.upper()} consumed {remaining}@{best_price}")
                remaining = 0

        # Note: matching is NOT needed because market orders directly remove opposing liquidity.


    def remove_order(self, side, price, volume):
        if side == "buy":
            if self.bids.get(price) == None: #if the level does'nt exist
                print(f"no order found at {price} bid level")
                return
            self.bids[price] -= volume #delete order
            if self.bids[price] <= 0:
                # leftover = abs(self.bids[price])
                del self.bids[price]
                # return leftover #TODO we can directly execute order for the next level

        if side == "sell":
            if self.asks.get(price) == None: #if the level does'nt exist
                print(f"no order found at {price} ask level")
                return
            self.asks[price] -= volume #delete order
            if self.asks[price] <= 0:
                # leftover = abs(self.asks[price])
                del self.asks[price]
                # return leftover #TODO we can directly execute order for the next level
    
    def best_bid(self):
        if not self.bids: #empty
            return None
        return max(self.bids.keys()) 
    
    def best_ask(self):
        if not self.asks: #empty
            return None
        return min(self.asks.keys())

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

    
    def display(self, depth=10):
        print("\n====== ORDER BOOK ======")

        # Sort bids descending, asks ascending
        sorted_bids = sorted(self.bids.items(), key=lambda x: -x[0])
        sorted_asks = sorted(self.asks.items(), key=lambda x: x[0])

        # Limit depth
        sorted_bids = sorted_bids[:depth]
        sorted_asks = sorted_asks[:depth]

        print("  BID_VOL |  BID_PRICE  ||  ASK_PRICE | ASK_VOL")
        print("-----------------------------------------------")

        # Print line by line
        for i in range(max(len(sorted_bids), len(sorted_asks))):
            bid_str = ask_str = ""

            if i < len(sorted_bids):
                bid_price, bid_vol = sorted_bids[i]
                bid_str = f"{str(bid_vol).rjust(8)} | {str(bid_price).rjust(10)}"
            else:
                bid_str = " " * 22

            if i < len(sorted_asks):
                ask_price, ask_vol = sorted_asks[i]
                ask_str = f"{str(ask_price).rjust(10)} | {ask_vol}"
            else:
                ask_str = ""

            print(f"{bid_str}  ||  {ask_str}")
        print("========================\n")





