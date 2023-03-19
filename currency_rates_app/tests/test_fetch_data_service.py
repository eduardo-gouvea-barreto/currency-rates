import datetime
from django.test import TestCase
from django.urls import reverse

from currency_rates_app.models import Currencies, RatesBaseDollar
from currency_rates_app.services.fetch_data_service import FetchDataService


class TestFetchDataEmptyRates(TestCase):
    fixtures = ['currencies.json']

    def test_single_api_fetch(self):
        """
        Test if FetchService is working by requesting some data and inserting in database.
        Depends on external API!
        """
        currencies_codes = list(Currencies.objects.values_list('code', flat=True))
        fetch_serv = FetchDataService(currencies_codes)
        new_data = fetch_serv.get_currency_rates([datetime.date(2023, 1, 2)])
        fetch_serv.insert_currency_rates(new_data)

        inserted_data = [
            value for value in RatesBaseDollar.objects.all().values('currency_id', 'date')
        ]
        expected_data = [
            {'currency_id': 1, 'date': datetime.date(2023, 1, 2)},
             {'currency_id': 2, 'date': datetime.date(2023, 1, 2)},
             {'currency_id': 3, 'date': datetime.date(2023, 1, 2)}
        ]

        self.assertListEqual(
            inserted_data, expected_data,
            "Couldn't fetch from API, I recommend to check its status on https://status.vatcomply.com/"
        )

    def test_double_fetch(self):
        """
        Checks if data won't be duplicated in database if multiple requests occur.
        Depends on external API!
        """
        currencies_codes = list(Currencies.objects.values_list('code', flat=True))
        fetch_serv = FetchDataService(currencies_codes)

        # First Request
        new_data = fetch_serv.get_currency_rates([datetime.date(2023, 1, 2)])
        fetch_serv.insert_currency_rates(new_data)

        # Second Request
        new_data = fetch_serv.get_currency_rates([datetime.date(2023, 1, 2)])
        fetch_serv.insert_currency_rates(new_data)

        expected_record_length = 3
        inserted_data_length = len(RatesBaseDollar.objects.all())

        self.assertEqual(expected_record_length, inserted_data_length)


class TestFetchDataExistingRates(TestCase):
    fixtures = ['currencies.json', 'rates_base_dollar.json']

    def test_fetch_from_index_call(self):
        """
        Test if Service fetches correctly when an Index call has missing data.
        In this example, 4 new Records are fetches for currency=2
        Depends on external API!
        """
        existing_length = len(RatesBaseDollar.objects.all())
        expected_new_length = existing_length + 4

        self.client.get(
            reverse('index'), data={'currency': 2, 'date_range': '01/06/2023 - 01/12/2023'}
        )
        self.assertEqual(len(RatesBaseDollar.objects.all()), expected_new_length)
