from typing import List

from pydantic import BaseModel


class MessageIn(BaseModel):
    recipients: List[str]
    template_name: str
    template_data: dict


class EmailMessage(MessageIn):
    subject: str
    body_html: str
