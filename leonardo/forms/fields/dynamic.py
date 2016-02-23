import six
from django import forms
from django.core import urlresolvers
from django.forms import fields, widgets
from django.forms.utils import flatatt  # noqa
from django.utils import html
from django.utils.encoding import force_text
from django.utils.functional import Promise  # noqa
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2Widget, ModelSelect2Widget


class SelectWidget(widgets.Select):
    """Customizable select widget, that allows to render
    data-xxx attributes from choices. This widget also
    allows user to specify additional html attributes
    for choices.

    .. attribute:: data_attrs

        Specifies object properties to serialize as
        data-xxx attribute. If passed ('id', ),
        this will be rendered as:
        <option data-id="123">option_value</option>
        where 123 is the value of choice_value.id

    .. attribute:: transform

        A callable used to render the display value
        from the option object.

    .. attribute:: transform_html_attrs

        A callable used to render additional HTML attributes
        for the option object. It returns a dictionary
        containing the html attributes and their values.
        For example, to define a title attribute for the
        choices::

            helpText = { 'Apple': 'This is a fruit',
                      'Carrot': 'This is a vegetable' }

            def get_title(data):
                text = helpText.get(data, None)
                if text:
                    return {'title': text}
                else:
                    return {}

            ....
            ....

            widget=forms.SelectWidget( attrs={'class': 'switchable',
                                             'data-slug': 'source'},
                                    transform_html_attrs=get_title )

            self.fields[<field name>].choices =
                ([
                    ('apple','Apple'),
                    ('carrot','Carrot')
                ])

    """

    def __init__(self, attrs=None, choices=(), data_attrs=(), transform=None,
                 transform_html_attrs=None):
        self.data_attrs = data_attrs
        self.transform = transform
        self.transform_html_attrs = transform_html_attrs
        super(SelectWidget, self).__init__(attrs, choices)

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        other_html = (u' selected="selected"'
                      if option_value in selected_choices else '')

        if callable(self.transform_html_attrs):
            html_attrs = self.transform_html_attrs(option_label)
            other_html += flatatt(html_attrs)

        if not isinstance(option_label, (six.string_types, Promise)):
            for data_attr in self.data_attrs:
                data_value = html.conditional_escape(
                    force_text(getattr(option_label,
                                       data_attr, "")))
                other_html += ' data-%s="%s"' % (data_attr, data_value)

            if callable(self.transform):
                option_label = self.transform(option_label)

        return u'<option value="%s"%s>%s</option>' % (
            html.escape(option_value), other_html,
            html.conditional_escape(force_text(option_label)))


class DynamicSelectWidget(Select2Widget):
    """A subclass of the ``Select2Widget`` widget which renders extra attributes for
    use in callbacks to handle dynamic changes to the available choices.
    """
    _data_add_url_attr = "data-add-item-url"

    def render(self, *args, **kwargs):
        add_item_url = self.get_add_item_url()
        if add_item_url is not None:
            self.attrs[self._data_add_url_attr] = add_item_url
        return super(DynamicSelectWidget, self).render(*args, **kwargs)

    def get_add_item_url(self):
        if callable(self.add_item_link):
            return self.add_item_link()
        try:
            if self.add_item_link_args:
                return urlresolvers.reverse(self.add_item_link,
                                            args=self.add_item_link_args)
            else:
                return urlresolvers.reverse(self.add_item_link)
        except urlresolvers.NoReverseMatch:
            return self.add_item_link


class DynamicChoiceField(fields.ChoiceField):
    """A subclass of ``ChoiceField`` with additional properties that make
    dynamically updating its elements easier.

    Notably, the field declaration takes an extra argument, ``add_item_link``
    which may be a string or callable defining the URL that should be used
    for the "add" link associated with the field.
    """
    widget = DynamicSelectWidget

    def __init__(self,
                 add_item_link=None,
                 add_item_link_args=None,
                 search_fields=None,
                 *args,
                 **kwargs):
        super(DynamicChoiceField, self).__init__(*args, **kwargs)

        if search_fields:
            self.widget.search_fields = search_fields

        self.widget.add_item_link = add_item_link
        self.widget.add_item_link_args = add_item_link_args


DEFAULT_SEARCH_FIELDS = [
    'id__icontains',
]


class DynamicModelSelect2Widget(DynamicSelectWidget, ModelSelect2Widget):

    pass


class DynamicModelChoiceField(forms.ModelChoiceField):
    """A subclass of ``ChoiceField`` with additional properties that make
    dynamically updating its elements easier.

    Notably, the field declaration takes an extra argument, ``add_item_link``
    which may be a string or callable defining the URL that should be used
    for the "add" link associated with the field.
    """
    widget = DynamicModelSelect2Widget

    def __init__(self,
                 add_item_link=None,
                 add_item_link_args=None,
                 search_fields=None,
                 *args,
                 **kwargs):
        super(DynamicModelChoiceField, self).__init__(*args, **kwargs)

        if search_fields:
            self.widget.search_fields = search_fields

        self.widget.add_item_link = add_item_link
        self.widget.add_item_link_args = add_item_link_args


class DynamicTypedChoiceField(DynamicChoiceField, fields.TypedChoiceField):
    """Simple mix of ``DynamicChoiceField`` and ``TypedChoiceField``."""
    pass
