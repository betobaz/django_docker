from django import forms

class SignUpForm(forms.Form):
    instance_url = forms.URLField(label='You instance URL', max_length=100)
    client_id = forms.CharField(label='OAuth Client ID', max_length=100)
    client_secret = forms.CharField(label='OAuth Client Secret', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)

