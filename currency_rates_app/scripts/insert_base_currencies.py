import django
from django.core.validators import ValidationError
import os
from typing import List, Dict


def insert_base_currencies(currencies: List[Dict[str, str]]):
    """
    Simple script that inserts in Database the base currencies for the project.
    You can also add them manually from the Admin page or directly in the database.
    """
    for currency in currencies:
        currency_model = Currencies(**currency)
        try:
            currency_model.validate_unique()
        except ValidationError:
            print(f"The currency {currency['name']} already exists.")
        else:
            currency_model.save()
            print(f"Currency {currency['name']} inserted successfully.")


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'currency_rates.settings'
    django.setup()

    from currency_rates_app.models import Currencies

    currencies_list = [
        {
            'name': 'Brazilian real',
            'code': 'BRL',
            'symbol': 'R$'
        },
        {
            'name': 'Euro',
            'code': 'EUR',
            'symbol': '€'
        },
        {
            'name': 'Japanese yen',
            'code': 'JPY',
            'symbol': '¥'
        },
    ]

    insert_base_currencies(currencies_list)
