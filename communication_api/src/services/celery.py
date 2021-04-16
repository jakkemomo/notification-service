from celery import Celery

from communication_api.src import celery_app
from communication_api.src.settings import settings

DELIVERY_TYPE_TASKS = settings.celery.delivery


class CeleryService:
    def __init__(self, app: Celery):
        self._app = app

    async def send_task(self, delivery_type: str, message: dict):
        task_name = DELIVERY_TYPE_TASKS[delivery_type]
        self._app.send_task(task_name, kwargs=message)


def get_celery_service() -> CeleryService:
    return CeleryService(celery_app.app)
