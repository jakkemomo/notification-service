from typing import List

from aiohttp.client import ClientSession

from communication_api.src.settings import NOTIFICATION_API_HOST, NOTIFICATION_API_PORT


async def check_user_notifications(user_id: str):
    """ Получение из Notification API список отключенных уведомлений пользователя """
    async with ClientSession() as session:
        uri = "http://%s:%s/service/user/%s/notice" % (
            NOTIFICATION_API_HOST,
            NOTIFICATION_API_PORT,
            user_id
        )
        async with session.get(uri) as resp:
            excluded_notices = await resp.json()
            return excluded_notices


async def filter_recipients(content_type: str, recipients: List[str]):
    """ Фильтрация получателей уведомления с содержимым типа `content_type` """
    filtered_recipients = []
    for user_id in recipients:
        excluded_notices = await check_user_notifications(user_id)
        if content_type in excluded_notices:
            continue
        filtered_recipients.append(user_id)
    return filtered_recipients
