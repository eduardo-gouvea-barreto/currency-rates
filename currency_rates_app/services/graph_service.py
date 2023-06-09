import datetime
from typing import List

from currency_rates.settings import DEFAULT_CURRENCY_CODE, MAX_ENTRIES, DEFAULT_DATE_FORMAT
from currency_rates_app.models import Currencies, RatesBaseDollar
from currency_rates_app.services.date_service import build_workdays_list
from currency_rates_app.services.fetch_data_service import FetchDataService


def gather_graph_info(currency: Currencies, date_min: datetime.date, date_max: datetime.date,
                      try_to_fetch_if_data_is_missing=True) -> (List[str], List[float], List[str]):
    """
    Creates graph series from cleaned form data.
    Also validates if all dates were used, if not, tries once to fetch them from external API.

    Returns a pair of lists containing dates and their respective currency exchange rates,
    and also a list with the dates where the information is missing in the database.
    """

    currency_rates = RatesBaseDollar.objects.filter(
        currency=currency,
        date__gte=date_min,
        date__lte=date_max
    ).order_by('date').values('date', 'rate')

    workday_list = build_workdays_list(date_min, date_max)

    dates = [date.strftime(DEFAULT_DATE_FORMAT) for date in currency_rates.values_list('date', flat=True)]
    rates = [float(rate) for rate in currency_rates.values_list('rate', flat=True)]
    missing_dates = [date for date in workday_list if date not in currency_rates.values_list('date', flat=True)]

    if missing_dates and try_to_fetch_if_data_is_missing:
        fetch_serv = FetchDataService([currency.code])
        new_data = fetch_serv.get_currency_rates(missing_dates)
        fetch_serv.insert_currency_rates(new_data)

        dates, rates, missing_dates = gather_graph_info(
            currency, date_min, date_max, try_to_fetch_if_data_is_missing=False
        )

    elif missing_dates:
        missing_dates = [date.strftime(DEFAULT_DATE_FORMAT) for date in missing_dates]

    return dates, rates, missing_dates


def build_default_graph() -> (Currencies, List[str], List[float]):
    """
    The default graph consists of the latest MAX_ENTRIES data for DEFAULT_CURRENCY_CODE
    """

    currency = Currencies.objects.get(code=DEFAULT_CURRENCY_CODE)

    currency_rates = RatesBaseDollar.objects.filter(
        currency__name=currency.name
    ).order_by('-date').values('date', 'rate')[:MAX_ENTRIES]

    dates = [date.strftime(DEFAULT_DATE_FORMAT) for date in currency_rates.values_list('date', flat=True)]
    dates.reverse()
    if not dates:  # No data in database
        dates = [datetime.date.today()]

    rates = [float(rate) for rate in currency_rates.values_list('rate', flat=True)]
    rates.reverse()

    return currency, dates, rates
