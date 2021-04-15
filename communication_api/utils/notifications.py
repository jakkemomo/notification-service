from aiohttp.client import ClientSession


async def check_user_notifications(user_id: str):
    """ Получает от Notification API список отключенных уведомлений пользователя"""
    async with ClientSession() as session:
        async with session.get(f"http://localhost:8000/service/user/{user_id}/notice") as resp:
            excluded_notices = await resp.json()
            return excluded_notices
