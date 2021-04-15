from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import parse_obj_as

from notification_api.src.exceptions import DocAlreadyExists, DocNotFound
from notification_api.src.models.api import ExcludedNoticeOut
from notification_api.src.services.user_notice import (
    UserNoticeService,
    get_user_notice_service,
)

user_notice_api = APIRouter()


@user_notice_api.get("/notice")
async def get_user_notice_list(
    user_notice_service: UserNoticeService = Depends(get_user_notice_service),
) -> List[ExcludedNoticeOut]:
    # TODO: User authorization
    user_id = "user-12345"
    excluded_notices = await user_notice_service.get_excluded_notices(user_id)
    return parse_obj_as(List[ExcludedNoticeOut], excluded_notices)


@user_notice_api.post("/notice/{notice_type}")
async def create_notice(
    notice_type: str,
    user_notice_service: UserNoticeService = Depends(get_user_notice_service),
):
    # TODO: User authorization
    user_id = "user-12345"
    try:
        await user_notice_service.activate(user_id, notice_type)
    except DocNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@user_notice_api.delete("/notice/{notice_type}")
async def delete_notice(
    notice_type: str,
    user_notice_service: UserNoticeService = Depends(get_user_notice_service),
):
    # TODO: User authorization
    user_id = "user-12345"
    try:
        await user_notice_service.deactivate(user_id, notice_type)
    except DocNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    except DocAlreadyExists:
        raise HTTPException(status.HTTP_409_CONFLICT)
