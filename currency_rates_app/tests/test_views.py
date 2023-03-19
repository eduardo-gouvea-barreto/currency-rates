import bs4
from django.test import TestCase
from django.urls import reverse

from currency_rates_app.models import Currencies


class TestRenderViews(TestCase):
    fixtures = ['currencies.json']

    def test_status_index(self):
        """
        Checks if Index returns status code 200
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_status_api_currencies(self):
        """
        Checks if GET Currencies returns status code 200
        """
        response = self.client.get(reverse('currencies'))
        self.assertEqual(response.status_code, 200)

    def test_status_api_rates(self):
        """
        Checks if GET Rates returns status code 200
        """
        response = self.client.get(reverse('rates'))
        self.assertEqual(response.status_code, 200)


class TestViewsContents(TestCase):
    fixtures = ['currencies.json', 'rates_base_dollar.json']

    def test_index_content(self):
        """
        Checks if Dates and Rates are in HTML
        """
        response = self.client.get(reverse('index'))
        content = response.content.decode('utf-8')
        self.assertIn("rates = [5.3401, 5.3728, 5.4494, 5.3825, 5.3366]", content)
        self.assertIn("dates = ['01/02/2023', '01/03/2023', '01/04/2023', '01/05/2023', '01/06/2023']", content)

    def test_api_currencies_response(self):
        """
        Checks if simple API call (currencies) returns correctly
        """
        response = self.client.get(reverse('currencies'))
        content = response.json()
        expected_response = [
            {'name': 'Brazilian real', 'code': 'BRL', 'symbol': 'R$'},
            {'name': 'Euro', 'code': 'EUR', 'symbol': '€'},
            {'name': 'Japanese yen', 'code': 'JPY', 'symbol': '¥'}
        ]
        self.assertListEqual(content, expected_response)

    def test_api_rates_response(self):
        """
        Checks if simple API call (rates) returns correctly
        """
        parameters = {'currency_code': 'EUR', 'date_min': '2023-01-03', 'date_max': '2023-01-05'}
        response = self.client.get(reverse('rates'), data=parameters)
        content = response.json()
        expected_response = [
            {'currency_code': 'EUR', 'date': '2023-01-05', 'rate': '0.9433'},
            {'currency_code': 'EUR', 'date': '2023-01-04', 'rate': '0.9435'},
            {'currency_code': 'EUR', 'date': '2023-01-03', 'rate': '0.9483'}
        ]
        self.assertListEqual(content, expected_response)

    def test_index_form_error_currency(self):
        """
        Passes invalid parameters (currency = 999) and checks if error rendered correctly
        """
        response = self.client.get(reverse('index'), data={'currency': 999, 'date_range': '01/02/2023 - 01/06/2023'})
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        error_tags = soup.find_all('ul', {'class': 'errorlist'})
        for error in error_tags:
            select_with_error = error.find_parent('div').find_all('select')[0].get('name')
            self.assertEqual(select_with_error, 'currency')

    def test_index_form_error_date_range(self):
        """
        Passes invalid parameters (date_range = '01/02/2100 - 01/06/2100') and checks if error rendered correctly
        """
        response = self.client.get(reverse('index'), data={'currency': 1, 'date_range': '01/02/2100 - 01/06/2100'})
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        error_tags = soup.find_all('ul', {'class': 'errorlist'})
        for error in error_tags:
            select_with_error = error.find_parent('div').find_all('input')[0].get('name')
            self.assertEqual(select_with_error, 'date_range')

    def test_api_rates_error_currency(self):
        """
        Passes invalid parameters (currency_code = 'AAA') and checks json response
        """
        response = self.client.get(reverse('rates'), data={'currency_code': 'AAA'})
        self.assertEqual(response.status_code, 400)

        content = response.json()
        self.assertDictEqual(content, {'currency_code': 'Invalid currency_code'})

    def test_api_rates_error_date_min(self):
        """
        Passes invalid parameters (date_min = '111-111-111') and checks json response
        """
        response = self.client.get(reverse('rates'), data={'date_min': '111-111-111'})
        self.assertEqual(response.status_code, 400)

        content = response.json()
        self.assertDictEqual(content, {'date_min': 'Invalid date_min'})

    def test_api_rates_error_date_max(self):
        """
        Passes invalid parameters (date_max = '111-111-111') and checks json response
        """
        response = self.client.get(reverse('rates'), data={'date_max': '111-111-111'})
        self.assertEqual(response.status_code, 400)

        content = response.json()
        self.assertDictEqual(content, {'date_max': 'Invalid date_max'})

    def test_index_when_api_fails_to_find_data(self):
        """
        When called by index, the Fetch Service will only send a request to the API once.
        If it fails to find, it must show the user an error message.
        """
        fake_currency = Currencies(**{'name': 'Fake Currency', 'code': 'XXX', 'symbol': 'XXX'})
        fake_currency.save()

        response = self.client.get(
            reverse('index'), data={'currency': fake_currency.id, 'date_range': '01/06/2023 - 01/12/2023'}
        )
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        error_message = soup.find('div', {'class': 'alert-danger'}).text

        expected_error_message = (
            'Unable to fetch data from dates: 01/06/2023, 01/09/2023, 01/10/2023, 01/11/2023, 01/12/2023'
        )

        self.assertEqual(error_message, expected_error_message)
