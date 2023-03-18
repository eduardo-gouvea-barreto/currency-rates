import datetime
import json
import requests
from typing import List, Dict

from currency_rates_app.services.date_service import build_workdays_list


class FetchDataService:
    """
    Class that handles all requests between server and the public Currency Rate API.
    """

    def __init__(self, currencies_codes_list: List[str]):
        self._main_url = "https://api.vatcomply.com/rates"
        self._base_currency = 'USD'

        self.currencies_codes_list = currencies_codes_list

    @property
    def main_url(self):
        return self._main_url

    @property
    def base_currency(self):
        return self._base_currency

    def get_currency_rates(self, date_start: datetime.date, date_end: datetime.date) -> List[Dict]:
        """
        Method that gets currency rates from class's currency lists, given a date range.
        It returns a list of dicts with the desired information.

        Example:
                >>> fetch_serv = FetchDataService(['BRL', 'EUR', 'JPY'])
                >>> data = fetch_serv.get_currency_rates(datetime.date(2020, 1, 3), datetime.date(2020, 1, 3))
                >>> print(data)
                [
                    {'date': datetime.date(2020, 1, 3), 'currency_code': 'BRL', 'rate': 4.061272091145599},
                    {'date': datetime.date(2020, 1, 3), 'currency_code': 'EUR', 'rate': 0.8971023593792051},
                    {'date': datetime.date(2020, 1, 3), 'currency_code': 'JPY', 'rate': 108.13671839956939}
                ]
        """

        list_currency_rates = []

        dates_list = build_workdays_list(date_start, date_end)

        for date in dates_list:
            parameters = {
                'base': self.base_currency,
                'date': date
            }

            response = requests.get(self.main_url, parameters)

            if response.status_code == 200:
                content = json.loads(response.content)

                api_date = content['date']
                if api_date == date.strftime('%Y-%m-%d'):
                    rates = content['rates']

                    for currency_code in self.currencies_codes_list:
                        if currency_code in rates.keys():
                            dict_currency_date = {
                                'date': date,
                                'currency_code': currency_code,
                                'rate': rates[currency_code]
                            }

                            list_currency_rates.append(dict_currency_date)

        return list_currency_rates
