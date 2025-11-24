from src.orderBook import OrderBook
from src.randomAgent import RandomAgent
from src.marketMaker import MarketMaker
from src.marketOrder import MarketOrderAgent
from src.trendFollower import TrendFollower
from src.whale import WhaleAgent

import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import random
from datetime import datetime, timedelta

# ------------------------------
# CONFIG
# ------------------------------
CANDLE_WINDOW = 5
PLOT_INTERVAL = 25
SIMULATION_STEPS = 10000

N_Random_Agent = 1000
N_Market_Order_Agent = 300
N_Trend_Follower_Agent = 200
N_Whale_Agent = 10

INITIAL_PRICE = 100.0
# ------------------------------

# State
book = OrderBook()
history = []
_candle_buffer = []
_ohlc_records = []

# Plot state
candle_fig = None
candle_ax = None
fig = None
ax = None
line = None


# ------------------------------
# Candle + History Helpers
# ------------------------------
def append_candle_sample(sample):
    global _candle_buffer, _ohlc_records

    _candle_buffer.append(sample)

    if len(_candle_buffer) >= CANDLE_WINDOW:
        chunk = _candle_buffer[:CANDLE_WINDOW]

        o = chunk[0]
        h = max(chunk)
        l = min(chunk)
        c = chunk[-1]

        # timestamp for candle
        if _ohlc_records:
            next_dt = _ohlc_records[-1]["Date"] + timedelta(seconds=1)
        else:
            next_dt = datetime.now()

        _ohlc_records.append({
            "Date": next_dt,
            "Open": o,
            "High": h,
            "Low": l,
            "Close": c
        })

        _candle_buffer = _candle_buffer[CANDLE_WINDOW:]


def update_midprice_history():
    bid = book.best_bid()
    ask = book.best_ask()

    if bid is not None and ask is not None:
        mid = (bid + ask) / 2
    elif bid is not None:
        mid = bid
    elif ask is not None:
        mid = ask
    else:
        mid = history[-1] if history else INITIAL_PRICE

    history.append(mid)
    append_candle_sample(mid)


# ------------------------------
# Plot Functions
# ------------------------------
def update_price_line():
    line.set_xdata(range(len(history)))
    line.set_ydata(history)

    ax.relim()
    ax.autoscale_view()

    fig.canvas.draw()
    fig.canvas.flush_events()


def update_candles():
    global candle_fig, candle_ax

    if not _ohlc_records:
        return

    df = pd.DataFrame(_ohlc_records)
    df.set_index("Date", inplace=True)

    mc = mpf.make_marketcolors(up='g', down='r')
    s = mpf.make_mpf_style(base_mpf_style='charles', marketcolors=mc)

    # First time
    if candle_fig is None:
        candle_fig, axes = mpf.plot(
            df,
            type='candle',
            style=s,
            returnfig=True,
            figsize=(8, 4)
        )
        candle_ax = axes[0]
        plt.show(block=False)
        return

    # Update existing
    candle_ax.clear()
    mpf.plot(
        df,
        type='candle',
        style=s,
        ax=candle_ax,
        returnfig=False
    )

    candle_fig.canvas.draw()
    candle_fig.canvas.flush_events()


# ------------------------------
# INIT interactive plot
# ------------------------------
plt.ion()
fig, ax = plt.subplots(figsize=(8, 3))
line, = ax.plot([], [])
ax.set_title("Price History")
ax.set_xlabel("Time Step")
ax.set_ylabel("Mid Price")
plt.show(block=False)


# ------------------------------
# Seed & Agents
# ------------------------------
book.add_order("buy", 100, 20)
book.add_order("sell", 101, 20)

agents = [MarketMaker("MarketMaker")]

agents += [RandomAgent(f"RandomAgent{x}") for x in range(N_Random_Agent)]
agents += [MarketOrderAgent(f"MarketOrder{x}") for x in range(N_Market_Order_Agent)]
agents += [TrendFollower(f"Trend{x}") for x in range(N_Trend_Follower_Agent)]
agents += [WhaleAgent(f"Whale{x}") for x in range(N_Whale_Agent)]


# ------------------------------
# RUN SIMULATION
# ------------------------------
print("Starting simulation...")

for step in range(SIMULATION_STEPS):
    random.shuffle(agents)

    for ag in agents:
        ag.act(book, history)

    book.match()
    update_midprice_history()

    if step % PLOT_INTERVAL == 0:
        update_price_line()
        update_candles()

# Final sync
update_price_line()
update_candles()

plt.ioff()
plt.show()

print("Simulation complete. Total samples:", len(history))
