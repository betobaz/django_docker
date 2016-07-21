from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView

from .forms import SignUpForm
from .lib.sugarcrm_api_py.SugarCRMAPI import SugarCRMAPI 
import pdb

class SignupView(TemplateView):
    template_name = "portal/signup.html"

def get_singup(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignUpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            sugarApi = SugarCRMAPI(
                form.cleaned_data['instance_url'], 
                form.cleaned_data['client_id'], 
                form.cleaned_data['client_secret']
            )
            pdb.set_trace()
            result = sugarApi.oauth2_token(
                form.cleaned_data['username'], 
                form.cleaned_data['password']
            )
            if result['status_code'] == 200: 
                return HttpResponseRedirect('/portal/signup-success/')
            else:
                return HttpResponseRedirect('/portal/signup-error/')
            
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignUpForm()

    return render(request, 'portal/signup.html', {'form': form})

def get_singup_success(request):
    return render(request, 'portal/signup-success.html', {})

def get_singup_error(request):
    return render(request, 'portal/signup-error.html', {})