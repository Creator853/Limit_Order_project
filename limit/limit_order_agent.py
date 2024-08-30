from typing import List, Dict, Any
from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener

class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient) -> None:
        self.execution_client = execution_client
        self.orders = []  # A list to store orders

    def add_order(self, buy: bool, product_id: str, amount: int, limit: float) -> None:
        order = {
            'buy': buy,
            'product_id': product_id,
            'amount': amount,
            'limit': limit
        }
        self.orders.append(order)

    def on_price_tick(self, product_id: str, price: float) -> None:
        for order in self.orders:
            if order['product_id'] == product_id:
                if order['buy'] and price <= order['limit']:
                    self.execution_client.buy(product_id, order['amount'])
                    self.orders.remove(order)
                elif not order['buy'] and price >= order['limit']:
                    self.execution_client.sell(product_id, order['amount'])
                    self.orders.remove(order)
