from src.orderBook import OrderBook
from src.agent import RandomAgent

book = OrderBook()
agent1 = RandomAgent("A1")
agent2 = RandomAgent("A2")

for step in range(10000):
    agent1.act(book)
    agent2.act(book)
    book.match()
