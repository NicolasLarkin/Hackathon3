import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fullstack.settings')

app = Celery('fullstack')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
