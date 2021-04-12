from fastapi import APIRouter, Depends, Response, status

from notification_api.models.api import MessageIn
from notification_api.services.rabbit import RabbitService, get_rabbit_service

router = APIRouter()


@router.post("/notification")
async def send_notification(
    message: MessageIn,
    response: Response,
    rabbit: RabbitService = Depends(get_rabbit_service),
):
    # TODO: check if user want to receive the notifications
    await rabbit.send_message(message.type, message.dict())
    # TODO: Send to history

    response.status_code = status.HTTP_200_OK
    return response
