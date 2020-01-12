from typing import NamedTuple, str, int, float
from datetime import date
from enum import Enum

class TrackedOrder(NamedTuple):
    asset: str
    units: int
    price: float
    date: date
    operation: Operation

class Operation(Enum):
    buy = 1
    sell = 2
