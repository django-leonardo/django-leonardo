# -*- coding: UTF-8 -*-
"""
Business models
"""

import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from sorl.thumbnail.fields import ImageField

ROLE_CHOICES = (
    ('business', _('Business')),
    ('client', _('Client')),
    ('partner', _('Partner')),
)

TYPE_CHOICES = (
    ('person', _('Regular person')),
    ('sole', _('Sole enterpreteur')),
    ('inc', _('Incorporated company')),
    ('joint', _('Joint stock company')),
)


class Entity(models.Model):
    """
    Business entity model.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, default='inc')
    business_id = models.CharField(max_length=255, blank=True, null=True)
    vat_id = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    bank = models.CharField(max_length=255, blank=True)
    bank_account = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True, null=True)
    core = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('entity')
        verbose_name_plural = _('entities')
        ordering = ['name',]


class CorporateIdentity(models.Model):
    """
    Business corporate model.
    """
    entity = models.ForeignKey(Entity, verbose_name=_('business entity'),)
    default = models.BooleanField(default=True)
    logo_bitmap = ImageField(upload_to='company/logo/bitmap', null=True, blank=True)
    logo_vector = models.FileField(upload_to='company/logo/vector', null=True, blank=True)
    sign = ImageField(upload_to='company/signs', null=True, blank=True)
    template_eml = models.TextField(blank=True, null=True)
    template_html = models.TextField(blank=True, null=True)
    template_rml = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.entity.__unicode__()

    class Meta:
        verbose_name = _('corporate identity')
        verbose_name_plural = _('corporate identities')

