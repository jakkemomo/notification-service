import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from communication_api.src.api.v1.notification import router
from communication_api.src.db import mongo
from communication_api.src.settings import settings

MONGO_URI = settings.mongo.get_uri()


app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup():
    mongo.mongo_conn = AsyncIOMotorClient(MONGO_URI)


@app.on_event("shutdown")
async def shutdown():
    await mongo.mongo_conn.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888)
