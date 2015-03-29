import xml.parsers.expat
from decimal import Decimal

from django.conf import settings
from django.template.loader import render_to_string
import xml.dom.minidom

import pprint
pp = pprint.PrettyPrinter(indent=1, width=20).pprint


def autofill_svg_size(sender, **kwargs):
    if not kwargs['instance'].autofill_dimensions:
        return
    
    dims = {}
    def start_element(name, attrs):
        if name == 'svg':
            if u'height' in attrs and u'width' in attrs:
                dims['height'] = attrs[u'height']
                dims['width'] = attrs[u'width']

                
    p = xml.parsers.expat.ParserCreate()    
    p.StartElementHandler = start_element
    p.Parse(kwargs['instance'].file.read())
    if 'height' in dims and 'width' in dims:
        #attention! measure unit is deleted! need to find - what measure units can be used for size
        #and how it can be implemented in svg-editor
        kwargs['instance'].height = Decimal(dims['height'].rstrip('px').rstrip('em').rstrip('%'))
        kwargs['instance'].width = Decimal(dims['width'].rstrip('px').rstrip('em').rstrip('%'))



class recompose(object):
    def __init__(self, modify_type):
        self.modify_type = modify_type
        self.sizes = []
        self.urls = []
    
    def __call__(self, *args, **kwargs):
        self.sizes = []
        self.urls = []
        content_tokens = []
        content_attr_name = kwargs['sender'].__name__.split("_")[-1]
        modified_contents = getattr(kwargs['instance'],
                           content_attr_name).filter(id__in=list(kwargs['pk_set']))
        for modified_content in modified_contents: 
            content_tokens += {"orm_id":unicode(modified_content.id),
                               "orm_page_id":unicode(modified_content.parent.id),
                               "orm_region":unicode(modified_content.region),
                               "orm_ordering":unicode(modified_content.ordering)},
            self.sizes += (modified_content.markup.height, 
                           modified_content.markup.width),
            self.urls += modified_content.markup.file.url,
        return self.modify(markup_path=kwargs['instance'].markup.file.path,
                           content_tokens=content_tokens,
                           modify_type=self.modify_type,
                           sizes =self.sizes,)
        
    def modify(self, markup_path="", content_tokens=[], sizes=[], modify_type=""):
        
        def marked_elements(root, element_name, content_tokens):
            for element in root.getElementsByTagName(element_name):
                attrs = dict(((attr_node.name, attr_node.value) for\
                            attr_node in element._attrs.values()))
                for content_token in content_tokens:
                    related_attrs = dict((a[0],a[1]) for a in attrs.items() if \
                                          a[0] in content_token \
                                          and a[1] == content_token[a[0]])
                    if len(related_attrs) == len(content_token):
                        yield element
                        

        def adder(doc):
            if not len(list(marked_elements(doc, 'image', content_tokens))):
                for content_token in content_tokens:
#                    print content_tokens.index(content_token)
#                    print self.urls
#                    print self.urls[content_tokens.index(content_token)]
                    image_node = xml.dom.minidom.parseString(render_to_string('svg/image_node.xml',
                                                                           {'token':content_token,
                                                                            'size':self.sizes[content_tokens.index(content_token)],
                                                                            'url':self.urls[content_tokens.index(content_token)]})).\
                                                                            childNodes[0].childNodes[0]
                    image_node.ownerDocument = None
                    image_node.parentNode = None
                    doc.childNodes[0].appendChild(image_node)
        def remover(doc):
            for element in marked_elements(doc, 'image', content_tokens):
                element.parentNode.removeChild(element)
        
        if modify_type == 'add':
            modifier = adder
        elif modify_type == 'remove':
            modifier = remover
        else:
            raise ValueError("'modify_type' must be either 'add' or 'remove' string")
        markup = open(markup_path)
        doc = xml.dom.minidom.parse(markup)
        markup.close()
        #markup = open(markup_path, mode='w')
        modifier(doc)
        markup = file(markup_path, mode='w')
        markup.write(doc.toprettyxml())
        markup.close()


RECOMPOSE_MAP = {('pre_remove', "SVGComposerContentType_composers"):recompose('remove'),
                 ('post_add', "SVGComposerContentType_composers"):recompose('add'),
                 ('pre_remove', "SVGComposerContentType_components"):recompose('remove'),
                 ('post_add', "SVGComposerContentType_components"):recompose('add'),}


def recompose_dispatcher(*args, **kwargs):
    if kwargs['instance'].__class__.__name__ == 'SVGComposerContentType':
        if  (kwargs['action'],kwargs['sender'].__name__) in RECOMPOSE_MAP:
                RECOMPOSE_MAP[(kwargs['action'],kwargs['sender'].__name__)](*args, **kwargs)
                
def create_markup_if_empty(*args, **kwargs):
    
    if kwargs['sender'].__name__ == 'SVGComposerContentType' and\
       not kwargs['instance'].markup and\
       not hasattr(kwargs['instance'],'_markup_resetted'):
        print "reset"    
        kwargs['instance'].reset_markup()
        setattr(kwargs['instance'],'_markup_resetted', True)
        kwargs['instance'].save()
