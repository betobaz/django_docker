# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
import uuid
from portal.models import Instance
from model_utils import Choices



@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    SUGAR_TYPES = Choices('normal', 'admin')
    
    # id = models.AutoField(primary_key=True)
    name = models.CharField(_('Name'), blank=True, max_length=255)
    sugar_username = models.CharField(_('Sugar Username'), blank=True, max_length=255)
    sugar_id = models.CharField(_('Sugar ID'), blank=True, max_length=255)
    access_token = models.CharField(_('Sugar Access Token'), blank=True, max_length=255)
    refresh_token = models.CharField(_('Sugar Refresh Token'), blank=True, max_length=255)
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, blank=True, null=True)
    sugar_type = models.CharField(_('Sugar Type User'), choices=SUGAR_TYPES, default=SUGAR_TYPES.normal, max_length=10)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
