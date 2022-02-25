from datetime import date
from typing import List

from models import Invoice, RecurringItem

budgeted_amount_per_month = 2000

credit_card: List[Invoice] = [
    Invoice(
        due_date=date(year=2022, month=3, day=22),
        closing_date=date(year=2022, month=3, day=16),
        value=1000.50,
    ),
    Invoice(
        due_date=date(year=2022, month=4, day=22),
        closing_date=date(year=2022, month=4, day=16),
        value=900,
    ),
    Invoice(
        due_date=date(year=2022, month=5, day=22),
        closing_date=date(year=2022, month=5, day=16),
        value=800,
    ),
    Invoice(
        due_date=date(year=2022, month=6, day=22),
        closing_date=date(year=2022, month=6, day=16),
        value=700,
    ),
    Invoice(
        due_date=date(year=2022, month=7, day=22),
        closing_date=date(year=2022, month=7, day=16),
        value=600,
    ),
    Invoice(
        due_date=date(year=2022, month=8, day=22),
        closing_date=date(year=2022, month=8, day=16),
        value=500,
    ),
]

recurring_items_on_credit_card: List[RecurringItem] = [
    RecurringItem(name='Service 1', day=3, value=40.23),
    RecurringItem(name='Service 2', day=11, value=50),
    RecurringItem(name='Service 3', day=18, value=55),
]
