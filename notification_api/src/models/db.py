from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


def gen_uuid():
    return str(uuid4())


class NoticeType(BaseModel):
    type: str


class UserNoticeSettings(BaseModel):
    user_id: str
    excluded: List[NoticeType]


class Notice(BaseModel):
    id: str = Field(default_factory=gen_uuid, alias="_id")
    type: str
    name: str
    description: Optional[str]

    class Config:
        allow_population_by_field_name = True
