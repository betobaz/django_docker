# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
	# URL pattern for the UserListView
    url(
        regex=r'^signup/$',
        view=views.get_singup,
        name='portal-signup'
    ),
]