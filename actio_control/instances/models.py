# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models

@python_2_unicode_compatible
class Instance(models.Model):

    url = models.UrlField(_('Sugar Url'), blank=True, max_length=255)
    client_id = models.CharField(_('Client ID'), blank=True, max_length=255)
    client_secret = models.CharField(_('Client Secret'), blank=True, max_length=255)
    uuid = models.CharField(_('External ID'), max_length=64, default=uuid.uuid1())

    def __str__(self):
        return self.url

