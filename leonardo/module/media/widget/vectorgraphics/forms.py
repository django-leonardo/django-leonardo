from itertools import chain
import random

from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from feincms.admin.item_editor import ItemEditorForm
from feincms._internal import monkeypatch_method
from feincms.module.page.models import Page

class SVGPreviewAdminForm(ItemEditorForm):
    def __init__(self, *args, **kwargs):    
        super(SVGPreviewAdminForm, self).__init__(*args, **kwargs)
        from models import SVGFile
        instance = kwargs.get('instance', False) or (len(args) and args[0]) or False  
        
        
        orig_render_options = self.fields['markup'].widget.widget.render_options
        widget = self.fields['markup'].widget.widget
        
        
        @monkeypatch_method(self.fields['markup'].widget.widget)
        def render_options(choices, selected_choices):
            def render_option(option_value, option_label):
                try:
                    id = int(option_value)
                except ValueError:
                    id = None
                if id:
                    svgfile = SVGFile.objects.get(id=id)
                    option_src = svgfile.file.url
                    option_width = svgfile.width
                    option_height = svgfile.height
                else:
                    option_src = None
                    
                
                option_value = force_unicode(option_value)
                selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
                if option_src:
                    selected_html += ' src="%s" width="%s" height="%s"'%(option_src,
                                                                         option_width,
                                                                         option_height,)
                return u'<option value="%s"%s>%s</option>' % (
                    escape(option_value), 
                    selected_html,
                    conditional_escape(force_unicode(option_label)))
            # Normalize to strings.
            selected_choices = set([force_unicode(v) for v in selected_choices])
            output = []
            for option_value, option_label in chain(widget.choices, choices):
                if isinstance(option_label, (list, tuple)):
                    output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                    for option in option_label:
                        output.append(render_option(*option))
                    output.append(u'</optgroup>')
                else:
                    output.append(render_option(option_value, option_label))
            return u'\n'.join(output) 
        
        orig_render = self.fields['markup'].widget.render
        @monkeypatch_method(self.fields['markup'].widget)
        def render(self, *args, **kwargs):
            kwargs['attrs'] = {'onchange':mark_safe(render_to_string('admin/svgfile/render_option_with_preview.html',
                                                           {}).replace('\n',''))}
            output = [orig_render(self, *args, **kwargs)]

            if instance and getattr(instance, 'markup'):
                #TODO: render this with template
                output.insert(0,"<span style='float:left;left:0px;'><ul style='margin-left:0px;padding-left:0px'>",)
                output.append("<li>",)
                output.append((getattr(instance.markup,'link',False) \
                                      and instance.markup.link()) or '')
                output.append("</li>",)
                output.append("<li>",)
                output.append((getattr(instance.markup,'edit_link',False) \
                                      and instance.markup.edit_link()) or '')
                output.append("</li>",)
                output.append("</ul></span><span>",)
                output.append((getattr(instance.markup,'preview',False) \
                                      and instance.markup.preview()) or '')
                output.append("</span>",)
            else:
                output.insert(0,"<span style='float:left;'><ul style='margin-left:0px'>",)
                output.append("</ul></span><span>",)
                output.append(render_to_string('admin/svgfile/preview.html',
                                {}))
                output.append("</span>",)
            return mark_safe(u''.join(output))

class SVGComponentsTree(forms.Widget):
    
    def __init__(self, *args, **kwargs):
        super(SVGComponentsTree, self).__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None):
        return render_to_string('widget/svg_components_tree.html',
                                {'roots':Page.objects.filter(parent=None),
                                 'components':getattr(self, 'components', []),
                                 'composers':getattr(self, 'composers', []),
                                 'composer':getattr(self, 'composer', None)})

class SVGComponentsTreeField(forms.Field):
    widget = SVGComponentsTree
    
    def __init__(self, *args, **kwargs):
        super(SVGComponentsTreeField, self).__init__(*args, **kwargs)




class SVGComposerForm(ItemEditorForm):
    tree = SVGComponentsTreeField(required=False)
    class Meta:
        pass
#        exclude = ('markup')
    def __init__(self, *args, **kwargs):
        super(SVGComposerForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', False) or (len(args) and args[0]) or False

        self.fields['markup'].widget.attrs.update({'style':'display:none'})
        self.fields['markup'].widget.widget.attrs.update({'style':'display:none'})

        orig_render = self.fields['markup'].widget.render
        @monkeypatch_method(self.fields['markup'].widget)
        def render(self, *args, **kwargs):
            output = [orig_render(self, *args, **kwargs)]

            if instance and getattr(instance, 'markup'):
                #TODO: render this with template
                output.insert(0,"<span style='float:left;left:0px;'><ul style='margin-left:0px;padding-left:0px'>",)
                output.append("<li>",)
                output.append((getattr(instance.markup,'link',False) \
                                      and instance.markup.link()) or '')
                output.append("</li>",)
                output.append("<li>",)
                output.append((getattr(instance.markup,'edit_link',False) \
                                      and instance.markup.edit_link()) or '')
                output.append("</li>",)
                output.append("</ul></span><span>",)
                output.append((getattr(instance.markup,'preview',False) \
                                      and instance.markup.preview()) or '')
                output.append("</span>",)
            else:
                output.insert(0,"<span style='float:left;'><ul style='margin-left:0px'>",)
                output.append("</ul></span><span>",)
                output.append(render_to_string('admin/svgfile/preview.html',
                                {}))
                output.append("</span>",)
            return mark_safe(u''.join(output))

        self.fields['components'].widget.widget.attrs.update({'style':'display:none'})
        self.fields['composers'].widget.widget.attrs.update({'style':'display:none'})
        if self.instance.id:
            self.fields['tree'].widget.components = self.instance.components
            self.fields['tree'].widget.composers = self.instance.composers
            self.fields['tree'].widget.composer = self.instance

    
    def clean(self, *args, **kwargs):
        return super(SVGComposerForm, self).clean(*args, **kwargs)