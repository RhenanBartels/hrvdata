from django import forms
from django.core.exceptions import ValidationError

import hrv

class FileForm(forms.Form):
    rri_data = forms.FileField()
    #TODO: make better validation
    def clean_rri_data(self):
        rri_data = self.cleaned_data['rri_data']
        if not rri_data.name.endswith(".txt") and not rri_data.name.endswith(".hrm"):
            raise ValidationError("Sorry, only text and polar files are accepted.")
        else:
            try:
                rri_to_validate = read_rri_from_django(rri_data)
            except ValueError:
                raise ValidationError("Sorry, we did not understand you file.")
            #TODO: dont know why this validation is here down.
            hrv._validate_rri(rri_to_validate)
        return rri_data

def read_rri_from_django(signal):
    if signal.name.endswith(".txt"):
        rri_to_validate = [float(value.strip()) for value in
                signal.readlines() if value.strip()]
    else:
        import re
        file_content = signal.readlines()
        file_content = ''.join(file_content)
        rri_to_validate = [float(value.strip()) for value in
                re.findall("\d{3,4}\\r\\n", file_content)]
    return rri_to_validate
