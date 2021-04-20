from typing import List

from pydantic import BaseModel

from communication_api.src.models.common import ContentType, DeliveryType


class MessageIn(BaseModel):
    recipients: List[str]
    template_name: str
    template_data: dict


class NotificationIn(BaseModel):
    delivery_type: DeliveryType
    content_type: ContentType
    message: MessageIn
