from django.contrib import admin
from django import forms

from .models import Instance

# class MyInstanceChangeForm(forms.ModelForm):
#     class Meta:
#         model = Instance

# class InstanceAdmin(Instance):
	# fields = ('url', 'client_id', 'client_secret')

admin.site.register(Instance)
