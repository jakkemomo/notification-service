import logging

from fastapi import Depends
from motor.core import AgnosticCollection as MongoCollection
from motor.core import AgnosticDatabase as MongoDatabase
from pymongo.results import InsertOneResult

from communication_api.src.db.mongo import get_mongo_conn
from communication_api.src.settings import settings

MONGO_DB = settings.mongo.db

logger = logging.getLogger(__name__)


class HistoryService:
    """ Класс для сохранения истории уведомлений """

    COLLECTION_NAME = "notification_history"

    def __init__(self, db: MongoDatabase):
        self.db = db
        self.collection: MongoCollection = db[self.COLLECTION_NAME]

    async def add(self, **kwargs):
        """ Сохранить уведомление в истории """

        res: InsertOneResult = await self.collection.insert_one(kwargs)
        if not res.inserted_id:
            logger.warning("Notice is not added to history. Doc: [%s]" % kwargs)


def get_history_service(mongo_conn=Depends(get_mongo_conn)) -> HistoryService:
    mongo_db = mongo_conn[MONGO_DB]
    return HistoryService(mongo_db)
