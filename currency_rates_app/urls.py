from django.urls import path
from currency_rates_app.views import CurrenciesApiView, RatesApiView

urlpatterns = [
    path('currencies', CurrenciesApiView.as_view()),
    path('rates', RatesApiView.as_view()),
]
