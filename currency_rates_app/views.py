import datetime

from django.shortcuts import render
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from currency_rates.settings import MAX_ENTRIES
from currency_rates_app.forms.graph_form import GraphForm
from currency_rates_app.services.graph_service import gather_graph_info, build_default_graph
from currency_rates_app.models import Currencies, RatesBaseDollar
from currency_rates_app.serializers import CurrenciesSerializer, RatesSerializer


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


class CurrenciesApiView(APIView):
    def get(self, requests):
        currencies = Currencies.objects.all()
        serializer = CurrenciesSerializer(currencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RatesApiView(APIView):
    def get(self, request):
        rates = RatesBaseDollar.objects.all().order_by('-date', 'currency__code')
        date_min, date_max, currency_code = (
            request.query_params.get('date_min'),
            request.query_params.get('date_max'),
            request.query_params.get('currency_code'),
        )
        errors = {}
        max_records = 1000

        if date_min:
            try:
                date_min = datetime.datetime.strptime(date_min, '%Y-%m-%d').date()
                rates = rates.filter(date__gte=date_min)
            except ValueError:
                errors['date_min'] = 'Invalid date_min'

        if date_max:
            try:
                date_max = datetime.datetime.strptime(date_max, '%Y-%m-%d').date()
                rates = rates.filter(date__lte=date_max)
            except ValueError:
                errors['date_max'] = 'Invalid date_max'

        if currency_code:
            try:
                currency = Currencies.objects.get(code=currency_code)
                rates = rates.filter(currency=currency)
            except ObjectDoesNotExist:
                errors['currency_code'] = 'Invalid currency_code'

        if errors:
            return JsonResponse(errors, status=status.HTTP_400_BAD_REQUEST)

        if not date_min:
            rates = rates[:max_records]

        serializer = RatesSerializer(rates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
