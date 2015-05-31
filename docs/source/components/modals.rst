
==============
Modals Dialogs
==============

Standard modals via views

``modal_size`` - valid options ``md``, ``lg``, ``sm``

.. code-block:: python

    from horizon import forms

    class WidgetDeleteView(forms.ModalFormView):

        form_class = WidgetDeleteForm

	    template_name = 'leonardo/common/modal.html'

        def get_context_data(self, **kwargs):
            context = super(WidgetDeleteView, self).get_context_data(**kwargs)

            context['url'] = self.request.build_absolute_uri()
            context['form_action'] = 'POST'
            context['modal_header'] = _('Create new Moon')
            context['title'] = _('Create new Moon')
            context['form_submit'] = _('Create')
            context['heading'] = self.get_header()
            context['help_text'] = _('Your awesome help text')
            context['modal_size'] = 'lg'

            return context

Lightboxes
==========

For galleries you can use default Lightboxes for Bootstrap 3 see example below::

    <a class="thumbnail" data-toggle="lightbox" data-title="{{ image.caption }}" data-footer="{{ image.description }}" href="{{ image.url }}">
      {% thumbnail file.file "320x200" crop="center" as thumbnail %}
      <img class="img-responsive" src="{{ thumbnail.url }}" alt="{{ category_file.default_alt_text }}" />
      {% endthumbnail %}
    </a>