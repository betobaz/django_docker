from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView

from .forms import SignUpForm
from .lib.sugarcrm_api_py.SugarCRMAPI import SugarCRMAPI 

class SignupView(TemplateView):
    template_name = "portal/signup.html"
    form_class = SignUpForm
    success_url = '/portal/signup-success/'

    def form_valid(self, form):
        result = form.login_sugar()
        return result

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            result = self.form_valid(form)
            if result['status_code'] == 200: 
                return HttpResponseRedirect('/portal/signup-success/')
            else:
                error = "No Responde sugar :("
        return render(request, 'portal/signup.html', {'form': form, 'error': error})


def get_singup_success(request):
    return render(request, 'portal/signup-success.html', {})