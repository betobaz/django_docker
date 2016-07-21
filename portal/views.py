from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView

from .forms import SignUpForm
from .models import Instance
from actio_control.users.models import User
from .lib.sugarcrm_api_py.SugarCRMAPI import SugarCRMAPI 

class SignupView(TemplateView):
    template_name = "portal/signup.html"
    form_class = SignUpForm
    success_url = '/portal/signup-success/'

    def form_valid(self, form):
        result = form.login_sugar()
        if result['status_code'] == 200:
            result['current_user'] = form.me()['current_user']
        return result

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            result = self.form_valid(form)
            if result['status_code'] == 200: 
                instance = Instance(
                    url = form.cleaned_data['instance_url'], 
                    client_id = form.cleaned_data['client_id'], 
                    client_secret = form.cleaned_data['client_secret']
                )
                instance.save()
                user = User(
                    sugar_username = form.cleaned_data['username'],
                    sugar_id = result['current_user']['id'],
                    access_token = result['response_dic']['access_token'],
                    refresh_token = result['response_dic']['refresh_token'],
                )
                user.save()
                return HttpResponseRedirect('/portal/signup-success/')
            else:
                error = "No Responde sugar :("
        return render(request, 'portal/signup.html', {'form': form, 'error': error})


def get_singup_success(request):
    return render(request, 'portal/signup-success.html', {})