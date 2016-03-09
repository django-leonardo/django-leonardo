
from django_select2.forms import Select2Mixin


def patch_select2():
    Select2Mixin.build_attrs = build_attrs


def build_attrs(self, extra_attrs=None, **kwargs):
    """Add select2 data attributes.
    set default width to 100%
    """
    attrs = super(Select2Mixin, self).build_attrs(
        extra_attrs=extra_attrs, **kwargs)
    if self.is_required:
        attrs.setdefault('data-allow-clear', 'false')
    else:
        attrs.setdefault('data-allow-clear', 'true')
        attrs.setdefault('data-placeholder', '')

    attrs.setdefault('data-width', "100%")
    attrs.setdefault('data-minimum-input-length', 0)
    if 'class' in attrs:
        attrs['class'] += ' django-select2'
    else:
        attrs['class'] = 'django-select2'
    return attrs
