from typing import Tuple, Any, List
from lib.robinhood_order import RobinhoodOrder
from fast_arrow import Client, StockOrder

class Account(NamedTuple):
    user: str
    password: str

class AuthConfig(NamedTuple):
    account: Account

class RobinhoodOrder(NamedTuple):
    state: str

class FastArrowClient:
    def __init__(self, auth_config: AuthConfig):
        self.auth_config = auth_config
        self.client = None

    def initialize(self):
        if self.client is None:
            self.client = Client(self.auth_config)

    def get_stock_orders(self) -> Tuple[str, Any]:
        if self.client is None:
            raise Exception("Initialize the client first.")

        return StockOrder.all(self.client)
