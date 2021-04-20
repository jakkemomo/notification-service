import logging
from typing import List

from fastapi import Depends
from motor.core import AgnosticCollection as MongoCollection
from motor.core import AgnosticDatabase as MongoDatabase
from pydantic import parse_obj_as
from pymongo.results import InsertOneResult, UpdateResult

from notification_api.src.db.mongo import get_mongo_conn
from notification_api.src.exceptions import DocAlreadyExists, DocNotFound
from notification_api.src.models.db import ExcludedNotice, UserNoticeSettings
from notification_api.src.services.notice import (
    NoticeService,
    get_notice_service,
)
from notification_api.src.settings import settings

MONGO_DB = settings.mongo.db

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

    collection_name = "user_notices"

    def __init__(self, db: MongoDatabase, notice_service: NoticeService):
        self._db = db
        self._collection: MongoCollection = db[self.collection_name]
        self._notice_service = notice_service

    async def activate(self, user_id: str, notice_id: str):
        """ Включить пользователю уведомление `notice_id` """

        notice = await self._notice_service.get(notice_id)
        excluded_notice = ExcludedNotice.parse_obj(notice)

        res: UpdateResult = await self._collection.update_one(
            {"user_id": user_id},
            {"$pull": {"excluded": excluded_notice.dict()}},
        )

        # Так как `user_id` получается из токена, то считаем, что он задан верно.
        # При выполнении условия считаем, что у пользователя еще не было отключенных
        # уведомлений, т.е. все уведомления включены.
        if not res.matched_count or not res.modified_count:
            msg = "User [%s] tries to turn on already active [%s] notice." % (
                user_id,
                notice_id,
            )
            logger.info(msg)
            raise DocNotFound(msg=msg)

    async def deactivate(self, user_id: str, notice_id: str):
        """ Отключить у пользователя уведомления данного типа """
        notice = await self._notice_service.get(notice_id)
        excluded_notice = ExcludedNotice.parse_obj(notice)

        res: UpdateResult = await self._collection.update_one(
            {"user_id": user_id},
            {"$addToSet": {"excluded": excluded_notice.dict()}},
        )

        # Так как `user_id` получается из токена, то считаем, что он задан верно.
        # При выполнении условия считаем, что у пользователя еще не было отключенных
        # уведомлений. Создаем для него новый документ.
        if not res.matched_count:
            logger.info(
                "User [%s] has not any turned notice off. Created a new one." % user_id
            )
            await self._create_new_notice_settings(user_id, excluded_notice)

        if not res.modified_count:
            msg = "User [%s] already has the turned notice [%s] off." % (
                user_id,
                notice_id,
            )
            logger.info(msg)
            raise DocAlreadyExists(msg=msg)

    async def get_excluded_notices(self, user_id: str) -> List[ExcludedNotice]:
        """ Получение списка уведомлений, отключенных пользователем """
        res = await self._collection.find_one({"user_id": user_id})
        if not res:
            return []
        return parse_obj_as(List[ExcludedNotice], res["excluded"])

    async def _create_new_notice_settings(self, user_id: str, notice: ExcludedNotice):
        """ Создание нового документа с настройками уведомлений пользователя """
        new_doc = UserNoticeSettings(
            user_id=user_id,
            excluded=[notice],
        )

        res: InsertOneResult = await self._collection.insert_one(new_doc.dict())
        if not res.inserted_id:
            logger.warning(
                "User [%s] notice settings is not created. Doc: [%s]"
                % (user_id, new_doc.dict())
            )


def get_user_notice_service(
    mongo_conn=Depends(get_mongo_conn),
    notice_service=Depends(get_notice_service),
) -> UserNoticeService:
    mongo_db = mongo_conn[MONGO_DB]
    return UserNoticeService(mongo_db, notice_service)
