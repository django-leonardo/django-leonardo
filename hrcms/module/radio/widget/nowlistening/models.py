# -#- coding: utf-8 -#-

import datetime

from decimal import Decimal

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.utils.safestring import mark_safe

from webcms.utils.models import JSONField
from webcms.models import Widget

from BeautifulSoup import BeautifulStoneSoup

from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson as json

import math
import random

import urllib
import urllib2

class NowListeningWidget(Widget):
    max_items = models.IntegerField(_('max. items'), default=500)
    map_width = models.IntegerField(_('map width'), default=640)
    map_height = models.IntegerField(_('map height'), default=480)
    icecast_listeners_url = models.URLField(_('Icecast listeners URL'), verify_exists=False)
    icecast_admin_auth = models.CharField(_('Icecast authentication'), max_length=255)
    ipinfodb_api_key = models.CharField(_('IPinfoDB API key'), max_length=255)
    cached_data = models.TextField(blank=True, null=True, editable=False)
    last_updated = models.DateTimeField(_('last updated'), blank=True, null=True, editable=False)

    def render_content(self, options):

        regen = False
        if self.last_updated:
            now = datetime.datetime.now()
            delta = now - self.last_updated
            if delta.seconds > 1800:
                regen = True
        else:
            regen = True

     #   if regen:
        self.cache_content(None, True)

        context = RequestContext(options.get('request'), { 
            'widget': self,
            'data': json.loads(self.cached_data),
        })

        return render_to_string(self.template_name, context)

    def cache_content(self, date_format=None, save=True):
        user, passwd = self.icecast_admin_auth.split(':')
        ipdb_key = self.ipinfodb_api_key
        ipdb_url = 'http://api.ipinfodb.com/v3/ip-city/'
        icecast_url = self.icecast_listeners_url

        try:
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None, icecast_url, user, passwd)
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)
            remote_data = urllib2.urlopen(self.icecast_listeners_url)
            data = remote_data.read()

            soup = BeautifulStoneSoup(data)

            parsed_data = []

            listeners = soup.findAll('listener')
            for listener in listeners:
                listn = {
                    'ip': str(listener.contents[0].contents[0]),
                    'agent': str(listener.contents[1].contents[0]),
                    'connected': str(listener.contents[2].contents[0]),
                }

                response = urllib.urlopen('%s?key=%s&ip=%s&timezone=true' % (ipdb_url, ipdb_key, listn['ip']))
                attrs = response.read().split(';')
                axis_y = math.floor((90 - float(attrs[9])) / 180 * self.map_height) + random.randint(-2, 2) + 7
                if axis_y < 0:
                    axis_y += self.map_height

                if attrs[0] == 'OK':
                    listn['lat'] = str(attrs[8])
                    listn['long'] = str(attrs[9])
                    listn['axis_x'] = math.floor((float(attrs[8]) + 90) / 180 * self.map_width) + random.randint(-2, 2) - 20
                    listn['axis_y'] = axis_y

                parsed_data.append(listn)

            self.cached_data = json.dumps(parsed_data, cls=DjangoJSONEncoder)
            self.last_updated = datetime.datetime.now()

            if save:
                self.save()
        except:
            pass

    def save(self, *args, **kwargs):
        self.cache_content(None, False)
        super(NowListeningWidget, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        verbose_name = _("now listening")
        verbose_name_plural = _('now listening')
