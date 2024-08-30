# Limit_Order_project

To implement the LimitOrderAgent class and the required functionalities, follow these steps:

1. Implement LimitOrderAgent

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

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

2. Implement Tests for LimitOrderAgent

import unittest
from unittest.mock import Mock
from limit.limit_order_agent import LimitOrderAgent

class LimitOrderAgentTest(unittest.TestCase):
    def setUp(self):
        self.execution_client = Mock()
        self.agent = LimitOrderAgent(self.execution_client)

    def test_buy_order_execution(self):
        self.agent.add_order(buy=True, product_id='IBM', amount=1000, limit=100.0)
        self.agent.on_price_tick('IBM', 99.0)
        self.execution_client.buy.assert_called_with('IBM', 1000)

    def test_sell_order_execution(self):
        self.agent.add_order(buy=False, product_id='IBM', amount=500, limit=150.0)
        self.agent.on_price_tick('IBM', 151.0)
        self.execution_client.sell.assert_called_with('IBM', 500)

    def test_no_order_execution(self):
        self.agent.add_order(buy=True, product_id='IBM', amount=1000, limit=100.0)
        self.agent.on_price_tick('IBM', 101.0)
        self.execution_client.buy.assert_not_called()

if __name__ == '__main__':
    unittest.main()



-------------------------------------------------------------THESE ARE TESTS------------------------------------------------------------------------------------

1. Test: Buy Order Execution
Description: Test if a buy order is executed when the market price drops below the limit.

Test Code:

def test_buy_order_execution(self):
    self.agent.add_order(buy=True, product_id='IBM', amount=1000, limit=100.0)
    self.agent.on_price_tick('IBM', 99.0)
    self.execution_client.buy.assert_called_with('IBM', 1000)

Expected Output:

----------------------------------------------------------------------
Ran 1 test in 0.001s

OK

Explanation: The test should pass if the buy method of the execution_client is called with the correct product ID and amount when the price is below the limit.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

2. Test: Sell Order Execution
Description: Test if a sell order is executed when the market price exceeds the limit.

Test Code:

def test_sell_order_execution(self):
    self.agent.add_order(buy=False, product_id='IBM', amount=500, limit=150.0)
    self.agent.on_price_tick('IBM', 151.0)
    self.execution_client.sell.assert_called_with('IBM', 500)

Expected Output:

----------------------------------------------------------------------
Ran 1 test in 0.001s

OK

Explanation: The test should pass if the sell method of the execution_client is called with the correct product ID and amount when the price is above the limit.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

3. Test: No Order Execution
Description: Test that no order is executed when the market price is not at or better than the limit.

Test Code:

def test_no_order_execution(self):
    self.agent.add_order(buy=True, product_id='IBM', amount=1000, limit=100.0)
    self.agent.on_price_tick('IBM', 101.0)
    self.execution_client.buy.assert_not_called()

Expected Output:

----------------------------------------------------------------------
Ran 1 test in 0.001s

OK

Explanation: The test should pass if the buy method is not called when the price is above the limit, ensuring that no incorrect order execution occurs.

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

4. Test: Multiple Orders Handling

Description: Test if multiple orders are handled correctly.

Test Code:

def test_multiple_orders_execution(self):
    self.agent.add_order(buy=True, product_id='IBM', amount=1000, limit=100.0)
    self.agent.add_order(buy=False, product_id='AAPL', amount=500, limit=200.0)
    
    self.agent.on_price_tick('IBM', 99.0)
    self.agent.on_price_tick('AAPL', 201.0)
    
    self.execution_client.buy.assert_called_with('IBM', 1000)
    self.execution_client.sell.assert_called_with('AAPL', 500)

Expected Output:

----------------------------------------------------------------------
Ran 1 test in 0.002s

OK

Explanation: The test should pass if the correct buy and sell methods are called for different products when their respective price conditions are met.

These tests cover the primary functionality of the LimitOrderAgent and validate that it works as intended.
