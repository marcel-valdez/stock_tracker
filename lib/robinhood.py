import json

from urllib import request
from datetime import datetime
from enum import Enum
from typing import List, NamedTuple, Callable
from lib.fast_arrow_client import FastArrowClient

class Operation(Enum):
    ''' Operation type of the transaction. '''
    BUY = 1
    SELL = 2

    def __str__(self):
        return {
            Operation.BUY: "BUY",
            Operation.SELL: "SELL"
        }.get(self)

ROBINHOOD_SIDE_TO_OPERATION = {
    "buy": Operation.BUY,
    "sell": Operation.SELL
}

TrackedOrder = NamedTuple('TrackedOrder', [
    ('asset', str), ('units', float), ('price', float), ('date', datetime),
    ('operation', Operation)
])

OrderQueryOptions = NamedTuple('OrderQueryOptions', [('only_filled', bool)])

def get_client(filepath: str) -> FastArrowClient:
    ''' Creates an authentication client for Robinhood. '''
    with open(filepath) as auth_json:
        auth_config = json.loads(auth_json.read())
    return FastArrowClient(auth_config)

def fetch_url(asset_url: str) -> str:
    with request.urlopen(asset_url) as url:
        return url.read().decode()

class RobinhoodTracker:
    ''' Tracks stock orders from the Robinhood Exchange. '''

    def __init__(self,
                 client: FastArrowClient,
                 url_fetcher: Callable[[str], str] = fetch_url):
        self.client = client
        self.url_fetcher = url_fetcher
        self.asset_cache = {}

    def initialize(self) -> None:
        ''' Initializes the authentication client. '''
        self.client.initialize()

    def stock_orders(self, options: OrderQueryOptions) -> List[TrackedOrder]:
        '''
        options:
        - only_filled. Only return filled orders. Default = False.
        '''
        raw_orders = self.client.get_stock_orders()
        only_filled = options.only_filled
        if only_filled:
            raw_orders = list(filter(lambda x: x.state == 'filled', raw_orders))

        orders = []
        for raw_order in raw_orders:
            fields = {}
            fields['units'] = float(raw_order.quantity)
            fields['asset'] = self.__fetch_asset_name(raw_order.instrument)
            fields['price'] = float(raw_order.price)
            fields['date'] = RobinhoodTracker.__parse_datetime(raw_order.last_transaction_at)
            fields['operation'] = ROBINHOOD_SIDE_TO_OPERATION[raw_order.side]
            orders.append(TrackedOrder(**fields))
        return orders

    @staticmethod
    def __parse_datetime(datetime_str: str) -> datetime:
        try:
            return datetime.strptime(datetime_str, '%Y-%m-%dT%X.%fZ')
        except ValueError:
            pass
        return datetime.strptime(datetime_str, '%Y-%m-%dT%XZ')

    def __fetch_asset_name(self, asset_url: str) -> str:
        if self.asset_cache.get(asset_url) is None:
            response = self.url_fetcher(asset_url)
            asset = json.loads(response)
            self.asset_cache[asset_url] = asset['symbol']
        return self.asset_cache.get(asset_url)
