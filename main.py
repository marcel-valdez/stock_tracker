
import argparse

from lib.robinhood import get_client, OrderQueryOptions, RobinhoodTracker
from lib.util import to_csv, write_to_file

parser = argparse.ArgumentParser(
    prog='Stock Tracker',
    description='Simple portfolio exporter for exchanges. Supported exchanges: Robinhood'
)
parser.add_argument('--auth_config_file',
                    metavar='auth_config_file',
                    type=str,
                    help='Path the json file with the account information. JSON structure \n{ account: {user: <username>, password: <password> } }')
parser.add_argument('--csv_file',
                    metavar='csv_file',
                    type=str,
                    help='File on which the CSV contents will be written to.')

def main() -> None:
    args = parser.parse_args()
    client = get_client(args.auth_config_file)
    tracker = RobinhoodTracker(client)
    tracker.initialize()
    orders = tracker.stock_orders(OrderQueryOptions(only_filled=True))
    csv = to_csv(orders)
    write_to_file(args.csv_file, csv)

if __name__ == '__main__':
    main()
