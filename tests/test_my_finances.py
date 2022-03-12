from datetime import date

import pytest
from dateutil.relativedelta import relativedelta

from my_finances import (
    date_is_within_the_invoice_period,
    float_to_currency_str,
    future_items_in_invoice,
    int_to_str,
    invoice_start_date,
    next_invoice_to_close,
    percentage_to_str,
    total_debt,
)


def test_total_debt(credit_card):
    result = total_debt(credit_card)
    expected = 500 + 400 + 300

    assert result == expected


def test_next_invoice_to_close(credit_card):
    today = date.today()
    credit_card[0].closing_date = today - relativedelta(months=1)
    credit_card[1].closing_date = today
    credit_card[2].closing_date = today + relativedelta(months=1)

    result = next_invoice_to_close(
        invoice_list=credit_card, reference_date=today - relativedelta(days=1)
    )

    assert result == credit_card[1]


def test_date_is_within_the_invoice_period__closing_today(
    invoice_closing_today,
):
    reference_date = invoice_closing_today.closing_date

    assert (
        date_is_within_the_invoice_period(
            invoice=invoice_closing_today, reference_date=reference_date
        )
        is False
    )


def test_date_is_within_the_invoice_period__one_day_before_closing(
    invoice_closing_today,
):
    reference_date = invoice_closing_today.closing_date - relativedelta(days=1)

    assert (
        date_is_within_the_invoice_period(
            invoice=invoice_closing_today, reference_date=reference_date
        )
        is True
    )


def test_date_is_within_the_invoice_period__one_month_before_closing(
    invoice_closing_today,
):
    reference_date = invoice_closing_today.closing_date - relativedelta(
        months=1
    )

    assert (
        date_is_within_the_invoice_period(
            invoice=invoice_closing_today, reference_date=reference_date
        )
        is True
    )


def test_date_is_within_the_invoice_period__one_month_and_one_day_before_closing(
    invoice_closing_today,
):
    reference_date = (
        invoice_closing_today.closing_date
        - relativedelta(months=1)
        - relativedelta(days=1)
    )

    assert (
        date_is_within_the_invoice_period(
            invoice=invoice_closing_today, reference_date=reference_date
        )
        is False
    )


def test_date_is_within_the_invoice_period__one_day_after_closing(
    invoice_closing_today,
):
    reference_date = invoice_closing_today.closing_date + relativedelta(days=1)

    assert (
        date_is_within_the_invoice_period(
            invoice=invoice_closing_today, reference_date=reference_date
        )
        is False
    )


def test_future_items_in_invoice__1(
    invoice_closing_today, recurring_item_for_today
):
    reference_date = invoice_closing_today.closing_date - relativedelta(days=2)
    recurring_item_for_today.day = (
        invoice_closing_today.closing_date - relativedelta(days=1)
    ).day

    result = future_items_in_invoice(
        reference_date=reference_date,
        invoice=invoice_closing_today,
        recurring_item_list=[recurring_item_for_today],
    )

    assert result == [recurring_item_for_today]


def test_future_items_in_invoice__2(
    invoice_closing_today, recurring_item_for_today
):
    reference_date = invoice_closing_today.closing_date - relativedelta(days=1)
    recurring_item_for_today.day = reference_date.day

    result = future_items_in_invoice(
        reference_date=reference_date,
        invoice=invoice_closing_today,
        recurring_item_list=[recurring_item_for_today],
    )

    assert result == []


def test_future_items_in_invoice__3(
    invoice_closing_today, recurring_item_for_today
):
    reference_date = (
        invoice_closing_today.closing_date
        - relativedelta(months=1)
        - relativedelta(days=1)
    )
    recurring_item_for_today.day = (
        invoice_closing_today.closing_date - relativedelta(days=1)
    ).day

    result = future_items_in_invoice(
        reference_date=reference_date,
        invoice=invoice_closing_today,
        recurring_item_list=[recurring_item_for_today],
    )

    assert result == [recurring_item_for_today]


@pytest.mark.parametrize(
    'value, expected',
    [(0.3, '0.30'), (3, '3.00'), (3.33, '3.33'), (3.333, '3.33')],
)
def test_float_to_currency_str(value, expected):
    assert float_to_currency_str(value) == expected


@pytest.mark.parametrize(
    'value, expected',
    [(123, '123'), (1234, '1,234')],
)
def test_int_to_str(value, expected):
    assert int_to_str(value) == expected


def test_invoice_start_date(invoice_closing_today):
    closing_date = invoice_closing_today.closing_date
    result = invoice_start_date(closing_date)

    assert (
        result.year == closing_date.year
        and result.month == (closing_date - relativedelta(months=1)).month
        and result.day == closing_date.day
    )


def test_percentage_to_str__with_1():
    assert percentage_to_str(1) == '1.00 %'


def test_percentage_to_str__with_1_point_2():
    assert percentage_to_str(1.2) == '1.20 %'


def test_percentage_to_str__with_1_point_23():
    assert percentage_to_str(1.23) == '1.23 %'


def test_percentage_to_str__with_1_point_234():
    assert percentage_to_str(1.234) == '1.23 %'


def test_percentage_to_str__with_1_point_235():
    assert percentage_to_str(1.235) == '1.24 %'
