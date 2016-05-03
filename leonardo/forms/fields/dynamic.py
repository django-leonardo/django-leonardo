import six
from django import forms
from django.core import urlresolvers
from django.core.urlresolvers import reverse_lazy
from django.forms import fields, widgets
from django.forms.utils import flatatt  # noqa
from django.utils import html
from django.utils.encoding import force_text
from django.utils.functional import Promise  # noqa
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import ModelSelect2Widget, Select2Widget


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
    _data_edit_url_attr = "data-edit-item-url"

    def render(self, *args, **kwargs):
        add_item_url = self.get_add_item_url()
        if add_item_url is not None:
            self.attrs[self._data_add_url_attr] = add_item_url

        content = super(DynamicSelectWidget, self).render(*args, **kwargs)

        if self.get_cls_name() or self.get_update_view_name():
            content += self.get_edit_handler()

        return content

    def get_edit_handler(self):
        '''TODO: Fix add-to-field'''
        # just a flag
        self.generic = 'false'

        return '''

        <span class="input-group-btn">
            <a href="#" id="item-edit-%(id)s" data-add-to-field="id_file" class="btn btn-default disabled"><span class="fa fa-pencil"></span></a></span>
        <script>

        if ($('*[data-add-item-url="%(url)s"]').val()) {
            $('#item-edit-%(id)s').removeClass('disabled');
        }

        $('*[data-add-item-url="%(url)s"]').on('change', function (e) {
            if ($('*[data-add-item-url="%(url)s"]').val()) {
                $('#item-edit-%(id)s').removeClass('disabled');
            } else {
                $('#item-edit-%(id)s').addClass('disabled');
            }
        });

        $("#item-edit-%(id)s").click(function() {

            var generic = %(generic)s;
            var ajax_opts = {};
            var id = $('*[data-add-item-url="%(url)s"]').val();

            if (generic) {

                ajax_opts = {
                  url: "/widget/js-reverse/",
                  method: 'POST',
                  data: {
                    viewname: '%(update_viewname)s',
                    kwargs:  JSON.stringify({
                        cls_name: '%(cls_name)s',
                        id: id,
                        form_cls: '%(form_cls)s'
                        })
                    }
                };

            } else {
                ajax_opts = {
                  url: "/widget/js-reverse/",
                  method: 'POST',
                  data: {
                    viewname: '%(update_viewname)s',
                    args: JSON.stringify({id: id})
                    }
                };
            }
            $.ajax(ajax_opts)
              .done(function( data ) {

                horizon.modals._request = $.ajax(data.url, {
                  beforeSend: function () {
                    horizon.modals.modal_spinner(gettext("Loading"));
                  },
                  complete: function () {
                    // Clear the global storage;
                    horizon.modals._request = null;
                    horizon.modals.spinner.modal('hide');
                  },
                  error: function(jqXHR, status, errorThrown) {
                    if (jqXHR.status === 401){
                      var redir_url = jqXHR.getResponseHeader("X-Horizon-Location");
                      if (redir_url){
                        location.href = redir_url;
                      } else {
                        location.reload(true);
                      }
                    }
                    else {
                      if (!horizon.ajax.get_messages(jqXHR)) {
                        // Generic error handler. Really generic.
                        horizon.alert("danger", gettext(
                            "An error occurred. Please try again later."));
                      }
                    }
                  },
                  success: function (data, textStatus, jqXHR) {
                    var update_field_id = 'data-add-to-field',
                      modal,
                      form;
                    modal = horizon.modals.success(
                        data, textStatus, jqXHR);
                    if (update_field_id) {
                      form = modal.find("form");
                      if (form.length) {
                        form.attr("data-add-to-field", update_field_id);
                      }
                    }
                  }
                });
              });
        });
        </script>
        ''' % {'update_viewname': self.get_update_view_name(),
               'cls_name': self.get_cls_name(),
               'url': self.get_add_item_url(),
               'form_cls': self.get_form_cls(),
               'id': self.__hash__(),
               'generic': self.generic}

    def get_update_view_name(self):

        if hasattr(self, '_edit_url'):
            return self._edit_url

        self._edit_url = self.get_edit_item_url()

        if not self._edit_url:
            if self.get_form_cls():
                self._edit_url = 'forms:update_with_form'
            else:
                self._edit_url = 'forms:update'
            self.generic = 'true'
        return self._edit_url

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

    def get_edit_item_url(self):
        if callable(self.edit_item_link):
            return self.edit_item_link()
        try:
            if self.add_item_link_args:
                return urlresolvers.reverse(self.edit_item_link,
                                            args=self.add_item_link_args)
            else:
                return urlresolvers.reverse(self.edit_item_link)
        except urlresolvers.NoReverseMatch:
            return self.edit_item_link

    def get_cls_name(self):
        if hasattr(self, 'cls_name'):
            return self.cls_name
        return ''

    def get_form_cls(self):
        if hasattr(self, 'form_cls'):
            return self.form_cls
        return ''


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
                 edit_item_link=None,
                 edit_item_link_args=None,
                 cls_name=None,
                 form_cls=None,
                 search_fields=None,
                 *args,
                 **kwargs):
        super(DynamicChoiceField, self).__init__(*args, **kwargs)

        if search_fields:
            self.widget.search_fields = search_fields

        if cls_name or hasattr(self, 'cls_name'):
            self.widget.cls_name = cls_name or self.cls_name
            cls_name = cls_name or self.cls_name

        if form_cls or hasattr(self, 'form_cls'):
            self.widget.form_cls = form_cls or self.form_cls
            form_cls = form_cls or self.form_cls

        if search_fields:
            self.widget.search_fields = search_fields

        if cls_name and not add_item_link and not form_cls:
            self.widget.add_item_link = 'forms:create'
            self.widget.add_item_link_args = (cls_name, )

        if cls_name and form_cls and not add_item_link:
            self.widget.add_item_link = 'forms:create_with_form'
            self.widget.add_item_link_args = (cls_name, form_cls)

        if not form_cls:
            self.widget.add_item_link = add_item_link
            self.widget.add_item_link_args = add_item_link_args

        self.widget.edit_item_link = edit_item_link or getattr(
            self, 'edit_item_link', None)
        self.widget.edit_item_link_args = edit_item_link_args or getattr(
            self, 'add_item_link_args', None)

DEFAULT_SEARCH_FIELDS = [
    'id__icontains',
]


class DynamicModelSelect2Widget(DynamicSelectWidget, ModelSelect2Widget):

    pass


class DynamicModelChoiceField(forms.ModelChoiceField):
    """A subclass of ``ChoiceField`` with additional properties that make
    dynamically updating its elements easier.

    Notably, the field declaration takes an extra argument, ``add_item_link``
    and ``edit_item_link``
    which may be a string or callable defining the URL that should be used
    for the "add" link associated with the field.
    or just set ``cls_name`` and ``form_cls`` which will be used to
    horizon-contrib views
    """
    widget = DynamicModelSelect2Widget

    def __init__(self,
                 add_item_link=None,
                 add_item_link_args=None,
                 edit_item_link=None,
                 edit_item_link_args=None,
                 cls_name=None,
                 form_cls=None,
                 search_fields=None,
                 *args,
                 **kwargs):
        super(DynamicModelChoiceField, self).__init__(*args, **kwargs)

        if cls_name or hasattr(self, 'cls_name'):
            self.widget.cls_name = cls_name or self.cls_name
            cls_name = cls_name or self.cls_name

        if form_cls or hasattr(self, 'form_cls'):
            self.widget.form_cls = form_cls or self.form_cls
            form_cls = form_cls or self.form_cls

        if cls_name and not add_item_link and not form_cls:
            self.widget.add_item_link = 'forms:create'
            self.widget.add_item_link_args = (cls_name, )

        if cls_name and form_cls and not add_item_link:
            self.widget.add_item_link = 'forms:create_with_form'
            self.widget.add_item_link_args = (cls_name, form_cls)

        if search_fields:
            self.widget.search_fields = search_fields

        if not cls_name:
            self.widget.add_item_link = add_item_link or getattr(
                self, 'add_item_link', None)
            self.widget.add_item_link_args = add_item_link_args or getattr(
                self, 'add_item_link_args', None)

        self.widget.edit_item_link = edit_item_link or getattr(
            self, 'edit_item_link', None)
        self.widget.edit_item_link_args = edit_item_link_args or getattr(
            self, 'add_item_link_args', None)


class DynamicTypedChoiceField(DynamicChoiceField, fields.TypedChoiceField):
    """Simple mix of ``DynamicChoiceField`` and ``TypedChoiceField``."""
    pass
