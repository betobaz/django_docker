# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid

@python_2_unicode_compatible
class Instance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(_('Sugar Url'), blank=True, max_length=255)
    client_id = models.CharField(_('Client ID'), blank=True, max_length=255)
    client_secret = models.CharField(_('Client Secret'), blank=True, max_length=255)

    def __str__(self):
        return self.url

