import datetime
from django.test import TestCase

from currency_rates_app.models import Currencies
from currency_rates_app.forms.graph_form import GraphForm


class TestGraphForm(TestCase):
    fixtures = ['currencies.json']

    def test_form_valid(self):
        """
        Simple case of a valid form
        """
        inputs = {'currency': 1, 'date_range': '01/02/2023 - 01/06/2023'}
        form = GraphForm(inputs)

        self.assertTrue(form.is_valid())

        expected_cleaned_data = {
            'currency': Currencies.objects.get(pk=1),
            'date_range': (datetime.date(2023, 1, 2), datetime.date(2023, 1, 6))
        }

        self.assertDictEqual(form.cleaned_data, expected_cleaned_data)

    def test_form_error_currency(self):
        """
        Tests if form returns error for invalid currency
        """
        inputs = {'currency': 999, 'date_range': '01/02/2023 - 01/06/2023'}
        form = GraphForm(inputs)

        self.assertFalse(form.is_valid())

        field_error_list = ['currency']

        self.assertListEqual(list(form.errors.keys()), field_error_list)

    def test_form_error_date(self):
        """
        Tests if form returns error for invalid date
        """
        inputs = {'currency': 1, 'date_range': 'AAA'}
        form = GraphForm(inputs)

        self.assertFalse(form.is_valid())

        field_error_list = ['date_range']

        self.assertListEqual(list(form.errors.keys()), field_error_list)

    def test_form_error_date_range_greater_than_max_entries(self):
        """
        Tests if form returns error when user requests a date range greater than the max entries number.
        """
        inputs = {'currency': 1, 'date_range': '01/04/1999 - 01/06/2023'}
        form = GraphForm(inputs)

        self.assertFalse(form.is_valid())

        field_error_list = ['date_range']

        self.assertListEqual(list(form.errors.keys()), field_error_list)

    def test_form_error_date_range_in_the_future(self):
        """
        Tests if form returns error when user requests a date in the future.
        """
        inputs = {'currency': 1, 'date_range': '01/04/3000 - 01/06/3000'}
        form = GraphForm(inputs)

        self.assertFalse(form.is_valid())

        field_error_list = ['date_range']

        self.assertListEqual(list(form.errors.keys()), field_error_list)
