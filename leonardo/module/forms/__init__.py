"""
from django.forms import (Form, ModelForm, BaseModelForm, model_to_dict,
                          fields_for_model, save_instance, ValidationError,
                          #                          DEFAULT_DATE_INPUT_FORMATS,
                          #                          DEFAULT_TIME_INPUT_FORMATS,
                          #                          DEFAULT_DATETIME_INPUT_FORMATS,
                          Media, MediaDefiningClass)

# Import SelectDateWidget from extras
from django.forms.extras import SelectDateWidget

from .fields import *
from .models import *
"""

from django.apps import AppConfig

from .widget import *


default_app_config = 'leonardo.module.forms.FormConfig'


class Default(object):

    @property
    def apps(self):
        return [
            'form_designer',
            'django_remote_forms',
        ]

    @property
    def widgets(self):
        return [
            FormWidget,
        ]


class FormConfig(AppConfig):
    name = 'leonardo.module.forms'
    verbose_name = "Module Forms"

    conf = Default()

default = Default()
