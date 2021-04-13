from typing import List, Optional

from pydantic import BaseModel


class EmailMessage(BaseModel):
    recipients: List
    subject: str
    template_name: str
    template: Optional[str]
    template_data: dict
    body_html: Optional[str]
    body_text: Optional[str]
