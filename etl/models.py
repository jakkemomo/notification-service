from typing import List

from pydantic import BaseModel


class EmailMessage(BaseModel):
    recipients: List
    subject: str
    template_name: str
    template: str
    template_data: dict
    body_html: str
    body_text: str
