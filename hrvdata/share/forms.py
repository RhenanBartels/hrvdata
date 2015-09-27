from django import forms
from django.core.exceptions import ValidationError

class ShareForm(forms.Form):
    receiver_email = forms.EmailField(label=(u''),
            widget=forms.TextInput(attrs={'placeholder': 'name@example.com'}))

    def clean_usermail(self):
        receiver_email = self.cleaned_data['receiver_email']
        if not receiver_email:
            raise ValidationError("Please inform an email address")
        return receiver_email
