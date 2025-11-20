from src.orderBook import OrderBook
from src.randomAgent import RandomAgent
from src.marketMaker import MarketMaker
from src.marketOrder import MarketOrderAgent
from src.trendFollower import TrendFollower
from src.whale import WhaleAgent

import matplotlib.pyplot as plt
import random
import time
import mplfinance as mpf
import pandas as pd

book = OrderBook()
history = []

CANDLE_WINDOW = 20

candle_fig = None
candle_ax = None

def update_candles(history):
    global candle_fig, candle_ax

    if len(history) < CANDLE_WINDOW:
        return

    # Convert history into OHLC
    ohlc = []
    for i in range(0, len(history), CANDLE_WINDOW):
        chunk = history[i:i+CANDLE_WINDOW]
        if len(chunk) < CANDLE_WINDOW:
            break
            
        ohlc.append([
            chunk[0],      # open
            max(chunk),    # high
            min(chunk),    # low
            chunk[-1],     # close
        ])

    df = pd.DataFrame(ohlc, columns=["Open", "High", "Low", "Close"])
    df.index = pd.date_range("2024-01-01", periods=len(df))

    # First-time initialization
    if candle_fig is None:
        candle_fig, axes = mpf.plot(
            df,
            type='candle',
            style='charles',
            returnfig=True
        )

        candle_ax = axes[0]  # <-- FIXED: use first (and only) axis

        plt.show(block=False)
        return

    # Update existing figure
    candle_ax.clear()

    mpf.plot(
        df,
        type='candle',
        style='charles',
        ax=candle_ax
    )

    candle_fig.canvas.draw()
    candle_fig.canvas.flush_events()
def update_graph():
    line.set_ydata(history)
    line.set_xdata(range(len(history))) 
        
    # Rescale the x and y axes automatically
    ax.relim()
    ax.autoscale_view()
        
    # Redraw the canvas
    fig.canvas.draw()
    fig.canvas.flush_events() 
        
    # Pause briefly so the OS can update the window
    # plt.pause(0.0001)

def update_history():
    bid = book.best_bid()
    ask = book.best_ask()

    if bid is not None and ask is not None:
        # normal mid price
        mid = (bid + ask) / 2
    elif bid is not None:
        # only bid side exists
        mid = bid
    elif ask is not None:
        # only ask side exists
        mid = ask
    else:
        # both sides empty, add last midpoint
        mid = history[-1]

    history.append(mid)


plt.ion() #enable plt interactive mode
#setup the plot
fig, ax = plt.subplots()
line, = ax.plot(history) # Get a reference to the line object
ax.set_title("Price History")
ax.set_xlabel("Time Step")
ax.set_ylabel("Mid Price")

#seed the market
book.add_order("buy", 100, 20)
book.add_order("sell", 101, 20)

agents = [
    MarketMaker("MarketMaker")
]

#number of agent
N_Random_Agent = 300
N_Market_Order_Agent = 50
N_Trend_Follower_Agent = 100
N_Whale_Agent = 10

#add random agent
for x in range(N_Random_Agent):
    agents.append(RandomAgent(f"RandomAgent{x+1}"))

for x in range(N_Market_Order_Agent):
    agents.append(MarketOrderAgent(f"MarketOrderAgent{x+1}"))

for x in range(N_Trend_Follower_Agent):
    agents.append(TrendFollower(f"TrendFollowerAgent{x+1}"))

for x in range(N_Whale_Agent):
    agents.append(WhaleAgent(f"WhaleAgent{x+1}"))

for step in range(10000):
    random.shuffle(agents) #to mix them up to simulate unpredictability
    for agent in agents:
        agent.act(book, history)
    book.match()
    book.display()
    update_history()
    update_graph()
    update_candles(history)
    time.sleep(0.01)


# Keep the plot displayed after the loop finishes
plt.ioff()
plt.show()

# plt.plot(history)
# plt.title("Price History")
# plt.xlabel("Time Step")
# plt.ylabel("Mid Price")
# plt.show()


