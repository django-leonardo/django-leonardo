from __future__ import unicode_literals

import django
from django import forms
from django.core import exceptions, validators
from django.db import models
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _


class MaxValueMultiFieldValidator(validators.MaxLengthValidator):
    clean = lambda self, x: len(','.join(x))
    code = 'max_multifield_value'


class MaxChoicesValidator(validators.MaxLengthValidator):
    message = _(u'You must select a maximum of  %(limit_value)d choices.')
    code = 'max_choices'


def get_max_length(choices, max_length, default=200):
    if max_length is None:
        if choices:
            return len(','.join([key for key, label in choices]))
        else:
            return default
    return max_length


class MultiSelectFormField(forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple

    def __init__(self, *args, **kwargs):
        self.max_choices = kwargs.pop('max_choices', None)
        self.max_length = kwargs.pop('max_length', None)
        super(MultiSelectFormField, self).__init__(*args, **kwargs)
        self.max_length = get_max_length(self.choices, self.max_length)
        self.validators.append(MaxValueMultiFieldValidator(self.max_length))
        if self.max_choices is not None:
            self.validators.append(MaxChoicesValidator(self.max_choices))


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        for slots_var in orig_vars.get('__slots__', ()):
            orig_vars.pop(slots_var)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


class MultiSelectField(models.CharField):

    """ Choice values can not contain commas. """

    def __init__(self, *args, **kwargs):
        self.max_choices = kwargs.pop('max_choices', None)
        super(MultiSelectField, self).__init__(*args, **kwargs)
        self.max_length = get_max_length(self.choices, self.max_length)
        self.validators[0] = MaxValueMultiFieldValidator(self.max_length)
        if self.max_choices is not None:
            self.validators.append(MaxChoicesValidator(self.max_choices))

    @property
    def flatchoices(self):
        return None

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def get_choices_selected(self, arr_choices):
        choices_selected = []
        for choice_selected in arr_choices:
            choices_selected.append(choice_selected[0])
        return choices_selected

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def validate(self, value, model_instance):
        arr_choices = self.get_choices_selected(self.get_choices_default())
        for opt_select in value:
            if (opt_select not in arr_choices):
                if django.VERSION[0] == 1 and django.VERSION[1] >= 6:
                    raise exceptions.ValidationError(
                        self.error_messages['invalid_choice'] % {"value": value})
                else:
                    raise exceptions.ValidationError(
                        self.error_messages['invalid_choice'] % value)

    def get_default(self):
        default = super(MultiSelectField, self).get_default()
        if isinstance(default, int):
            default = str(default)
        return default

    def formfield(self, **kwargs):
        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text,
                    'choices': self.choices,
                    'max_length': self.max_length,
                    'max_choices': self.max_choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_prep_value(self, value):
        return '' if value is None else ",".join(value)

    def to_python(self, value):
        if value:
            return value if isinstance(value, list) else value.split(',')

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            def get_list(obj):
                fieldname = name
                choicedict = dict(self.choices)
                display = []
                if getattr(obj, fieldname):
                    for value in getattr(obj, fieldname):
                        item_display = choicedict.get(value, None)
                        if item_display is None:
                            try:
                                item_display = choicedict.get(int(value), value)
                            except (ValueError, TypeError):
                                item_display = value
                        display.append(str(item_display))
                return display

            def get_display(obj):
                return ", ".join(get_list(obj))

            setattr(cls, 'get_%s_list' % self.name, get_list)
            setattr(cls, 'get_%s_display' % self.name, get_display)

MultiSelectField = add_metaclass(models.SubfieldBase)(MultiSelectField)
