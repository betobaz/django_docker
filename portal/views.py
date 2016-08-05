from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.views.generic import FormView

from django.contrib.auth import login, authenticate, logout

from .forms import (
    SignUpForm,
    SignInForm
)
from .models import Instance
from actio_control.users.models import User
from .lib.sugarcrm_api_py.SugarCRMAPI import SugarCRMAPI 

class SignupView(FormView):
    template_name="portal/signup.html"
    form_class=SignUpForm
    success_url='/portal/signup-success/'

    def form_valid(self, form):
        tokens = form.login_sugar()
        if tokens['status_code'] == 200:
            instance = form.create_instance()
            me = form.get_me()
            if me['current_user']:
                form.create_user(tokens, me, instance)
                return True
        return False

    def post(self, request):
        error = ""
        form = self.form_class(request.POST)
        if form.is_valid():
            result = self.form_valid(form)
            if result: 
                return HttpResponseRedirect('/portal/signup-success/')
            else:
                error = "No Responde sugar :("
        return render(request, 'portal/signup.html', {'form': form, 'error': error})

class SigninView(FormView):
    template_name="portal/signin.html"
    form_class=SignInForm

    def post(self, request):
        form = self.form_class(request.POST)
        error = ""
        if form.is_valid():
            user = authenticate(url=form.cleaned_data['instance_url'], username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/') 
            else:
                error = "No encuentro el usuario"
        else:
            error = "Credenciales invalidas"
        return render(request, 'portal/signin.html', {'form': form, 'error':error})

def get_singup_success(request):
    return render(request, 'portal/signup-success.html', {})