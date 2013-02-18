from django import forms

class SignupForm(forms.Form):
    email = forms.EmailField()
    timezone = forms.CharField()
    #invite_code = forms.CharField(widget=forms.HiddenInput())
