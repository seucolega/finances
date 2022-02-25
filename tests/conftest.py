from datetime import date
from typing import List

import pytest
from models import Invoice, RecurringItem


@pytest.fixture
def credit_card() -> List[Invoice]:
    return [
        Invoice(
            due_date=date(year=2022, month=3, day=22),
            closing_date=date(year=2022, month=3, day=15),
            value=500,
        ),
        Invoice(
            due_date=date(year=2022, month=4, day=22),
            closing_date=date(year=2022, month=4, day=15),
            value=400,
        ),
        Invoice(
            due_date=date(year=2022, month=5, day=22),
            closing_date=date(year=2022, month=5, day=15),
            value=300,
        ),
    ]


@pytest.fixture
def invoice_closing_today() -> Invoice:
    today = date.today()
    return Invoice(closing_date=today, due_date=today, value=0)


@pytest.fixture
def recurring_item_for_today() -> RecurringItem:
    return RecurringItem(name='A Service', day=(date.today()).day, value=1)
