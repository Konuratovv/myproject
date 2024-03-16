from __future__ import absolute_import
import os
from celery.schedules import crontab

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every':{
        'task': 'apps.users.tasks.spam_email',
        'schedule': 2.0
    }
}

