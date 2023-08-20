import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'send_verification_email.settings')

app = Celery('send_verification_email')
app.config_from_object('django.conf.settings', namespace=Celery)
app.autodiscover_tasks()
