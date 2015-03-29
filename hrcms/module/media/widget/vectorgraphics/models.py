import os

from itertools import chain

from django.utils.translation import ugettext_lazy as _
from django.db import models

from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape

from django.conf import settings
from django.template.loader import render_to_string

from django.contrib import messages
from django.db.models.signals import pre_save, post_save, m2m_changed
 
from django.db.models.loading import cache as apps_cache

from feincms.module.page.models import Page

#from forms import SVGPreviewAdminForm, SVGComposerForm
#from util import autofill_svg_size, recompose_dispatcher, create_markup_if_empty

from webcms.module.media.models import File

from webcms.models import Widget

from feincms.admin.item_editor import ItemEditorForm
from feincms._internal import monkeypatch_method
from feincms.module.page.models import Page


#import pprint
#pp = pprint.PrettyPrinter(indent=1, width=20).pprint

# Create your models here.

"""

SVG_MEDIA = getattr(settings, 'SVG_MEDIA', 'svgmedia')
SVG_IMAGES_PATH = getattr(settings, 'SVG_IMAGES_PATH', 'img/svg')
SVG_EDITOR_PATH = getattr(settings, 'SVG_EDITOR_PAGE_URL', os.path.join(SVG_MEDIA, 
                                                                        'svg-editor/svg-editor.html'))

class SVGFileBase(models.Model):
    class Meta:
        abstract = True
    
    file = models.FileField(_('SVG file'), 
                            upload_to=SVG_IMAGES_PATH)
    
    width = models.DecimalField(blank=True, 
                                null=True,
                                max_digits=9,
                                decimal_places=5) 
    height = models.DecimalField(blank=True, 
                                 null=True,
                                 max_digits=9, 
                                 decimal_places=5)
    autofill_dimensions = models.BooleanField(default=True)

    def name(self):
        return os.path.basename(self.file.path)
    
    def __unicode__(self):
        return self.name()
    
    def preview(self, remove_xml_decl=True):
        return render_to_string('admin/svgfile/preview.html',
                                {'file':self.file,
                                 'width':self.width,
                                 'height':self.height,}) 
    
    def link(self):
        return render_to_string('admin/svgfile/link.html',
                                {'file_url':self.file.url}) 
    

    def edit_link(self):
        return render_to_string('admin/svgfile/edit_link.html',
                                {'svg':self,
                                 'editor_page_url':os.path.join(settings.MEDIA_URL,
                                                                SVG_EDITOR_PATH)}) 
    
    def save_from_editor(self, svg, check_xml_header=True):
            try:
                f = file(self.file.path,'w')
                if check_xml_header and not svg.lstrip().startswith('<?xml'): 
                    f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
                f.write(svg)
                f.close()
                self.save()
                return messages.success, '%s saved succesfully'% self
            except Exception, e:
                    return messages.error, '%s save error:<br/><pre>%s</pre>'% \
                                            (self, unicode(e))
            finally:
                f.close()
    def svgmodel(self):
        return self._meta.module_name


    def render(self):
        return "\n".join(self.file.readlines()[1:])

class SVGFile(SVGFileBase):
    pass

class SVGComposerFile(SVGFileBase):
    pass

pre_save.connect(autofill_svg_size, sender=SVGFile)
pre_save.connect(autofill_svg_size, sender=SVGComposerFile)

"""

class ManyToManyField(models.ManyToManyField):
    def save_form_data(self, *args, **kwargs):
        remove=list(set(getattr(args[0], self.attname).all()) - set(args[1]))
        add=list(set(args[1]) - set(getattr(args[0], self.attname).all()))
        getattr(args[0],self.attname).remove(*remove)
        getattr(args[0],self.attname).add(*add)

class SVGPreviewAdminForm(ItemEditorForm):
    def __init__(self, *args, **kwargs):    
        super(SVGPreviewAdminForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', False) or (len(args) and args[0]) or False  
               
        orig_render_options = self.fields['markup'].widget.widget.render_options
        widget = self.fields['markup'].widget.widget

        """
        @monkeypatch_method(self.fields['markup'].widget.widget)
        def render_options(choices, selected_choices):
            def render_option(option_value, option_label):
                try:
                    id = int(option_value)
                except ValueError:
                    id = None
                if id:
                    svgfile = File.objects.get(id=id)
#                    option_src = svgfile.file.url
#                    option_width = svgfile.width
#                    option_height = svgfile.height
                else:
                    option_src = None
                    
                
                option_value = force_unicode(option_value)
                selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
#                if option_src:
#                    selected_html += ' src="%s" width="%s" height="%s"'%(option_src,
#                                                                         option_width,
#                                                                         option_height,)
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
            kwargs['attrs'] = {'onchange':mark_safe(render_to_string('admin/svg/render_option_with_preview.html',
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
                output.append(render_to_string('admin/svg/preview.html',
                                {}))
                output.append("</span>",)
            return mark_safe(u''.join(output))
        """

class VectorGraphicsWidget(Widget):
    markup = models.ForeignKey(File)
#    feincms_item_editor_form = SVGPreviewAdminForm
#    svg_content_type = "components" 

    class Meta:
        abstract = True
        verbose_name = _('Vector graphics')
        verbose_name_plural = _('Vector graphics')

#    def render(self, **kwargs):
#        return mark_safe(self.fragment_text)

"""
UNABSTRACTED_MODELS = []

def unabstract_model(model, base_model, models_selector=None):
    '''
    returns real model either from 'content_type_for' of model or unmanaged model 
    with guessed table name
    @param model: abstract model of content type
    @param base_model: feincms.models.Base subclass (e.g. Page)
    '''

    global UNABSTRACTED_MODELS
    UNABSTRACTED_MODELS += model,
    class Unabstracted(models.Model):
        #_module = base_model 
        __name__ = model.__name__
        class Meta:
            abstract = False
            managed = False
            db_table = "%s_%s"%(Page._meta.db_table, model.__name__.lower())
            
    
    Unabstracted._meta.module_name = model._meta.module_name
    Unabstracted._meta.object_name = model._meta.object_name
    Unabstracted._meta.verbose_name = model._meta.verbose_name
    try:
        #this model doesnot really exists
        del apps_cache.app_models['unabstracted']
    except KeyError:
        pass
    return Unabstracted


class UnabstractModelMetaclass(models.Model.__metaclass__):
    def __new__(cls, *args, **kwargs):
        real_svgcontenttype = Page.content_type_for(SVGContentType)
        if real_svgcontenttype:
             
            class SVGComposerContentType(models.Model):
                feincms_item_editor_form = SVGComposerForm
                feincms_item_editor_includes = {'head':
                                                ['admin/feincms/page/svgcomposercontenttype/init_composer_content_type.html']
                                                }
                svg_content_type = "composers"
                class Meta:
                    abstract = True
                    verbose_name = _('SVG composer')
                    verbose_name_plural = _('SVG composers')
                
                components = ManyToManyField(real_svgcontenttype,
                                                blank=True,
                                                null=True,
                                                verbose_name = 'Components',)

                composers = ManyToManyField('self',
                                            blank=True,
                                            null=True,)
                
                markup = models.ForeignKey(SVGComposerFile, blank=True, null=True)
                
                def reset_markup(self):
                    composer = self
                    class UploadedFileEmulator():
                        def __len__(self):
                            return 1
                        def chunks(self):
                            yield render_to_string('empty_composer.svg', 
                                                   {'composer':composer,
                                                    'settings':settings} )
                    markup = SVGComposerFile()
                    
                    markup.file.save("%s_%s_%s.svg"%(self.parent.slug,
                                                          self.region,
                                                          self.ordering,),
                                     UploadedFileEmulator())
                    self.markup = markup
                    

            args = list(args)
            args[1] = list(args[1])
            args[1][0] = SVGComposerContentType
            args[1] = tuple(args[1])
            

            
        return models.Model.__metaclass__.__new__(cls, *tuple(args), **kwargs)


class SVGComposerContentType(models.Model):
    __metaclass__=UnabstractModelMetaclass    
    feincms_item_editor_form = SVGComposerForm
    svg_content_type = "composers"
    feincms_item_editor_includes = {'head':
                                    ['admin/feincms/page/svgcomposercontenttype/init_composer_content_type.html']
                                    }
    class Meta:
        abstract = True
        verbose_name = _('SVG composer')
        verbose_name_plural = _('SVG composers')
    
    components = ManyToManyField(unabstract_model(SVGContentType, Page),
                                    blank=True,
                                    null=True,)

    composers = ManyToManyField('self',
                                        blank=True,
                                        null=True,)
    
    markup = models.ForeignKey(SVGComposerFile, blank=True, null=True)
        
        
m2m_changed.connect(recompose_dispatcher)
post_save.connect(create_markup_if_empty)

def fix_apps_cache(*args, **kwargs):
    #fix apps_cache to hide unabstracted models
    for k in filter(lambda x: bool(x[0]), apps_cache._get_models_cache.keys()):
        if os.path.abspath(k[0].__file__).rstrip('c') == \
            os.path.abspath(__file__).rstrip('c'):
            unabstracted_indexes = []
            for model in apps_cache._get_models_cache[k]:
                i = 0
                if model.__name__ in map(lambda x: x.__name__, UNABSTRACTED_MODELS):
                    unabstracted_indexes += i,
                else:
                    i += 1
            shifter = 0
            for index in unabstracted_indexes:        
                del apps_cache._get_models_cache[k][index-shifter]
                shifter += 1
    if 'unabstracted' in apps_cache.app_models['svg']:      
        del apps_cache.app_models['svg']['unabstracted']
models.signals.post_syncdb.connect(fix_apps_cache)

"""
