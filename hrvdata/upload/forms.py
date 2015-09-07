from django import forms

class FileForm(forms.Form):
    rri_data = forms.FileField()
