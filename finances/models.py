from dataclasses import dataclass
from datetime import date


@dataclass
class Invoice:
    closing_date: date
    due_date: date
    value: float


@dataclass
class RecurringItem:
    name: str
    day: int
    value: float
