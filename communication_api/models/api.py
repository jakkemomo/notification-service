from typing import List

from pydantic import BaseModel

from .common import MsgTypes


class MessageIn(BaseModel):
    type: MsgTypes
    src_service: str
    dst: List[str]
    template_name: str
    template_data: dict
