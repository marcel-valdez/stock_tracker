
from typing import List
from io import StringIO
from lib.robinhood import TrackedOrder

def to_csv(orders: List[TrackedOrder]) -> str:
    '''
    Convert tracked orders to a string in CSV format.
    '''
    buffer = StringIO()
    for order in orders:
        order_dict = order._asdict()
        for field in TrackedOrder._fields:
            buffer.write(str(order_dict.get(field)))
            buffer.write(',')
        buffer.write('\n')
    return buffer.getvalue()

def write_to_file(path: str, content: str) -> None:
    ''' Writes a string to a file. '''
    with open(path, 'w') as file:
        file.write(content)
