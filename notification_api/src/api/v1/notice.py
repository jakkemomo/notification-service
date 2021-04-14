from typing import List

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from notification_api.src.models.api import NoticeIn, NoticeOut
from notification_api.src.services.notice import (
    NoticeService,
    get_notice_service,
)

notice_api = APIRouter()


@notice_api.get("/notice")
async def get_notice_list(
    notice_service: NoticeService = Depends(get_notice_service),
) -> List[NoticeOut]:
    notices = await notice_service.get_all()
    result = parse_obj_as(List[NoticeOut], notices)
    return result


@notice_api.post("/notice")
async def create_notice(
    notice: NoticeIn,
    notice_service: NoticeService = Depends(get_notice_service),
):
    await notice_service.create(
        notice_type=notice.type,
        name=notice.name,
        description=notice.description,
    )


@notice_api.put("/notice/{notice_id}")
async def update_notice(
    notice_id: str,
    notice: NoticeIn,
    notice_service: NoticeService = Depends(get_notice_service),
):
    await notice_service.update(
        notice_id=notice_id,
        notice_type=notice.type,
        name=notice.name,
        description=notice.description,
    )


@notice_api.delete("/notice/{notice_id}")
async def delete_notice(
    notice_id: str,
    notice_service: NoticeService = Depends(get_notice_service),
):
    await notice_service.delete(notice_id)
