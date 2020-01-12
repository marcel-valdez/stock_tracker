import json

from typing import Tuple, Any, List, NamedTuple
from lib import util
from lib.fast_arrow_client import FastArrowClient
from lib.tracked_order import TrackedOrder

class OrderQueryOptions(NamedTuple):
    only_filled: bool = False


def get_client(filepath: str) -> FastArrowClient:
    with open(filepath) as auth_json:
        auth_config = json.loads(auth_json.read())

    return FastArrowClient(auth_config)

def stock_orders(client: FastArrowClient, options: OrderQueryOptions) -> List[TrackedOrder]:
    '''
    options:
        - only_filled. Only return filled orders. Default = False.
    '''
    orders = client.get_stock_orders()
    only_filled = options.only_filled
    if only_filled:
        orders = list(filter(lambda x: x["state"] == "filled", orders))
    return orders
