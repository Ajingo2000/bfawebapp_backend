from django import forms

class SubscriptionForm(forms.Form):
    email = forms.EmailField(label='Email')
