from typing import List

from aiohttp.client import ClientSession

from communication_api.src.settings import settings

NOTIFICATION_API_URI = settings.notification_app.get_uri()


async def check_user_notifications(session: ClientSession, user_id: str):
    """ Получение из Notification API список отключенных уведомлений пользователя """
    uri = NOTIFICATION_API_URI.format(user_id=user_id)
    async with session.get(uri) as resp:
        excluded_notices = await resp.json()
        return excluded_notices


async def filter_recipients(content_type: str, recipients: List[str]):
    """ Фильтрация получателей уведомления с содержимым типа `content_type` """
    filtered_recipients = []
    async with ClientSession() as session:
        for user_id in recipients:
            excluded_notices = await check_user_notifications(session, user_id)
            if content_type in excluded_notices:
                continue
            filtered_recipients.append(user_id)
    return filtered_recipients
