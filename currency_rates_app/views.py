from django.shortcuts import render

from currency_rates.settings import DEFAULT_CURRENCY_CODE, MAX_ENTRIES
from currency_rates_app.models import Currencies, RatesBaseDollar
from currency_rates_app.forms.chart_form import ChartForm


def index(request):
    if request.method == 'GET':
        if len(request.GET) > 0:
            form = ChartForm(data=request.GET)
            if form.is_valid():
                currency = form.cleaned_data['currency']
                date_min, date_max = form.cleaned_data['date_range']

                currency_rates = RatesBaseDollar.objects.filter(
                    currency=currency,
                    date__gte=date_min,
                    date__lte=date_max
                ).order_by('date').values('date', 'rate')

                dates = [date.strftime("%m/%d/%Y") for date in currency_rates.values_list('date', flat=True)]
                rates = [float(rate) for rate in currency_rates.values_list('rate', flat=True)]
            else:
                currency = Currencies(**{'name': '', 'code': '', 'symbol': ''})
                dates = []
                rates = []
        else:
            currency = Currencies.objects.get(code=DEFAULT_CURRENCY_CODE)

            currency_rates = RatesBaseDollar.objects.filter(
                currency__name=currency.name
            ).order_by('-date').values('date', 'rate')[:MAX_ENTRIES]

            dates = [date.strftime("%m/%d/%Y") for date in currency_rates.values_list('date', flat=True)]
            dates.reverse()

            rates = [float(rate) for rate in currency_rates.values_list('rate', flat=True)]
            rates.reverse()

            form = ChartForm(initial={'currency': currency, 'date_range': f'{dates[0]} - {dates[-1]}'})

        context = {
            'currency': currency.name,
            'code': currency.name,
            'dates': dates,
            'rates': rates,
            'form': form,
            'max_entries': MAX_ENTRIES
        }
        return render(request, 'index.html', context=context)
