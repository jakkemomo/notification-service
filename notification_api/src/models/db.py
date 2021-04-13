from typing import List, Optional

from pydantic import BaseModel


class NoticeType(BaseModel):
    type: str


class UserNoticeSettings(BaseModel):
    user_id: str
    excluded: List[NoticeType]


class Notice(BaseModel):
    _id: str
    type: str
    name: str
    description: Optional[str]
