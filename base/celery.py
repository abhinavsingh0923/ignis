from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

app = Celery('base')  # Replace 'your_project' with your project's name.
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')

# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry = True

app.conf.broker_connection_retry_on_startup = True

# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)