import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eLibrary.settings')

app = Celery('eLibrary')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'count_top3_books': {
        'task': 'api.tasks.get_top3_books',
        'schedule': crontab(hour='0-23', minute=0),
    },
}
