from typing import List

from pydantic import BaseModel


class NoticeType(BaseModel):
    type: str


class UserNoticeSettings(BaseModel):
    user_id: str
    excluded: List[NoticeType]
