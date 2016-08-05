from django import forms
from .models import Instance
from actio_control.users.models import User

from .lib.sugarcrm_api_py.SugarCRMAPI import SugarCRMAPI 

class SignUpForm(forms.Form):
    instance_url = forms.URLField(label='You instance URL', max_length=100)
    client_id = forms.CharField(label='OAuth Client ID', max_length=100)
    client_secret = forms.CharField(label='OAuth Client Secret', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)

    def login_sugar(self):
        self.sugar_api = SugarCRMAPI(
            self.cleaned_data['instance_url'], 
            self.cleaned_data['client_id'], 
            self.cleaned_data['client_secret']
        )
        result = self.sugar_api.oauth2_token(
            self.cleaned_data['username'], 
            self.cleaned_data['password']
        )
        return result

    def get_me(self):
        result = self.sugar_api.call('get', 'me')
        return result

    def create_instance(self):
        try:
            instance = Instance.objects.get(url=self.cleaned_data['instance_url'])
        except Instance.DoesNotExist:
            instance = Instance(
                url = self.cleaned_data['instance_url'], 
                client_id = self.cleaned_data['client_id'], 
                client_secret = self.cleaned_data['client_secret']
            )
            instance.save()
        return instance

    def create_user(self, tokens, me, instance):
        try:
            user = User.objects.get(instance__url=self.cleaned_data['instance_url'], sugar_id=me['current_user']['id'])
        except User.DoesNotExist:
            user = User(
                sugar_username = self.cleaned_data['username'],
                sugar_id = me['current_user']['id'],
                access_token = tokens['response_dic']['access_token'],
                refresh_token = tokens['response_dic']['refresh_token'],
                instance = instance,
                sugar_type='admin'
            )
        user.save()

class SignInForm(forms.Form):
    instance_url = forms.URLField(label='You instance URL', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)

    def login(self):
        instance = Instance.objects.get(url=self.cleaned_data['instance_url'])
        user = User.objects.get(instance=instance, sugar_username=self.cleaned_data['username'])

        self.sugar_api = SugarCRMAPI(
            instance.url, 
            instance.client_id, 
            instance.client_secret
        )

        tokens = self.sugar_api.oauth2_token(
            self.cleaned_data['username'], 
            self.cleaned_data['password']
        )

        if tokens['status_code'] == 200 :
            user.access_token = tokens['response_dic']['access_token'] 
            user.refresh_token = tokens['response_dic']['refresh_token']
            user.save()

        return tokens







