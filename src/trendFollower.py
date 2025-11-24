import random

class TrendFollower():
    def __init__(self, name):
        self.name = name

    def act(self, orderbook, history):
        # volume = random.randint(1, 5)
        volume = 5

        # 5 midpoint from the newest - the newest midpoint
        price_difference = history[-5] - history[-1] if len(history) >= 5 else 0 

        buffer = 0.2

        # 0 = downtrend, 1 = uptrend, 2 = sideways
        if abs(price_difference) < buffer:
            current_trend = 2
        elif price_difference < 0:
            current_trend = 0
        elif price_difference > 0:
            current_trend = 1
        else:
            return

        if current_trend == 2: #sideways
            return #do nothing, no trend
        elif current_trend == 0: #downtrend
            orderbook.execute_market_order("sell", volume)
            print(f"{self.name}: MARKET SELL {volume}")
        else: # uptrend
            orderbook.execute_market_order("buy", volume)
            print(f"{self.name}: MARKET BUY {volume}")

        return
