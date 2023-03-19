import datetime
from django.test import TestCase
from django.db.utils import IntegrityError

from currency_rates_app.models import Currencies, RatesBaseDollar


class TestModels(TestCase):
    def test_duplicate_currency(self):
        """
        Checks for exception when trying to create same currency
        """
        first_currency = Currencies(**{'name': 'Sterling', 'code': 'GBP', 'symbol': '£'})
        first_currency.save()

        second_currency = Currencies(**{'name': 'Sterling', 'code': 'GBP', 'symbol': '£'})

        with self.assertRaises(IntegrityError):
            second_currency.save()

    def test_duplicate_rate(self):
        """
        Checks for exception when trying to create a rate for a currency that already has a currency for that date
        """
        currency = Currencies(**{'name': 'Sterling', 'code': 'GBP', 'symbol': '£'})
        currency.save()

        first_rate = RatesBaseDollar(**{'currency': currency, 'date': datetime.date(2023, 1, 2), 'rate': 0.8296})
        first_rate.save()

        second_rate = RatesBaseDollar(**{'currency': currency, 'date': datetime.date(2023, 1, 2), 'rate': 0.8296})

        with self.assertRaises(IntegrityError):
            second_rate.save()
