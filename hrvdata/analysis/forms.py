from django import forms
from django.core.exceptions import ValidationError

DETREND_CHOICES = ((0, "Linear"), (1, "Quadratic"), (2, "Cubic"), (0, "None"),)
FILTER_CHOICES = ((0, "None"), (1, "Quotient"), (2, "Moving Median"),
        (3, "Moving Average"),)

class TachogramSettingsForm(forms.Form):
    detrend_method = forms.ChoiceField(choices=DETREND_CHOICES)
    filter_method = forms.ChoiceField(choices=FILTER_CHOICES)
    filter_order = forms.IntegerField(min_value=3, initial=3)

