from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import SignUpForm
from .lib.sugarcrm_api_py.SugarCRMAPI import SugarCRMAPI 
import pdb


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
            sugarApi.oauth2_token(
                form.cleaned_data['username'], 
                form.cleaned_data['password']
            )
            pdb.set_trace()

            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SignUpForm()

    return render(request, 'portal/signup.html', {'form': form})