# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from instances.models import Instance


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    sugar_username = models.CharField(_('Sugar Username'), blank=True, max_length=255)
    sugar_id = models.CharField(_('Sugar ID'), blank=True, max_length=255)
    access_token = models.CharField(_('Sugar Access Token'), blank=True, max_length=255)
    refresh_token = models.CharField(_('Sugar Refresh Token'), blank=True, max_length=255)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    uuid = models.CharField(_('External ID'), max_length=64, default=uuid.uuid1())

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
