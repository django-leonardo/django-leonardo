from __future__ import absolute_import

from celery import shared_task
from django.core import management


@shared_task
def sync_search_indexes():
    management.call_command('rebuild_index', interactive=False)
    return {'result': 'Rebuild index OK'}
