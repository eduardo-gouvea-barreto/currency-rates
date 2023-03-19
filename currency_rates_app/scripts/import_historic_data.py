import datetime
import django
import os

from currency_rates.settings import FIRST_AVAILABLE_DATE
from currency_rates_app.services.fetch_data_service import FetchDataService
from currency_rates_app.services.date_service import build_workdays_list


def import_historic_data():
    """
    This script fecthes all historic data from the public API VATcomply and stores it in the Django Database
    For more information on the API, please visit https://vatcomply.com/
    It is intended for use only once when you first deploy the server.
    """
    date_start = datetime.date(*FIRST_AVAILABLE_DATE)
    date_end = datetime.date.today()
    dates_list = build_workdays_list(date_start, date_end)

    currencies_codes = list(Currencies.objects.values_list('code', flat=True))

    fetch_serv = FetchDataService(currencies_codes)
    new_data = fetch_serv.get_currency_rates(dates_list)
    fetch_serv.insert_currency_rates(new_data)


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'currency_rates.settings'
    django.setup()

    from currency_rates_app.models import Currencies

    import_historic_data()
