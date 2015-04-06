import string

from django.db.models import Q

from django.views.generic.list_detail import object_list
from django.db import connection, transaction
from django.utils.translation import get_language_from_request
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from webcms.module.glossary.models import Term, TermTranslation

def term_list(request, **kwargs):
    """
    Return a list of all terms

    """

    ec = {"a_z": string.lowercase}

    lang = get_language_from_request(request)
    """
    raw_terms = TermTranslation.objects.order_by('slug')


    if "q" in request.GET:
        query = request.GET['q']
        ec['query'] = query
        terms = terms.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(synonyms__title__icontains=query)
        ).distinct()
    else:
        initial = request.GET.get("l", "a").lower()
        ec['starts_with'] = initial
#        terms = terms.filter(title__istartswith=ec['starts_with'])
    """
#    terms = terms.extra(select={"lower_title": "LOWER(%s.title)" % Term._meta.db_table }).order_by("lower_title")

    t = terms = Term.objects.all()
    used_letters = []
    for i in ec["a_z"]:
        try:
            x = t.filter(title__istartswith=i)
            if x:
                used_letters.append(i)
        except:
            pass

    context = RequestContext(request, {
        'object_list': terms,
        'ec': ec,
#        'starts_with': ec['starts_with'],
        'a_z': ec['a_z'],
        'used_letters': used_letters
    })
    return render_to_response('glossary/term_list.html', {}, context_instance = context)
#    return object_list(request, queryset=terms, extra_context= extra_context, **kwargs)
