from django import forms
from bootstrap_daterangepicker import widgets, fields

from currency_rates.settings import DEFAULT_CURRENCY_CODE, MAX_ENTRIES
from currency_rates_app.models import Currencies
from currency_rates_app.services.date_service import build_workdays_list


class ChartForm(forms.Form):
    currency = forms.ModelChoiceField(queryset=Currencies.objects.all(),
                                      initial=Currencies.objects.get(code=DEFAULT_CURRENCY_CODE), required=True)
    date_range = fields.DateRangeField(input_formats=['%m/%d/%Y'],
                                 widget=widgets.DateRangeWidget(format='%m/%d/%Y', picker_options={
                                     'locale': {'autoUpdateInput': False, 'format': 'MM/DD/YYYY'}}), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_date_range(self):
        data_min, data_max = self.cleaned_data['date_range']
        workdays_list = build_workdays_list(data_min, data_max)
        if len(workdays_list) > MAX_ENTRIES:
            self.add_error('date_range', f'The date range must consist of {MAX_ENTRIES} workdays at most.')
        return data_min, data_max
