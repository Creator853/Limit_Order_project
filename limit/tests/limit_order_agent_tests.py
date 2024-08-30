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
