from celery import Celery

from communication_api.src import celery_app
from communication_api.src.models.api import NotificationIn
from communication_api.src.settings import settings

DELIVERY_TYPE_TASKS = settings.celery.delivery


class CeleryService:
    def __init__(self, app: Celery):
        self._app = app

    async def send_task(self, delivery_type: NotificationIn, message: dict):
        task_name = DELIVERY_TYPE_TASKS[delivery_type]
        queue = delivery_type.value
        self._app.send_task(f"{queue}.{task_name}", args=[message], queue=queue)


def get_celery_service() -> CeleryService:
    return CeleryService(celery_app.app)
