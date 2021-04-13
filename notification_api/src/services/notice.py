import logging
from typing import List, Optional

from motor.core import AgnosticCollection as MongoCollection
from motor.core import AgnosticDatabase as MongoDatabase
from pydantic import parse_obj_as
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from notification_api.src.models.db import Notice

logger = logging.getLogger(__name__)


class NoticeService:
    """Класс для управления уведомлениями.

    Документ в хранилище MongoDb имеет следующую схему:
    {
        type: str
        name: str
        description: Optional[str]
    }
    - `type`:str: поле отвечающее за тип уведомления, например, "likes", "news", "comments";
    - `name`:str: название уведомления для отображения пользователю;
    - `description`:str: подробное описание уведомления для отображения пользователю.
    """

    COLLECTION_NAME = "notices"

    def __init__(self, db: MongoDatabase):
        self.db = db
        self.collection: MongoCollection = db[self.COLLECTION_NAME]

    async def get(self, notice_id: str) -> Optional[Notice]:
        """ Получить информацию о конкретном уведомлении """
        res = await self.collection.find_one({"_id": notice_id})
        if not res:
            logger.info("Notice [%s] not found." % notice_id)
            return None

        return Notice.parse_obj(res)

    async def get_all(self) -> List[Notice]:
        """ Получить полный список уведомлений """
        res = await self.collection.find({})
        return parse_obj_as(List[Notice], res)

    async def create(self, notice_type: str, name: str, description: str = None):
        """ Создать новый тип уведомления """
        new_notice = Notice(
            type=notice_type,
            name=name,
            description=description,
        )

        res: InsertOneResult = await self.collection.insert_one(new_notice.dict())
        if not res.inserted_id:
            logger.warning(
                "New notice is not created. Doc: [%s]" % (new_notice.dict(),)
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

        res: UpdateResult = await self.collection.find_one_and_update(
            {"_id": notice_id},
            {"$set": updated_notice.dict()},
        )
        if not res.modified_count:
            logger.info("Notice [%s] not found." % notice_id)

    async def delete(self, notice_id: str):
        """ Удалить уведомление """

        res: DeleteResult = await self.collection.delete_one({"_id": notice_id})
        if not res.deleted_count:
            logger.info("Notice [%s] not found." % notice_id)
