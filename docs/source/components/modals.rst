
==============
Modals Dialogs
==============

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