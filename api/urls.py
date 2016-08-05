# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
	# URL pattern for the UserListView
    url(
        regex=r'^holamundo/$',
        view=views.TestView.as_view(),
        name='holamundo'
    ),
    url(
        regex=r'^login/$',
        view=views.LoginView.as_view(),
        name='login'
    ),
    url(
        regex=r'^search/$',
        view=views.SearchView.as_view(),
        name='search'
    ),
]