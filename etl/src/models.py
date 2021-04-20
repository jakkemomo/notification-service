from typing import List

from pydantic import BaseModel


class MessageIn(BaseModel):
    recipients: List[str]
    template_name: str
    template_data: dict


class EnrichableMessage(MessageIn):
    body_html: str


class EmailMessage(EnrichableMessage):
    subject: str
    body_html: str


class WebsocketMessage(EnrichableMessage):
    pass
