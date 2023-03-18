from django.db import models
from django.core.validators import MinLengthValidator


class Currencies(models.Model):
    name = models.CharField(unique=True, max_length=50)
    code = models.CharField(unique=True, max_length=3, validators=[MinLengthValidator(3)])
    symbol = models.CharField(unique=True, max_length=3)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'app_currencies'


class RatesBaseDollar(models.Model):
    currency = models.ForeignKey(Currencies, models.DO_NOTHING)
    date = models.DateField()
    rate = models.DecimalField(max_digits=14, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.currency.name} | {self.date} | {self.rate}"

    class Meta:
        db_table = 'app_rates_base_dollar'
