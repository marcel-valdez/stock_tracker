import json

from os import path
from typing import Tuple, Any, List, NamedTuple

from fast_arrow import Client, StockOrder
from fast_arrow_auth import Client as AuthClient

Account = NamedTuple('Account', [('user', str), ('password', str)])
AuthConfig = NamedTuple('AuthConfig', [('account', Account)])
RobinhoodOrder = NamedTuple('RobinhoodOrder', [
    ('instrument', str),
    ('last_transaction_at', str),
    ('price', str),
    ('quantity', str),
    ('state', str),
    ('side', str),
    ('id', str),
])

class FastArrowClient:
    '''
    Wrapper client around the Fast Arrow Robinhood API.
    '''
    def __init__(self, auth_config: AuthConfig):
        self.auth_config = auth_config
        self.client = None
        self.auth_client = None

    def initialize(self) -> None:
        '''
        Initializes the client by authenticating against the Robinhood exchange.
        '''
        if self.client is None:
            self.client = Client(self.__gen_credentials())

    def get_stock_orders(self) -> List[RobinhoodOrder]:
        '''
        Fetches the stock orders from the remote Robinhood exchange.
        '''
        if self.client is None:
            raise Exception("Initialize the client first.")
        raw_orders = StockOrder.all(self.client)
        return self.__raw_to_robinhood_orders(raw_orders)

    def __raw_to_robinhood_orders(self, raw_orders: List[Tuple[str, Any]]) -> List[RobinhoodOrder]:
        orders = []
        for raw_order in raw_orders:
# TODO: Handle execution of composed orders
#            if not raw_order.get('executions') is None:
#                more_raw_orders = raw_order.get('executions')
#                more_orders = self.__raw_to_robinhood_orders(more_raw_orders)
#                orders.extend(more_orders)
#            else:
            order = self.__raw_to_robinhood_order(raw_order)
            if not order is None:
                orders.append(order)
            else:
                print("Skipping order with missing required field value.")
                print(str(raw_order))
        return orders

    def __raw_to_robinhood_order(self, raw_order: Tuple[str, Any]) -> RobinhoodOrder:
        field_values = {}
        for field in RobinhoodOrder._fields:
            field_value = raw_order.get(field)
            if field_value is None and field == 'price':
                # This handles composed orders by using the average instead of each one individually
                field_value = raw_order['average_price']
            if field_value is None:
                return None
            field_values[field] = field_value
        return RobinhoodOrder(**field_values)

    def __gen_credentials(self) -> Tuple[str, str]:
        credentials = self.__load_credentials()
        if not credentials is None:
            # TODO: what about stale credentials?
            # we need to be able to delete those
            return credentials

        username = self.auth_config['account']['user']
        password = self.auth_config['account']['password']
        mfa_code = self.auth_config['account']['mfa_code']
        device_token = self.auth_config['account']['device_token']

        if self.auth_client is None:
            self.auth_client = AuthClient(
                username=username, password=password, mfa_code=mfa_code, device_token=device_token)

        while not self.auth_client.authenticated:
            print('Authenticating with Robinhood...')
            try:
                self.auth_client.authenticate()
            except KeyError as err:
                # fast_arrow_auth raises a KeyError when it gets the MFA challenge
                print('Error while authenticating with the Robinhood. You may need to privde a 2FA code.')
                print(err)

            if not self.auth_client.authenticated:
                mfa_code = input('Please enter 2FA code: ')
                self.auth_client.mfa_code = mfa_code

        if self.auth_client.authenticated:
            print('Successfully authenticated!')
            credentials = self.auth_client.gen_credentials()
            self.__store_credentials(credentials)
            return credentials

        raise Exception('Unable to authenticate with Robinhood server.')

    def __store_credentials(self, credentials: Tuple[str, Any]):
        # TODO: This should be encrypted.
        with open('credentials.json', 'w') as file:
            json.dump(credentials, file)

    def __load_credentials(self) -> Tuple[str, Any]:
        # TODO: This should be encrypted.
        if path.exists('credentials.json'):
            with open('credentials.json', 'r') as file:
                return json.load(file)
