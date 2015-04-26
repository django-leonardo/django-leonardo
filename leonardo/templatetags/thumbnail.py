from django.template import Library

try:
    from sorl.thumbnail.templatetags.thumbnail import thumbnail as sorl_thumb
    SORL = True
except Exception:
    SORL = False

try:
    from easy_thumbnails.templatetags.thumbnail import thumbnail as easy_thumb
    EASY = True
except Exception:
    EASY = False


register = Library()


# support for both tag style

def thumbnail(parser, token):
    thumb = None
    if SORL:
        try:
            thumb = sorl_thumb(parser, token)
        except Exception:
            thumb = False
    if EASY and not thumb:
        thumb = easy_thumb(parser, token)
    return thumb

register.tag(thumbnail)
