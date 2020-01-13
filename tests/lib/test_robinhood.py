import unittest

from datetime import datetime
from typing import Tuple, Any
from unittest.mock import MagicMock

from lib.robinhood import OrderQueryOptions, TrackedOrder, Operation, RobinhoodTracker
from lib.fast_arrow_client import FastArrowClient, RobinhoodOrder

DEFAULT_ORDER = {
    "price":"140.00000000",
    "quantity":"7.00000000",
    "account":"https://api.robinhood.com/accounts/921573903/",
    "executions":[],
    "last_trail_price":None,
    "ref_id":"4555b169-902a-44ad-9960-57ee4f1661af",
    "extended_hours":False,
    "override_day_trade_checks":False,
    "cancel":None,
    "last_transaction_at":"2018-11-19T07:15:58.654779Z",
    "instrument":"https://api.robinhood.com/instruments/ebab2398-028d-4939-9f1d-13bf38f81c50/",
    "created_at":"2018-11-18T01:23:55.205178Z",
    "override_dtbp_checks":False,
    "reject_reason":None,
    "last_trail_price_updated_at":None,
    "trigger":"immediate",
    "stop_price":None,
    "position":"https://api.robinhood.com/positions/921573903/ebab2398-028d-4939-9f1d-13bf38f81c50/",
    "updated_at":"2018-11-19T07:15:58.805745Z",
    "cumulative_quantity":"0.00000000",
    "time_in_force":"gfd",
    "average_price": None,
    "type":"limit",
    "response_category":"unknown",
    "url":"https://api.robinhood.com/orders/a5183212-cfbd-46aa-9df1-0b660c3ce6fc/",
    "state":"cancelled",
    "side":"buy",
    "stop_triggered_at":None,
    "fees":"0.00",
    "id":"a5183212-cfbd-46aa-9df1-0b660c3ce6fc"
}

class TestRobinhood(unittest.TestCase):

    def to_robinhood_order(self, test_order: Tuple[str, Any]) -> RobinhoodOrder:
        field_values = {}
        for key in RobinhoodOrder._fields:
            field_values[key] = test_order[key]
        return RobinhoodOrder(**field_values)

    def make_test_order(self, override={}) -> RobinhoodOrder:
        result = {}
        result.update(DEFAULT_ORDER)
        result.update(override)
        return self.to_robinhood_order(result)

    def test_stock_orders(self) -> None:
        # given
        mock_client = FastArrowClient({})
        mock_orders = [
            self.make_test_order({'state': 'filled', 'price': '141.0'}),
            self.make_test_order({'state': 'pending',
                                  'last_transaction_at':'2018-11-19T07:15:58Z'})
        ]
        expected_orders = [
            TrackedOrder(
                asset="FB",
                units=7.0,
                price=141.0,
                date=datetime(2018, 11, 19, 7, 15, 58, 654779),
                operation=Operation.BUY
            ),
            TrackedOrder(
                asset="FB",
                units=7.0,
                price=140.0,
                date=datetime(2018, 11, 19, 7, 15, 58),
                operation=Operation.BUY
            ),
        ]
        target = RobinhoodTracker(mock_client, lambda _: '{ "symbol": "FB" }')
        mock_client.get_stock_orders = MagicMock(return_value=mock_orders)
        # when
        actual_orders = target.stock_orders(OrderQueryOptions(only_filled=False))
        # then
        self.assertEqual(expected_orders, actual_orders)

if __name__ == '__main__':
    unittest.main()
