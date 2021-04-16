from celery import Celery

from communication_api.settings import CELERY_CONF, RABBIT_URI

app = Celery(broker=RABBIT_URI)
app.config_from_object(CELERY_CONF)
