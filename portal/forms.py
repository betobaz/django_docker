from django import forms
from .lib.sugarcrm_api_py.SugarCRMAPI import SugarCRMAPI 

class SignUpForm(forms.Form):
    instance_url = forms.URLField(label='You instance URL', max_length=100)
    client_id = forms.CharField(label='OAuth Client ID', max_length=100)
    client_secret = forms.CharField(label='OAuth Client Secret', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)

    def login_sugar(self):
        self.sugarApi = SugarCRMAPI(
            self.cleaned_data['instance_url'], 
            self.cleaned_data['client_id'], 
            self.cleaned_data['client_secret']
        )
        result = self.sugarApi.oauth2_token(
            self.cleaned_data['username'], 
            self.cleaned_data['password']
        )
        return result

    def me(self):
        result = self.sugarApi.call('get', 'me')
        return result