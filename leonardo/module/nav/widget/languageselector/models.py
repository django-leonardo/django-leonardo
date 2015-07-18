# -#- coding: utf-8 -#-

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import Widget, Page


class LanguageSelectorWidget(Widget):

    """blueprint on new field ``excludecurrent`` boolean
    """

    class Meta:
        abstract = True
        verbose_name = _("Language switch")
        verbose_name_plural = _("Language switches")

    def render_content(self, options):
        request = options['request']
        try:
            language = request.session['django_language']
        except:
            language = settings.LANGUAGE_CODE
        languages = {}
        for lang in settings.LANGUAGES:
            languages[lang[0]] = {
                'label': lang[1],
                'code': lang[0],
            }
        page = Page.objects.best_match_for_path(request.path, raise404=True)
        suffix = request.path.replace(page.get_absolute_url(), '')

        if page.language == settings.LANGUAGE_CODE:
            languages[page.language]['page'] = page
            languages[page.language]['suffix'] = suffix
            translated_pages = page.translations.all()
            for trans_page in translated_pages:
                languages[trans_page.language]['page'] = trans_page
                languages[trans_page.language]['suffix'] = suffix
        else:
            if page.translation_of:
                main_page = page.translation_of
                languages[main_page.language]['page'] = main_page
                languages[main_page.language]['suffix'] = suffix
                translated_pages = main_page.translations.all()
                for trans_page in translated_pages:
                    languages[trans_page.language]['page'] = trans_page
                    languages[trans_page.language]['suffix'] = suffix

        return render_to_string(self.get_template_name(), {
            'widget': self,
            'page': page,
            'request': request,
            'language': language,
            'languages': languages
        })
