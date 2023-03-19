from django.shortcuts import render
from django.contrib import messages

from currency_rates.settings import MAX_ENTRIES
from currency_rates_app.forms.graph_form import GraphForm
from currency_rates_app.services.graph_service import gather_graph_info, build_default_graph


def index(request):
    if request.method == 'GET':
        if len(request.GET) > 0:
            form = GraphForm(data=request.GET)
            if form.is_valid():
                currency = form.cleaned_data['currency']
                date_min, date_max = form.cleaned_data['date_range']
                dates, rates, missing_dates = gather_graph_info(currency, date_min, date_max)
                if missing_dates:
                    messages.warning(request, f"Unable to fetch data from dates: {', '.join(missing_dates)}")
            else:
                currency, dates, rates = None, [], []
        else:
            currency, dates, rates = build_default_graph()
            form = GraphForm(initial={'currency': currency, 'date_range': f'{dates[0]} - {dates[-1]}'})

        context = {
            'currency': currency.name if currency is not None else '',
            'code': currency.name if currency is not None else '',
            'dates': dates,
            'rates': rates,
            'form': form,
            'max_entries': MAX_ENTRIES
        }
        return render(request, 'index.html', context=context)
