from src.orderBook import OrderBook
from src.agent import RandomAgent
from src.marketMaker import MarketMaker
from src.marketOrder import MarketOrderAgent

import matplotlib.pyplot as plt
import random
import time

book = OrderBook()
history = []

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
        # both sides empty (very rare)
        mid = None

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
    RandomAgent("random1", "buy"),
    RandomAgent("random2", "buy"),
    RandomAgent("random3", "buy"),
    RandomAgent("random4", "buy"),
    RandomAgent("random5", "buy"),
    RandomAgent("random6", "sell"),
    RandomAgent("random7", "sell"),
    RandomAgent("random8", "sell"),
    RandomAgent("random9", "sell"),
    RandomAgent("random10", "sell"),

    MarketMaker("MarketMaker"),

    MarketOrderAgent("The Fomo Retail", "buy"),
    MarketOrderAgent("The Fomo Retail2", "sell"),
    MarketOrderAgent("agent"),
    MarketOrderAgent("agent"),
    MarketOrderAgent("agent"),
    MarketOrderAgent("agent"),
    MarketOrderAgent("agent"),
    MarketOrderAgent("agent")

]

for step in range(10000):
    random.shuffle(agents) #to mix them up to simulate unpredictability
    for agent in agents:
        agent.act(book)
    book.match()
    book.display()
    update_history()
    update_graph()
    time.sleep(0)


# Keep the plot displayed after the loop finishes
plt.ioff()
plt.show()

# plt.plot(history)
# plt.title("Price History")
# plt.xlabel("Time Step")
# plt.ylabel("Mid Price")
# plt.show()


