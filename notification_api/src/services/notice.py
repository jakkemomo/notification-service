import logging
from typing import List, Optional

from fastapi import Depends
from motor.core import AgnosticCollection as MongoCollection
from motor.core import AgnosticDatabase as MongoDatabase
from pydantic import parse_obj_as
from pymongo.errors import DuplicateKeyError
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from notification_api.src.db.mongo import get_mongo_conn
from notification_api.src.exceptions import DocAlreadyExists, DocNotFound
from notification_api.src.models.db import Notice
from notification_api.src.settings import settings

MONGO_DB = settings.mongo.db

logger = logging.getLogger(__name__)


class NoticeService:
    """Класс для управления уведомлениями."""

    collection_name = "notices"

    def __init__(self, db: MongoDatabase):
        self.db = db
        self.collection: MongoCollection = db[self.collection_name]

    async def get(self, notice_id: str) -> Optional[Notice]:
        """ Получить информацию о конкретном уведомлении """
        doc = await self.collection.find_one({"_id": notice_id})
        if not doc:
            msg = "Notice [%s] not found." % notice_id
            logger.info(msg)
            raise DocNotFound(msg=msg)

        return Notice.parse_obj(doc)

    async def get_all(self) -> List[Notice]:
        """ Получить полный список уведомлений """
        res = await self.collection.find().to_list(None)
        return parse_obj_as(List[Notice], res)

    async def create(self, notice_type: str, name: str, description: str = None):
        """ Создать новый тип уведомления """
        new_notice = Notice(
            type=notice_type,
            name=name,
            description=description,
        )

        try:
            res: InsertOneResult = await self.collection.insert_one(
                new_notice.dict(by_alias=True)
            )
        except DuplicateKeyError:
            msg = (
                "Try to create notice with already used type. Doc [%s]."
                % new_notice.dict(by_alias=True)
            )
            logger.info(msg)
            raise DocAlreadyExists(msg=msg)

        if not res.inserted_id:
            logger.warning(
                "New notice is not created. Doc: [%s]" % new_notice.dict(by_alias=True)
            )

    async def update(
        self, notice_id: str, notice_type: str, name: str, description: str = None
    ):
        """ Обновить информацию об уведомлении """
        updated_notice = Notice(
            type=notice_type,
            name=name,
            description=description,
        )

        try:
            res: UpdateResult = await self.collection.update_one(
                {"_id": notice_id},
                {"$set": updated_notice.dict()},
            )
        except DuplicateKeyError:
            msg = (
                "Try to set notice type with already used value. Doc [%s]."
                % updated_notice.dict(by_alias=True)
            )
            logger.info(msg)
            raise DocAlreadyExists(msg=msg)

        if not res.matched_count:
            msg = "Notice [%s] not found." % notice_id
            logger.info(msg)
            raise DocNotFound(msg=msg)

        if not res.modified_count:
            logger.warning("Notice [%s] was not modified." % notice_id)

    async def delete(self, notice_id: str):
        """ Удалить уведомление """
        res: DeleteResult = await self.collection.delete_one({"_id": notice_id})
        if not res.deleted_count:
            msg = "Notice [%s] not found." % notice_id
            logger.info(msg)
            raise DocNotFound(msg=msg)


def get_notice_service(mongo_conn=Depends(get_mongo_conn)) -> NoticeService:
    mongo_db = mongo_conn[MONGO_DB]
    return NoticeService(mongo_db)
