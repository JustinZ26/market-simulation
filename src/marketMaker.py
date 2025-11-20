import random

class MarketMaker:
    def __init__(
        self,
        name,
        fair_value=100,     # MM's internal "fundamental" reference price
        base_spread=2,      # minimum spread in ticks (integer)
        size=5,             # quote size per side
        max_inventory=50,   # inventory capacity (for risk control)
        alpha=0.7           # blending weight for market mid vs fair value (0..1)
    ):
        self.name = name
        self.fair_value = fair_value
        self.base_spread = int(base_spread)
        self.size = size
        self.max_inventory = max_inventory
        self.alpha = alpha

        # track active quotes so that we can cancel exactly what we placed
        self.last_bid = None
        self.last_ask = None

        # inventory: positive = net long, negative = net short
        self.inventory = 0

    # -------------------------
    # Public API
    # -------------------------
    def act(self, orderbook):
        """
        Called every simulation tick. The MM will:
         - determine a safe mid price (blend of market and fair)
         - compute spread (wider if inventory risk is high)
         - compute a small inventory skew (to reduce net position)
         - cancel previous quotes it placed
         - place new bid/ask quotes (buy below mid, sell above mid)
        """
        best_bid = orderbook.best_bid()
        best_ask = orderbook.best_ask()

        # if book is empty use fair value as fallback
        if best_bid is None or best_ask is None:
            market_mid = self.fair_value
        else:
            market_mid = (best_bid + best_ask) / 2

        # blended mid: follows market mostly but anchored to fair value
        mid = self.alpha * market_mid + (1 - self.alpha) * self.fair_value

        # dynamic spread: widen if inventory pressure is high
        inv_pressure = min(abs(self.inventory) / max(1, self.max_inventory), 1.0)
        spread = max(1, int(round(self.base_spread * (1 + inv_pressure))))
        half_spread = max(1, spread // 2)

        # inventory skew: push quotes toward reducing inventory
        # positive inventory -> more eager to sell -> shift quotes slightly down
        # negative inventory -> more eager to buy -> shift quotes slightly up
        skew_factor = 0.5  # tune: how aggressive inventory skew is relative to spread
        skew = int(round(skew_factor * (self.inventory / max(1, self.max_inventory)) * spread))

        # compute integer tick prices
        new_bid = int(round(mid)) - half_spread + skew
        new_ask = int(round(mid)) + half_spread + skew

        # safety: don't cross
        if new_ask <= new_bid:
            new_ask = new_bid + 1

        # cancel only our old quotes (so we don't touch other liquidity)
        if self.last_bid is not None:
            orderbook.remove_order("buy", self.last_bid, self.size)
        if self.last_ask is not None:
            orderbook.remove_order("sell", self.last_ask, self.size)

        # place new quotes
        orderbook.add_order("buy", new_bid, self.size)
        orderbook.add_order("sell", new_ask, self.size)

        # record quotes for future cancellation
        self.last_bid = new_bid
        self.last_ask = new_ask

        # debug
        print(f"{self.name}: QUOTE bid={new_bid} ask={new_ask} size={self.size} inv={self.inventory}")

    def on_trade(self, side, volume):
        """
        Notification hook: call this from your matching engine when
        any trade occurs against the MM's quotes.

        side = "buy" means the MM bought (so inventory increases)
        side = "sell" means the MM sold (inventory decreases)

        IMPORTANT: You must call on_trade only when the trade actually involved the MM.
        How to detect: compare trade price vs last_bid/last_ask and trade side vs quote side.
        """
        if side == "buy":
            # MM bought (someone sold to MM) -> inventory increases
            self.inventory += volume
        elif side == "sell":
            # MM sold (someone bought from MM) -> inventory decreases
            self.inventory -= volume

        # optional: clamp inventory to avoid runaway values (not strictly necessary)
        if self.inventory > self.max_inventory:
            self.inventory = self.max_inventory
        if self.inventory < -self.max_inventory:
            self.inventory = -self.max_inventory
