# -*- coding: utf-8 -*-

from dajax.core import Dajax
from dajaxice.core import dajaxice_functions

from django.utils.translation import ugettext_lazy as _, ugettext as __

from django import forms
from django.forms.models import modelform_factory

from django.db.models import loading
from django.template.loader import render_to_string
from django.template import RequestContext

from feincms.module.page.models import Page

from webcms.utils.forms import process_dajax_data
from webcms.forms import GenericWidgetModelForm, WidgetOptionsForm, WidgetCreateForm, PageSimpleUpdateForm, PageOptionsForm

from webcms.module.web.models import check_options

from webcms.utils.widgets import get_widget_from_id, get_widget_class_from_id

from forms import get_widget_update_forms

def widget_create(request, page_id, region, options):

    page = Page.objects.get(pk=page_id)
    position = options['index']  # position seems to start with 1
    temp_sources = options['id'].split('__')
    create_new = False
    options = {}

    for temp_source in temp_sources:
        if temp_source.startswith('new-'):
            source = temp_source.replace('new-', '')

            model_cls = loading.get_model('page', source)
            create_new = True
            kwargs = {
                'parent': page,
                'region': 'col3',
            }
            new_widget = model_cls(**kwargs)

    dajax = Dajax()

    if create_new:

        i = 0

        widgets = page.content.col3

        for widget in widgets:
            if i >= position:
                widget.ordering = i + 1
                widget.save()
            else:
                if widget.ordering != i:
                    widget.ordering = i
                    widget.save()
            i += 1

        try:
            new_widget.ordering = position
            new_widget.save()
        except:
            dajax.add_data({ 'text': __('Error occured while creating widget.'), 'type': 'error' }, 'fe_notice')
            return dajax.json()

        kwargs = {
            'request': request
        }

        options = {
            'id': new_widget.fe_identifier(),
            'position': position,
            'class': 'fe_box webcms-widget webcms-%s-widget span-24 normal-widget' % new_widget.widget_name,
            'content': new_widget.render_content(kwargs)
        }

        dajax.add_data(options, 'fe_widget_create')

        notice = {
            'text': __('Widget %(widget)s successfully created.') % { 'widget': new_widget.widget_label },
            'type': 'success' 
        }

        dajax.add_data(notice, 'fe_notice')

    return dajax.json()
dajaxice_functions.register(widget_create)

def widget_update(request, widget_id, page_id):
    form, obj_form = get_widget_update_forms(request, widget_id, True)

    context = RequestContext(request, {
        'request': request,
        'form': form,
        'obj_form': obj_form,
    })

    data = {
        'title': __('Update %(widget)s') % { 'widget': obj_form.instance.widget_label },
        'content': render_to_string('admin/webcms/widget/widget_update.html', context),
        'widget_id': widget_id,
        'display': obj_form.instance.options
    }

    dajax = Dajax()
    dajax.add_data(data, 'fe_widget_update')
    return dajax.json()
dajaxice_functions.register(widget_update)

def widget_update_process(request, data, widget_id, page_id):
    form, obj_form = get_widget_update_forms(request, widget_id, False, process_dajax_data(data))
    widget = obj_form.instance
    dajax = Dajax()

    if form.is_valid() and obj_form.is_valid():
        options = form.cleaned_data.copy()
        options['size'] = [options.pop('span'), options.pop('vertical_span')]
        options['padding'] = [options.pop('vertical_prepend'), options.pop('append'), options.pop('vertical_append'), options.pop('prepend')]
        options['margin'] = [options.pop('vertical_pull'), options.pop('push'), options.pop('vertical_push'), options.pop('pull')]
        options['align'] = [options.pop('align'), options.pop('vertical_align')]
        widget.options = options
        output = widget.render_content({'request': request})
        widget.save()
        obj_form.save()
        data = {
            'id': widget.fe_identifier(),
            'content': output,
        }
        notice = {'text': __('Widget successfully updated.'), 'type': 'success' }
        dajax.add_data(data, 'fe_widget_replace')
        dajax.add_data(None, 'fe_dialog_close')
        dajax.add_data(notice, 'fe_notice')
    else:
        content = render_to_string('admin/webcms/widget/widget_update.html', {
            'request': request,
            'form': form,
            'obj_form': obj_form,
        })
        data = {
            'title': __('Update %(widget)s') % { 'widget': obj_form.instance.widget_label },
            'content': content,
            'widget_id': widget_id,
            'display': obj_form.instance.options
        }
        notice = {'text': __('Form did not validate.'), 'type': 'error' }
        dajax.add_data(data, 'fe_widget_update')
        dajax.add_data(notice, 'fe_notice')
    return dajax.json()
dajaxice_functions.register(widget_update_process)

def widget_sort(request, page_id, region, widgets):

    page = Page.objects.get(pk=page_id)
    widget_list = []
    widget_list_id = []
    create_new = False

    dajax = Dajax()

    try:
        for widget_id in widgets:
            widget = get_widget_from_id(widget_id)
            widget_list.append(widget)

    except:
        dajax.add_data({ 'text': __('Error occured while sorting widgets.'), 'type': 'error' }, 'fe_notice')
        return dajax.json()

    i = 0

    for widget_id in widgets:
        widget = get_widget_from_id(widget_id)
        widget.ordering = i
        widget.save()
        widget_list_id.append('%s: %s' % (i, widget.fe_identifier()))
        i += 1

    dajax.add_data({ 'text': __('Widgets successfully reordered.'), 'type': 'success'}, 'fe_notice')
    dajax.add_data({ 'widgets': widgets, 'widget_list': widget_list_id}, 'fe_widget_sort')
    return dajax.json()

dajaxice_functions.register(widget_sort)

def widget_remove(request, widget_id, page_id):
    widget = get_widget_from_id(widget_id)

    content = render_to_string('admin/webcms/widget/widget_delete.html', {
        'object': widget,
        'request': request,
    })

    data = {
        'title': __('Really delete %(widget)s?') % { 'widget': widget.widget_label },
        'widget_id': widget.fe_identifier(),
        'content': content,
    }

    dajax = Dajax()
    dajax.add_data(data, 'fe_widget_remove')
    return dajax.json()
dajaxice_functions.register(widget_remove)

def widget_remove_process(request, widget_id, page_id):
    widget = get_widget_from_id(widget_id)
    dajax = Dajax()

    try:
        dajax.add_data(widget.fe_identifier(), 'fe_widget_delete')
        widget.delete()
        notice = {'text': __('Widget successfully deleted.'), 'type': 'success' }
        dajax.add_data(notice, 'fe_notice')
    except:
        notice = {'text': __('Error deleting widget.'), 'type': 'error' }
        dajax.add_data(notice, 'fe_notice')

    dajax.add_data(None, 'fe_dialog_close')

    return dajax.json()
dajaxice_functions.register(widget_remove_process)

def widget_info(request, widget_id, page_id):
    cls = get_widget_class_from_id(widget_id)
    widget = get_widget_from_id(widget_id)

    content = render_to_string('admin/webcms/widget/widget_info.html', {
        'object': widget,
        'type': cls._meta.__dict__['verbose_name'],
        'request': request,
    })

    data = { 'content': content }

    dajax = Dajax()
    dajax.add_data(data, 'fe_widget_info')
    return dajax.json()
dajaxice_functions.register(widget_info)

def page_move(request, page_id, target_id, position):
    page = Page.objects.get(id=page_id)
    target = Page.objects.get(id=target_id)

    if position == 'first':
        position = 'first-child'
    if position == 'last':
        position = 'last-child'
    if position == 'before':
        position = 'left'
    if position == 'after':
        position = 'right'

    page.move_to(target, position=position)

    dajax = Dajax()

    notice = {
        'text': __('Page successfully moved.'),
        'type': 'success'
    }

    dajax.add_data(notice, 'fe_notice')
    return dajax.json()
dajaxice_functions.register(page_move)

def page_create(request, page_id, target_id, position):
    target = Page.objects.get(id=target_id)

    if position == 'inside':
        position = 'first-child'
    if position == 'before':
        position = 'left'
    if position == 'after':
        position = 'right'

    page = Page(title=__('New page'))
    page.insert_at(target, position=position, save=True)

    dajax = Dajax()
    notice = {
        'text': __('Page successfully created.'),
        'type': 'success'
    }

    data = {
        'page_node': 'node_%s' % page.id,
    }

    dajax.add_data(data, 'fe_page_create')
    dajax.add_data(notice, 'fe_notice')
    return dajax.json()
dajaxice_functions.register(page_create)

def page_update(request, page_id):
    page = Page.objects.get(id=page_id)

    class PageUpdateForm(forms.ModelForm):
        never_copy_fields = ('title', 'slug', 'parent', 'active', 'override_url',
            'translation_of', '_content_title', '_page_title')

        def __init__(self, *args, **kwargs):
            super(PageUpdateForm, self).__init__(*args, **kwargs)
            if self.fields.has_key('template_key'):
                self.fields['template_key'].widget = forms.TextInput()

        class Meta:
            model = Page

    form = PageUpdateForm(instance=page)

    options = check_options(page)
    if options:
        initial = options
    else:
        initial = page.options

    options_form = PageOptionsForm(initial=initial)

    content = render_to_string('admin/webcms/page/page_update.html', {
        'object': page,
        'request': request,
        'form': form,
        'options_form': options_form,
    })

    data = {
        'title': __('Update page "%s"' % page.short_title()),
        'content': content,
    }

    dajax = Dajax()
    dajax.add_data(data, 'fe_page_update')
    return dajax.json()
dajaxice_functions.register(page_update)

def page_update_process(request, data, page_id):
    page = Page.objects.get(id=page_id)

    class PageUpdateForm(forms.ModelForm):
        never_copy_fields = ('title', 'slug', 'parent', 'active', 'override_url',
            'translation_of', '_content_title', '_page_title')

        def __init__(self, *args, **kwargs):
            super(PageUpdateForm, self).__init__(*args, **kwargs)
            if self.fields.has_key('template_key'):
                self.fields['template_key'].widget = forms.TextInput()

        class Meta:
            model = Page

    form = PageUpdateForm(data=process_dajax_data(data), instance=page)
    options_form = PageOptionsForm(data=process_dajax_data(data))

    dajax = Dajax()

    if form.is_valid() and options_form.is_valid():
        saved_page = form.save(commit=False)

        saved_page.options = options_form.cleaned_data.copy()
        saved_page.save()

        dajax.add_data(None, 'fe_dialog_close')
        dajax.add_data({'text': __('Page successfully updated.'), 'type': 'success' }, 'fe_notice')
        dajax.add_data(None, 'fe_page_refresh')

        return dajax.json()
    else:
        content = render_to_string('admin/webcms/page/page_update.html', {
            'object': page,
            'request': request,
            'form': form,
            'options_form': options_form,
        })
        data = {
            'title': u'Update page "%s"' % page.short_title(),
            'content': content,
        }

        dajax.add_data(data, 'fe_page_update')
        dajax.add_data({'text': __('Form did not validate.'), 'type': 'error' }, 'fe_notice')

        return dajax.json()
dajaxice_functions.register(page_update_process)

def page_simple_update(request, page_id):

    page = Page.objects.get(id=page_id)
    form = PageSimpleUpdateForm(instance=page)

    context = RequestContext(request, {
        'page': page,
        'form': form,
    })

    content = render_to_string('admin/webcms/page/page_simple_update.html', context)
#    render = render_to_string('base/plain.html', context)

    data = {
        'title': u'Update page "%s"' % page.short_title(),
        'content': content,
    }

    dajax = Dajax()
#    dajax.add_data({ 'render': render }, 'fe_container_refresh')
    dajax.add_data(data, 'fe_page_simple_update')
    return dajax.json()
dajaxice_functions.register(page_simple_update)

def page_simple_update_process(request, data, page_id):
    page = Page.objects.get(id=page_id)
    form = PageSimpleUpdateForm(data=process_dajax_data(data), instance=page)

    dajax = Dajax()

    content = render_to_string('admin/webcms/page/page_simple_update.html', RequestContext(request, { 'form': form, }))

    if form.is_valid():
        saved_page = form.save(commit=False)

        saved_page.save()

        dajax.add_data({'text': __('Page successfully updated.'), 'type': 'success' }, 'fe_notice')
    else:
        data = {
            'title': u'Update page "%s"' % page.short_title(),
            'content': content,
        }

        dajax.add_data({'text': __('Form did not validate.'), 'type': 'error' }, 'fe_notice')
    dajax.add_data(data, 'fe_page_simple_update')
    return dajax.json()
dajaxice_functions.register(page_simple_update_process)

def page_to_treenode(page):
    return {
        'data': {
            'title': page.title,
            'attr': {
                'id': 'node_%s' % page.id
            },
            'icon': 'folder',
        },
#        'state': 'closed',
        'children': [],
#        'language': page.language
    }

def get_site_structure(request, page_id):

    page = Page.objects.get(id=page_id)
    root = page.get_root()

    site_pages = []

    for l1 in root.get_children():
        l1_output = page_to_treenode(l1)
        for l2 in l1.get_children():
            l2_output = page_to_treenode(l2)
            l1_output['children'].append(l2_output)
        site_pages.append(l1_output)

    dajax = Dajax()
    dajax.add_data({'data': site_pages}, 'fe_site_structure_update')

    return dajax.json()

dajaxice_functions.register(get_site_structure)

def site_update(request, site_id, page_id):
    page = Page.objects.get(id=page_id)
    root = page.get_root()

    site_pages = []

    for l1 in root.get_children():
        l1_output = page_to_treenode(l1)
        for l2 in l1.get_children():
            l2_output = page_to_treenode(l2)
            for l3 in l2.get_children():
                l3_output = page_to_treenode(l3)
                if len(l3_output['children']) == 0:
                    l3_output.pop('children')
                l2_output['children'].append(l3_output)
            if len(l2_output['children']) == 0:
                l2_output.pop('children')
            l1_output['children'].append(l2_output)
        if len(l1_output['children']) == 0:
            l1_output.pop('children')
        site_pages.append(l1_output)

    form = PageSimpleUpdateForm(instance=page)

    content = render_to_string('admin/webcms/site/site_update.html', RequestContext(request, {
        'object': page,
        'form': form,
    }))

    data = {
        'title': u'Update site "%s"' % page.short_title(),
        'content': content,
        'site_pages': site_pages,
    }

    dajax = Dajax()
    dajax.add_data(data, 'fe_site_update')
#    dajax.add_data(None, 'fe_site_update_process')

    return dajax.json()
dajaxice_functions.register(site_update)
