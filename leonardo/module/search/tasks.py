from __future__ import absolute_import

import os
from celery import shared_task
from django.core import management
from leonardo.decorators import catch_result
from django.conf import settings


@shared_task
@catch_result
def sync_search_indexes():
    management.call_command('rebuild_index', interactive=False)

    # patch whoosh backend
    haystack = getattr(settings, 'HAYSTACK_CONNECTIONS', None)

    if 'default' in haystack and 'whoosh' in haystack['default']['ENGINE']:

        try:
            os.remove(os.path.join(
                haystack['default']['PATH'], 'MAIN_WRITELOCK'))
        except:
            pass

    return {'result': 'Rebuild index OK'}
