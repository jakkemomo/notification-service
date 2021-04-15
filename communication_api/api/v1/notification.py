from fastapi import APIRouter, Depends, status

from communication_api.models.api import NotificationIn
from communication_api.services.history import (
    HistoryService,
    get_history_service,
)
from communication_api.services.rabbit import RabbitService, get_rabbit_service
from communication_api.utils.notifications import check_user_notifications

router = APIRouter()


@router.post("/notification")
async def send_notification(
    notification: NotificationIn,
    rabbit: RabbitService = Depends(get_rabbit_service),
    history_service: HistoryService = Depends(get_history_service),
):
    # TODO: Hide in service
    filtered_recipients = []
    for user_id in notification.message.recipients:
        excluded_notices = await check_user_notifications(user_id)
        if notification.content_type in excluded_notices:
            continue
        filtered_recipients.append(user_id)

    if filtered_recipients:
        notification.message.recipients = filtered_recipients
        # TODO: Error processing
        await rabbit.send_message(notification.delivery_type, notification.dict())

    # TODO: Error processing
    await history_service.add(**notification.dict())

    return status.HTTP_200_OK
