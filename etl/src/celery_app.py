from celery import Celery

from etl.src.settings import settings

broker_config = settings.broker
backend_config = settings.backend
celery_config = settings.celery

broker_url = f"{broker_config.scheme}://{broker_config.host}:{broker_config.port}"
backend_url = f"{backend_config.scheme}://{backend_config.host}:{backend_config.port}"

app = Celery("tasks", broker=broker_url, backend=backend_url)

app.conf.task_routes = celery_config.task_routes
