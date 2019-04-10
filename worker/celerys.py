import os
from time import sleep

from celery import Celery

from worker import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")
BROKER_URL = 'redis://127.0.0.1:6379/1'
BACKEND_URL = 'redis://127.0.0.1:6379/1'

celery_app = Celery(broker=BROKER_URL,backend=BACKEND_URL)




# celery_app = Celery()
# celery_app.config_from_object(config)



# celery_app.autodiscover_tasks()




@celery_app.task
def add(x,y):
    sleep(10)
    return x+y


