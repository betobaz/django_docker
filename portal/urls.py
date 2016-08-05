# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
	# URL pattern for the UserListView
    url(
        regex=r'^signup/$',
        view=views.SignupView.as_view(),
        name='signup'
    ),
    url(
        regex=r'^signin/$',
        view=views.SigninView.as_view(),
        name='login'
    ),
    url(
        regex=r'^signup-success/$',
        view=views.get_singup_success,
        name='signup_success'
    ),
]