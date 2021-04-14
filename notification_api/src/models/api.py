from typing import Optional

from pydantic import BaseModel


class NoticeOut(BaseModel):
    id: str
    type: str
    name: str
    description: Optional[str]


class NoticeIn(BaseModel):
    type: str
    name: str
    description: Optional[str]


class ExcludedNoticeOut(BaseModel):
    type: str


class UserNoticeIn(BaseModel):
    type: str
    name: str
    description: Optional[str]
