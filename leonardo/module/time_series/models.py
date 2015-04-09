# -*- coding:/ utf-8 -*-

import datetime
from math import floor
from time import time

import requests
from django.db import models
from django.utils.translation import ugettext_lazy as _
from hrcms.module.boardie.models import WidgetMixin
from yamlfield.fields import YAMLField

SOURCE_TYPES = (
    ('graphite', _('Graphite')),
)

TIME_UNITS = (
    ('second', _('seconds')), 
    ('minute', _('minutes')), 
    ('hour', _('hours')),
    ('day', _('days')), 
)

STEP_FUNS = (
    ('sum', _('sum')), 
    ('avg', _('average')), 
    ('min', _('minimum')),
    ('max', _('maximum')), 
)

class TimeSeriesSource(models.Model):
    type  = models.CharField(max_length=255, verbose_name=_("type"), default='graphite', choices=SOURCE_TYPES)
    name = models.CharField(max_length=255, verbose_name=_("name"))
    data = YAMLField(verbose_name=_("data"), help_text=_('For graphite set: host, port, ssl, user, passwd'))

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _("time-series source")
        verbose_name_plural = _("time-series sources")

class TimeSeriesWidgetMixin(WidgetMixin):
    """
    Time-series widget mixin.
    """
    time_series_source = models.ForeignKey(TimeSeriesSource, verbose_name=_('data source'), blank=True, null=True)
    metrics = models.TextField(verbose_name=_('metrics'), blank=True)
    step_length = models.IntegerField(verbose_name=_('step length'), default=1)
    step_unit = models.CharField(max_length=55, verbose_name=_('step unit'), choices=TIME_UNITS, default="minute")
    step_fun = models.CharField(max_length=55, verbose_name=_('step function'), choices=STEP_FUNS, default="avg")
    start = models.DateTimeField(verbose_name=_('start time'), blank=True, null=True)
    duration_length = models.IntegerField(verbose_name=_('duration length'), default=2)
    duration_unit = models.CharField(max_length=55, verbose_name=_('duration unit'), choices=TIME_UNITS, default="hour")
    low_horizon = models.IntegerField(verbose_name=_('low horizon'), blank=True, null=True)
    high_horizon = models.IntegerField(verbose_name=_('high horizon'), blank=True, null=True)

    @property
    def source(self):
        return self.time_series_source

    def get_host(self):
        if self.source.type == 'graphite':
            if self.source.data['ssl']:
                protocol = 'https'
            else:
                protocol = 'http'
            return '%s://%s:%s' % (protocol, self.source.data['host'], self.source.data['port'])

    def relative_start(self):
        if self.start:
            return self.start
        else:
            now = datetime.datetime.now()
            return now - self.get_duration_delta()

    def get_duration_delta(self):
        delta = None
        if self.duration_unit == 'day':
            delta = datetime.timedelta(days=self.duration_length)
        if self.duration_unit == 'hour':
            delta = datetime.timedelta(hours=self.duration_length)
        if self.duration_unit == 'minute':
            delta = datetime.timedelta(minutes=self.duration_length)
        if self.duration_unit == 'second':
            delta = datetime.timedelta(seconds=self.duration_length)
        return delta 

    def get_step_delta(self):
        delta = None
        if self.step_unit == 'day':
            delta = datetime.timedelta(days=self.step_length)
        if self.step_unit == 'hour':
            delta = datetime.timedelta(hours=self.step_length)
        if self.step_unit == 'minute':
            delta = datetime.timedelta(minutes=self.step_length)
        if self.step_unit == 'second':
            delta = datetime.timedelta(seconds=self.step_length)
        return delta

    def get_step_label(self):
        if self.step_unit == 'day':
            return 'd'
        if self.step_unit == 'hour':
            return 'h'
        if self.step_unit == 'minute':
            return 'm'
        if self.step_unit == 'second':
            return 's'
        return '?'

    def get_metrics(self):
        metrics = self.metrics.split("\n")
        ret = []
        for metric in metrics:
            if metric.strip('\n').strip('\r') != '':
                line = metric.strip('\n').strip('\r').split('|')
                final_line = {
                    'target': line[2],
                    'unit': line[1],
                    'name': line[0]
                }
                if len(line) > 5:
                    final_line['type'] = line[3]
                    final_line['x'] = line[4]
                    final_line['y'] = line[5]
                ret.append(final_line)
        return ret

    def get_graphite_data(self):
        url = "%s/render" % self.get_host()
        target = 'summarize(%s, "%s%s", "%s")' % (self.get_metrics()[0]["target"], str(self.get_step_delta().total_seconds()).rstrip('.0'), self.step_unit, self.step_fun)
        start = str(floor(time() - self.get_step_delta().total_seconds())).rstrip('.0')        
        params = {
            "format": "raw",
            "from": start,
            "target": target,
        }
        request = requests.get(url, params=params)
        return request.text

    def get_graphite_last_value(self):
        url = "%s/render" % self.get_host()
        target = 'summarize(%s, "%s%s", "%s")' % (self.get_metrics()[0]["target"], self.step_length, self.step_unit, self.step_fun)
        start = str(floor(time() - (self.get_step_delta().total_seconds()*1))).rstrip('.0')
        
        params = {
            "format": "raw",
            "from": start,
            "target": target,
        }
        request = requests.get(url, params=params)
        try:
            response = {
                "value": float(request.text.split("|")[-1].split(",")[-2]),
                "unit": self.get_metrics()[0]["unit"]
            }
        except: 
            response = None    
        return response

    def get_graphite_last_values(self):

        url = "%s/render" % self.get_host()
        start = str(floor(time() - (self.get_step_delta().total_seconds()*2))).rstrip('.0')
        response = []
        i = 1

        for metric in self.get_metrics():
            target = 'summarize(%s, "%s%s", "%s")' % (metric["target"], self.step_length, self.step_unit, self.step_fun)

            params = {
                "format": "raw",
                "from": start,
                "target": target,
            }


            request = requests.get(url, params=params)

            try:
                value = float(request.text.split("|")[-1].split(",")[-1])
            except:
                try:
                    value = float(request.text.split("|")[-1].split(",")[-2])
                except:
                    try:
                        value = float(request.text.split("|")[-1].split(",")[-3])
                    except:
                        value = None

            response.append({
                "value": value,
                "unit": metric["unit"],
                "name": metric["name"],
                "type": metric.get("type", None),
                "x": metric.get("x", None),
                "y": metric.get("y", None),
                "device": i
            })

            i += 1

        return response

    def get_graphite_values(self):

        url = "%s/render" % self.get_host()
        start = str(floor(time() - (self.get_duration_delta().total_seconds()))).rstrip('.0')
        response = []
        i = 1

        for metric in self.get_metrics():
            target = 'summarize(%s, "%s%s", "%s")' % (metric["target"], self.step_length, self.step_unit, self.step_fun)

            params = {
                "format": "json",
                "from": start,
                "target": target,
            }

            request = requests.get(url, params=params)

            #values = request.text.split("|")[-1].split(",")

            response.append({
                "values": request.json()[0]['datapoints'],
                "unit": metric["unit"],
                "name": metric["name"],
                "type": metric.get("type", None),
                "x": metric.get("x", None),
                "y": metric.get("y", None)
            })

            i += 1

        return response

    class Meta:
        abstract = True
