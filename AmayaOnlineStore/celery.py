import os
from celery import Celery

#set the default Django setting module for the 'celery' program
os.environ.setdefault('DJANGO.SETTING_MODULE', 'AmayaOnlineStore.settings.py')

app = Celery('AmayaOnlineStore')

# load any custom configuration from our project settings using the config_from_object() method.
app.config_from_object('django.conf:settings', namespace='CELERY')

#with autodiscover, celery will look for a task.py in each app
app.autodiscover_tasks()
