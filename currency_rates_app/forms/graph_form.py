import datetime
from django import forms
from bootstrap_daterangepicker import widgets, fields

from currency_rates.settings import (
    DEFAULT_CURRENCY_CODE, MAX_ENTRIES, FIRST_AVAILABLE_DATE, DEFAULT_DATE_FORMAT, DEFAULT_DATE_FORMAT_WIDGET_INPUT
)
from currency_rates_app.models import Currencies
from currency_rates_app.services.date_service import build_workdays_list


class GraphForm(forms.Form):
    currency = forms.ModelChoiceField(queryset=Currencies.objects.all(),
                                      initial=Currencies.objects.get(code=DEFAULT_CURRENCY_CODE), required=True)
    date_range = fields.DateRangeField(input_formats=[DEFAULT_DATE_FORMAT],
                                       widget=widgets.DateRangeWidget(format=DEFAULT_DATE_FORMAT, picker_options={
                                           'locale': {'autoUpdateInput': False,
                                                      'format': DEFAULT_DATE_FORMAT_WIDGET_INPUT}}), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_date_range(self):
        """
        Custom clean method for date_range.
        """
        data_min, data_max = self.cleaned_data['date_range']
        workdays_list = build_workdays_list(data_min, data_max)

        if len(workdays_list) > MAX_ENTRIES:
            self.add_error('date_range', f'The date range must consist of {MAX_ENTRIES} workdays at most.')

        if data_min > datetime.date.today() or data_max > datetime.date.today():
            max_allowed_date = datetime.date.today().strftime(DEFAULT_DATE_FORMAT)
            self.add_error('date_range', f'The max. allowed date is the current date ({max_allowed_date})')

        if data_min < datetime.date(*FIRST_AVAILABLE_DATE) or data_max < datetime.date(*FIRST_AVAILABLE_DATE):
            min_allowed_date = datetime.date(*FIRST_AVAILABLE_DATE).strftime(DEFAULT_DATE_FORMAT)
            self.add_error('date_range', f'The min. allowed date is {min_allowed_date}')

        return data_min, data_max
