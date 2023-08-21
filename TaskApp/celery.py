import os
from celery import Celery
from celery import schedules

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskApp.settings')
app = Celery('TaskApp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-letter-every-week': {
        'task': 'users.tasks.send_marketing_email',
        'schedule': schedules.crontab(minute='0', hour='20', day_of_week='1')
    }

}