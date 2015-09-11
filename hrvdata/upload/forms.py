from django import forms
from django.core.exceptions import ValidationError

import hrv

class FileForm(forms.Form):
    rri_data = forms.FileField()
    #TODO: make better validation
    def clean_rri_data(self):
        rri_data = self.cleaned_data['rri_data']
        if not rri_data.name.endswith(".txt") or rri_data.name.endswith(".hrm"):
            raise ValidationError("Sorry, only text and polar files are accepted.")
        else:
            try:
                rri_to_validate = [float(value.strip()) for value in
                        rri_data.readlines() if value.strip()]
            except ValueError:
                raise ValidationError("Sorry, we did not understand you file.")
            hrv._validate_rri(rri_to_validate)
        return rri_data
