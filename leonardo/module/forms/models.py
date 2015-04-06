from django.db import models

#__all__ = ('ModelChoiceField', 'ModelMultipleChoiceField')

#class ModelChoiceField(models.ModelChoiceField):
#    widget = Select

#class ModelMultipleChoiceField(models.ModelMultipleChoiceField):
#    widget = SelectMultiple

from django.db import models
from django import forms
from django.utils.text import capfirst

"""
from fields import MultiSelectField as MultiSelectFormField

class MultiSelectField(models.Field):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "CharField"

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def _get_FIELD_display(self, field):
        value = getattr(self, field.attname)
        choicedict = dict(field.choices)

    def formfield(self, **kwargs):
        # don't call super, as that overrides default widget if it has choices
        defaults = {'required': not self.blank, 'label': capfirst(self.verbose_name),
                    'help_text': self.help_text, 'choices':self.choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_db_prep_value(self, value):
        if isinstance(value, basestring):
            return value
        elif isinstance(value, list):
            return ",".join(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        return value.split(",")

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            func = lambda self, fieldname = name, choicedict = dict(self.choices):",".join([choicedict.get(value,value) for value in getattr(self,fieldname)])
            setattr(cls, 'get_%s_display' % self.name, func)
"""
