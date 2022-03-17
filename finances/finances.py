import datetime
from typing import List, Union

from data import (
    budgeted_amount_per_month,
    credit_card,
    recurring_items_on_credit_card,
)
from dateutil.relativedelta import relativedelta
from models import Invoice, RecurringItem


def total_debt(invoice_list: List[Invoice]):
    return sum(month.value for month in invoice_list)


def next_invoice_to_close(
    invoice_list: List[Invoice], reference_date: datetime.date
) -> Invoice:
    return next(
        (
            month
            for month in invoice_list
            if month.closing_date > reference_date
        ),
        None,
    )


def future_items_in_invoice(
    reference_date: datetime.date,
    invoice: Invoice,
    recurring_item_list: List[RecurringItem],
) -> List[RecurringItem]:
    date_on_this_invoice = date_is_within_the_invoice_period(
        invoice=invoice, reference_date=reference_date
    )

    if date_on_this_invoice:
        return [
            item
            for item in recurring_item_list
            if reference_date.day < item.day < invoice.closing_date.day
        ]

    return recurring_item_list


def int_to_str(value: int) -> str:
    return f'{value:,}'


def float_to_currency_str(value: float) -> str:
    return f'{round(value, 2):,.2f}'


def percentage_to_str(value: float) -> str:
    return f'{round(value, 2):,.2f} %'


def invoice_info(*args: Union[str, int, float, datetime.date]) -> str:
    cols = (40, 15, 15, 13)
    padding_character = ' '
    result = ''

    for index, arg in enumerate(args):
        if isinstance(arg, int):
            arg = int_to_str(arg)
        elif isinstance(arg, float):
            arg = float_to_currency_str(arg)
        elif isinstance(arg, datetime.date):
            arg = arg.strftime('%d/%m/%Y')

        if index > 0:
            result += arg.rjust(cols[index], padding_character)
        else:
            result += arg.ljust(cols[index], padding_character)

    return result


def invoice_start_date(closing_date: datetime.date) -> datetime.date:
    return closing_date - relativedelta(months=1)


def date_is_within_the_invoice_period(
    invoice: Invoice, reference_date: datetime.date
) -> bool:
    return (
        invoice_start_date(invoice.closing_date)
        <= reference_date
        < invoice.closing_date
    )


def invoice_to_print(invoice: Invoice, reference_date: datetime.date) -> str:
    indentation = 4 * ' '
    result = []

    sum_of_future_items = sum(
        item.value
        for item in future_items_in_invoice(
            reference_date=reference_date,
            invoice=invoice,
            recurring_item_list=recurring_items_on_credit_card,
        )
    )
    invoice.value += sum_of_future_items

    start_date = invoice_start_date(invoice.closing_date)
    total_days = (invoice.closing_date - start_date).days
    elapsed_days = (max(reference_date, start_date) - start_date).days
    days_remaining = (
        invoice.closing_date - max(reference_date, start_date)
    ).days
    percentage_used = invoice.value / budgeted_amount_per_month * 100
    percentage_of_days_elapsed = elapsed_days / total_days * 100
    usage_status = (
        'Good' if percentage_used < percentage_of_days_elapsed else 'Not good'
    )

    result.append(
        invoice_info(
            f'{invoice.due_date.strftime("%B %Y")} Invoice',
            invoice.value,
            percentage_to_str(percentage_used),
            usage_status,
        )
    )

    if sum_of_future_items:
        current_value = invoice.value - sum_of_future_items
        result.append(
            invoice_info(
                indentation + 'Current value',
                current_value,
                percentage_to_str(
                    current_value / budgeted_amount_per_month * 100
                ),
            )
        )

        result.append(
            invoice_info(
                indentation + 'Value of future items',
                sum_of_future_items,
                percentage_to_str(
                    sum_of_future_items / budgeted_amount_per_month * 100
                ),
            )
        )

    if reference_date >= start_date:
        result.append(
            invoice_info(
                indentation + 'Days from the start of the invoice',
                elapsed_days,
                percentage_to_str(percentage_of_days_elapsed),
            )
        )
        result.append(
            invoice_info(
                indentation + 'Remaining days until closing',
                days_remaining,
                percentage_to_str(days_remaining / total_days * 100),
            )
        )

    available_value = budgeted_amount_per_month - invoice.value

    result.append(
        invoice_info(
            indentation + 'You are saving',
            available_value,
            percentage_to_str(
                available_value / budgeted_amount_per_month * 100
            ),
        )
    )

    if available_value > 0:
        value_available_per_day = available_value / days_remaining
        percentage_available_per_day = (
            value_available_per_day / budgeted_amount_per_month * 100
        )
        result.append(
            invoice_info(
                indentation + 'Daily value available until closing',
                value_available_per_day,
                percentage_to_str(percentage_available_per_day),
            )
        )

    result.append(
        invoice_info(
            indentation + 'Start and end date of items',
            start_date,
            invoice.closing_date - relativedelta(days=1),
        )
    )

    result.append(
        invoice_info(
            indentation + 'Closing and due date',
            invoice.closing_date,
            invoice.due_date,
        )
    )

    return '\n'.join(result)


def init():
    today = datetime.date.today()

    next_invoice = next_invoice_to_close(
        invoice_list=credit_card, reference_date=today
    )

    if next_invoice:
        print()
        print(invoice_to_print(invoice=next_invoice, reference_date=today))

        second_next_invoice = next_invoice_to_close(
            invoice_list=credit_card,
            reference_date=next_invoice.closing_date + relativedelta(days=1),
        )

        if second_next_invoice:
            print()
            print(invoice_to_print(second_next_invoice, reference_date=today))


if __name__ == '__main__':
    init()
