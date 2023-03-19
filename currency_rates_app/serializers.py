from rest_framework import serializers
from currency_rates_app.models import Currencies, RatesBaseDollar


class CurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = ["name", "code", "symbol"]


class RatesSerializer(serializers.ModelSerializer):
    currency_code = serializers.CharField(source='currency.code')

    class Meta:
        model = RatesBaseDollar
        fields = ["currency_code", "date", "rate"]
