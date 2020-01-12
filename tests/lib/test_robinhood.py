import unittest

from unittest.mock import MagicMock
from lib.robinhood import stock_orders
from lib.fast_arrow_client import FastArrowClient

class TestRobinhood(unittest.TestCase):

    def test_stock_orders(self) -> None:
        # given
        mock_client = FastArrowClient({})
        mock_orders = [
            {"state": "filled"},
            {"state": "pending"},
        ]
        expected_orders = [{
            "asset": "FB",
            "units": 1,
            "price": 10.1,
            "date": "1/1/2001",
            "operation": "buy"
        }]
        mock_client.get_stock_orders = MagicMock(return_value=mock_orders)
        # when
        actual_orders = stock_orders(mock_client)
        # then
        self.assertEqual(expected_orders, actual_orders)

if __name__ == '__main__':
    unittest.main()
