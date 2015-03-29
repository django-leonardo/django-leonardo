# -#- coding: utf-8 -#-
import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext, Context, loader
from django_extensions.db.fields import json    

import floppyforms as forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Button, Submit, TabHolder, Tab
from crispy_forms.bootstrap import FormActions

from rest_framework import serializers

from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["^yamlfield\.fields\.YAMLField"])
add_introspection_rules([], ["^markupfield\.fields\.MarkupField"])

PAGE_TEMPLATES = ({
    'key': 'dashboard',
    'title': _('Dashboard'),
    'path': 'layout/page.html',
    'regions': (
        ('main', _('Main region')),
        ('preview', _('Preview region')),
    ),
},
{
    'key': 'wiki',
    'title': _('Wiki'),
    'path': 'layout/page.html',
    'regions': (
        ('main', _('Main region')),
        ('preview', _('Preview region')),
    ),
})

PAGE_EXTENSIONS = (
    'feincms.module.extensions.ct_tracker',
    'feincms.module.extensions.translations',
    'feincms.module.extensions.featured',
    'feincms.module.extensions.seo',
    'feincms.module.page.extensions.navigation',
    'feincms.module.page.extensions.titles',
    'feincms.module.page.extensions.sites',
)

WIDGET_WIDTH_CHOICES = (
    (1, _('1 col')),
    (2, _('2 cols')),
    (3, _('3 cols')),
    (4, _('4 cols')),
    (5, _('5 cols')),
    (6, _('6 cols')),
)

WIDGET_HEIGHT_CHOICES = (
    (1, _('1 row')),
    (2, _('2 rows')),
    (3, _('3 rows')),
    (4, _('4 rows')),
    (5, _('5 rows')),
    (6, _('6 rows')),
)

WIDGET_UPDATE_INTERVAL_UNIT_CHOICES = (
    ('second', 'second'), 
    ('minute', 'minute'), 
    ('hour', 'hour'),
    ('day', 'day'), 
)

def timedelta_to_microtime(td):
  return td.seconds + td.days * 86400

class WidgetMixin(models.Model):

    name = models.CharField(max_length=255, verbose_name=_('name'), blank=True)
    kind = models.CharField(max_length=55, verbose_name=_('kind'), editable=False)
    uid = models.CharField(max_length=55, verbose_name=_('uid'), editable=False, blank=True, null=True)
    dashboard_id = models.IntegerField(verbose_name=_('dashboard ID'), editable=False)
    row = models.IntegerField(verbose_name=_('row'), default=1)
    col = models.IntegerField(verbose_name=_('col'), default=1)
    width = models.IntegerField(verbose_name=_('width'), default=1, choices=WIDGET_WIDTH_CHOICES)
    height = models.IntegerField(verbose_name=_('height'), default=1, choices=WIDGET_HEIGHT_CHOICES)
    update_interval_length = models.IntegerField(verbose_name=_('update interval length'), default=60)
    update_interval_unit = models.CharField(max_length=55, verbose_name=_('update interval unit'), default='second', choices=WIDGET_UPDATE_INTERVAL_UNIT_CHOICES)
    update_interval = models.IntegerField(verbose_name=_('update interval seconds'), editable=False, default=60)
    active = models.BooleanField(verbose_name=_('enabled'), default=True)
    overflow = models.CharField(max_length=55, verbose_name=_('overflow'), default="hidden")
    last_update = models.DateTimeField(verbose_name=_('last update'), editable=False)
    cache = json.JSONField(blank=True, null=True, editable=False)

    def save(self, reset_last_update=True):
        if not self.last_update:
            self.init()
        if reset_last_update:
            self.last_update = timezone.now() - self.get_update_interval
        self.update_interval = timedelta_to_microtime(self.get_update_interval)
        if not self.dashboard_id:
            self.dashboard_id = self.parent.id
        if not self.kind:
            self.kind = self.widget_name
        if not self.name:
            self.name = '%s' % self.kind
        if not self.col:
            self.col = 1
        if not self.row:
            self.row = 1
        if not self.width:
            self.width = 1
        if not self.height:
            self.height = 1
        if not self.overflow:
            self.overflow = 'hidden'
        if not self.update_interval:
            self.update_interval = self.get_update_interval.total_seconds()
        super(WidgetMixin, self).save()
        if not self.uid:
            self.uid = self.fe_identifier()
            super(WidgetMixin, self).save()

    class Meta:
        abstract = True
        verbose_name = _("dashboard widget mixin")
        verbose_name_plural = _("dashboard widget mixins")

    def _widget_name(self):
        return self.__class__.__name__.lower().replace('widget', '')
    widget_name = property(_widget_name)

    def _widget_label(self):
        return self._meta.verbose_name
    widget_label = property(_widget_label)

    def get_width(self):
        return self.parent.widget_width * self.width + (self.width - 1) * self.parent.widget_margin_horizontal

    def get_height(self):
        return self.parent.widget_height * self.height + (self.height - 1) * self.parent.widget_margin_vertical

    def get_template_name(self, format):
        return u'widget/%s/view.%s' % (self.widget_name, format)

    def init(self):
        self.last_update = timezone.now() - self.get_update_interval
        self.cache['html'] = ""
        self.cache['json'] = {}

    def render(self, **kwargs):
        request = kwargs.get('request')
        force_update = kwargs.get('force_update', False)
        now = timezone.now()
        delta = now - self.last_update
        if delta.seconds > self.get_update_interval.seconds or force_update:
            self.cache['json'] = self.widget_data(request)
#            except:
#                self.cache['json'] = 'no cache'
#            self.cache['html'] = self.render_html(request)
            self.last_update = now
            self.save()
        return self.cache['html']

    def render_html(self, request):
        base_template = 'widget/base.html'
        template = loader.get_template(self.get_template_name('html'))
        context = RequestContext(request, {
            'widget': self,
            'base_template': base_template,
        })
        return template.render(context)

    def _get_update_interval(self):
        if self.update_interval_unit == 'day':
            delta = datetime.timedelta(days=self.update_interval_length)
        elif self.update_interval_unit == 'hour':
            delta = datetime.timedelta(hours=self.update_interval_length)
        elif self.update_interval_unit == 'minute':
            delta = datetime.timedelta(minutes=self.update_interval_length)
        elif self.update_interval_unit == 'second':
            delta = datetime.timedelta(seconds=self.update_interval_length)
        else:
            delta = None
        return delta
    get_update_interval = property(_get_update_interval)

    @classmethod
    def get_defaults(self):
        ret = {}
        for f in self._meta.fields:
            if f.has_default():
                ret[f.get_attname()] = f.default
        return ret

    @classmethod
    def get_options(self):
        """
        Returns all fields choices and foreign key choices
        """
        ret = []
        for f in self._meta.fields:
            if f.choices:
                ret.append({
                    'name': f.get_attname(),
                    'choices': f.get_choices(include_blank=False)
                })
        for f in self._meta.fields:
            if f.get_internal_type().lower() == 'foreignkey':
                foreign_model = f.rel.to
                options = foreign_model.objects.all()
                choices = []
                for option in options:
                    choices.append((option.id, option.__unicode__()))
                ret.append({
                    'name': f.get_attname().replace('_id', ''),
                    'choices': choices,
                })
        return ret

    @classmethod
    def get_form(self):

        class WidgetForm(forms.ModelForm):

            class Meta:
                model = self
                fields = self.form_fields()
                widgets = self.form_widgets()

            def __init__(self, layout, *args, **kwargs):
                super(WidgetForm, self).__init__(*args, **kwargs)
                self.helper = FormHelper()
                self.helper.form_method = 'GET'
                self.helper.form_tag = False
                self.helper.layout = Layout(
                    layout,
                    #FormActions(
                    #    Submit('submit', 'Submit'),
                    #    Button('cancel', 'Cancel')
                    #)
                )

        return WidgetForm(layout=self.form_layout())

    def update_fields(self, kwargs):

        data = self.fix_kwargs(kwargs)

        for key, value in data.items():
            setattr(self, key, value) 

    @classmethod
    def fix_kwargs(self, kwargs):

        for f in self._meta.fields:
            if f.get_internal_type().lower() == 'foreignkey':
                name = f.get_attname().replace('_id', '')
                if kwargs.has_key(name):
                    foreign_model = f.rel.to
                    foreign_object = foreign_model.objects.get(pk=kwargs.get(name))
                    kwargs[name] = foreign_object

        return kwargs

    @classmethod
    def get_serial(self):

        base_fields = ['kind', 'dashboard_id', 'uid', 'update_interval', 'col', 'row']

        for field in self.form_fields():
            base_fields.append(field)

        class WidgetSerializer(serializers.ModelSerializer):

            class Meta:
                model = self
                fields = base_fields

        return WidgetSerializer