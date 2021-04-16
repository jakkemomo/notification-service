from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import parse_obj_as

from notification_api.src.exceptions import DocAlreadyExists, DocNotFound
from notification_api.src.models.api import NoticeIn, NoticeOut
from notification_api.src.services.notice import (
    NoticeService,
    get_notice_service,
)

notice_api = APIRouter()


@notice_api.get("/notice", response_model=List[NoticeOut])
async def get_notice_list(
    notice_service: NoticeService = Depends(get_notice_service),
) -> List[NoticeOut]:
    notices = await notice_service.get_all()
    result = parse_obj_as(List[NoticeOut], notices)
    return result


@notice_api.post("/notice", status_code=status.HTTP_201_CREATED)
async def create_notice(
    notice: NoticeIn,
    notice_service: NoticeService = Depends(get_notice_service),
):
    try:
        await notice_service.create(
            notice_type=notice.type,
            name=notice.name,
            description=notice.description,
        )
    except DocAlreadyExists:
        raise HTTPException(status.HTTP_409_CONFLICT)


@notice_api.put("/notice/{notice_id}")
async def update_notice(
    notice_id: str,
    notice: NoticeIn,
    notice_service: NoticeService = Depends(get_notice_service),
):
    try:
        await notice_service.update(
            notice_id=notice_id,
            notice_type=notice.type,
            name=notice.name,
            description=notice.description,
        )
    except DocAlreadyExists:
        raise HTTPException(status.HTTP_409_CONFLICT)
    except DocNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@notice_api.delete("/notice/{notice_id}")
async def delete_notice(
    notice_id: str,
    notice_service: NoticeService = Depends(get_notice_service),
):
    try:
        await notice_service.delete(notice_id)
    except DocNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
