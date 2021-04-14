from typing import List

from fastapi import APIRouter, Depends

from notification_api.src.services.user_notice import (
    UserNoticeService,
    get_user_notice_service,
)

service_api = APIRouter()


@service_api.get("/user/{user_id}/notice")
async def get_specified_user_notice_list(
    user_id: str,
    user_notice_service: UserNoticeService = Depends(get_user_notice_service),
) -> List[str]:
    excluded_notices = await user_notice_service.get_excluded_notices(user_id)
    res = [notice.type for notice in excluded_notices]
    return res
