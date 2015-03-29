from django.template import Library, Node, TemplateSyntaxError
from banners.models import Slot
import re

register = Library()

class BannersForSlotNode(Node):
    def __init__(self, symbol, cast_as=None, options=None):
        self.symbol = symbol
        self.cast_as = cast_as
        self.options = options
    
    def render(self, context):
        try:
            banners = Slot.objects.get(symbol=self.symbol).published_banners
            if self.cast_as:
                context[self.cast_as] = banners
                return ''
            if self.options.has_key('limit'):
                banners = banners[:self.options['limit']]

            return banners
        except Slot.DoesNotExist:
            return ''

@register.tag
def banners_for_section(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]

    m = re.search(r'^(.*?) as (\w+)(.*)$', arg)
    if m:
        symbol, cast_as, opts = m.groups()
        opts_dict = {}
        for opt in opts.split(' '):
            if opt.find('=')==-1:
                opts_dict[opt]=True
            else:
                name, value = opt.split('=')
                opts_dict[str(name)] = value
        return BannersForSlotNode(symbol, cast_as, opts_dict)

    return BannersForSlotNode(arg)





