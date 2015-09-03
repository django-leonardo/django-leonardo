
from feincms.templatetags.feincms_page_tags import *


class LanguageLinksNode(SimpleAssignmentNodeWithVarAndArgs):
    """
    ::
        {% feincms_languagelinks for feincms_page as links [args] %}
    This template tag needs the translations extension.
    Arguments can be any combination of:
    * all or existing: Return all languages or only those where a translation
      exists
    * excludecurrent: Excludes the item in the current language from the list
    * request=request: The current request object, only needed if you are using
      AppContents and need to append the "extra path"
    The default behavior is to return an entry for all languages including the
    current language.
    Example::
      {% feincms_languagelinks for feincms_page as links all,excludecurrent %}
      {% for key, name, link in links %}
          <a href="{% if link %}{{ link }}{% else %}/{{ key }}/{% endif %}">
            {% trans name %}</a>
      {% endfor %}
    """

    def what(self, page, args):
        only_existing = args.get('existing', False)
        exclude_current = args.get('excludecurrent', False)

        # Preserve the trailing path when switching languages if extra_path
        # exists (this is mostly the case when we are working inside an
        # ApplicationContent-managed page subtree)
        trailing_path = ''
        request = args.get('request', None)
        if request:
            # optionaly if is there request use app extra
            try:
                # Trailing path without first slash
                trailing_path = request._feincms_extra_context.get(
                    'extra_path', '')[1:]
            except:
                pass

        translations = dict(
            (t.language, t) for t in page.available_translations())
        translations[page.language] = page

        links = []
        for key, name in settings.LANGUAGES:
            if exclude_current and key == page.language:
                continue

            # hardcoded paths... bleh
            if key in translations:
                links.append((
                    key,
                    name,
                    translations[key].get_absolute_url() + trailing_path))
            elif not only_existing:
                links.append((key, name, None))

        return links

register.tag(
    'feincms_languagelinks',
    do_simple_assignment_node_with_var_and_args_helper(LanguageLinksNode))
