from __future__ import absolute_import

from celery import shared_task
from django.core import management
from leonardo.decorators import catch_result


@shared_task
@catch_result
def sync_search_indexes():
    management.call_command('rebuild_index', interactive=False)
    return {'result': 'Rebuild index OK'}
