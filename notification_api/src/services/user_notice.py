import logging
from typing import List

from motor.core import AgnosticCollection as MongoCollection
from motor.core import AgnosticDatabase as MongoDatabase
from pymongo.results import InsertOneResult, UpdateResult

from notification_api.src.models.db import NoticeType, UserNoticeSettings

logger = logging.getLogger(__name__)


class UserNoticeService:
    """
    Класс для управления уведомлениями пользователя.

    Выполняется хранение только тех типов уведомлений, которые отключены пользователем,
    таким образом упрощается сохранение согласованности данных при добавлении новых
    пользователей и типов уведомлений.

    При создании нового пользователя по умолчанию все уведомления включены,
    т.о. в коллекции не будет документа с отключенными типами уведомлений.
    Так же при добавлении нового типа уведомления, оно не будет помечено
    как отключенное пользователем и будет доставляться пользователю.

    В случае хранения полного списка включенных/отключенных уведомлений возникает проблема
    добавления новых типов уведомлений в документы с настройками пользователей.
    """

    COLLECTION_NAME = "user_notices"

    def __init__(self, db: MongoDatabase):
        self.db = db
        self.collection: MongoCollection = db[self.COLLECTION_NAME]

    async def activate(self, user_id: str, notice_type: str):
        """ Включить пользователю уведомления данного типа """
        excluded_notice = NoticeType(type=notice_type)

        res: UpdateResult = await self.collection.update_one(
            {"user_id": user_id},
            {"$pull": {"excluded": excluded_notice.dict()}},
        )
        if not res.modified_count:
            logger.info(
                "User [%s] had not the turned off [%s] notice." % (user_id, notice_type)
            )

    async def deactivate(self, user_id: str, notice_type: str):
        """ Отключить у пользователя уведомления данного типа """
        excluded_notice = NoticeType(type=notice_type)

        res: UpdateResult = await self.collection.update_one(
            {"user_id": user_id},
            {"$addToSet": {"excluded": excluded_notice.dict()}},
        )
        if not res.modified_count:
            logger.info(
                "User [%s] had not a turned notice off. Creating a new one."
                % (user_id,)
            )
            await self._create_new_notice_settings(user_id, notice_type)

    async def get_excluded_notices(self, user_id: str) -> List[NoticeType]:
        """ Получение типов уведомлений, отключенных пользователем """
        res = await self.collection.find_one({"user_id": user_id})
        if not res:
            return []
        return res["excluded"]

    async def _create_new_notice_settings(self, user_id: str, notice_type: str):
        """ Создание нового документа с настройками уведомлений пользователя """
        new_doc = UserNoticeSettings(
            user_id=user_id,
            excluded=[
                NoticeType(
                    type=notice_type,
                )
            ],
        )

        res: InsertOneResult = await self.collection.insert_one(new_doc.dict())
        if not res.inserted_id:
            logger.warning(
                "User [%s] notice settings is not created. Doc: [%s]"
                % (user_id, new_doc.dict())
            )
