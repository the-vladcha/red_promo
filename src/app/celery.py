import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'update-item-status-every-day': {
        'task': 'library.tasks.update_item_status',
        'schedule': crontab(minute="0", hour="2"),
    },
}
