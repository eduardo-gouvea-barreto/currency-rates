from django.apps import AppConfig


class CurrencyRatesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'currency_rates_app'

    def ready(self):
        from currency_rates_app import updater
        updater.start()
