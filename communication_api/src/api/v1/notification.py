from fastapi import APIRouter, Depends

from communication_api.src.models.api import NotificationIn
from communication_api.src.services.celery import (
    CeleryService,
    get_celery_service,
)
from communication_api.src.services.history import (
    HistoryService,
    get_history_service,
)
from communication_api.src.utils.filter import filter_recipients

router = APIRouter()


@router.post("/notification")
async def send_notification(
    notification: NotificationIn,
    celery: CeleryService = Depends(get_celery_service),
    history_service: HistoryService = Depends(get_history_service),
):
    notification.message.recipients = await filter_recipients(
        notification.content_type,
        notification.message.recipients,
    )

    if notification.message.recipients:
        await celery.send_task(notification.delivery_type, notification.message.dict())

    await history_service.add(**notification.dict())
