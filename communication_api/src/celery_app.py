from celery import Celery

from communication_api.src.settings import settings

RABBIT_URI = settings.rabbit.get_uri()
CELERY_CONF = settings.celery.conf

app = Celery(broker=RABBIT_URI)
