import aio_pika
import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from communication_api.api.v1.notification import router
from communication_api.db import mongo, rabbitmq
from communication_api.settings import MONGO_URI, RABBIT_URL

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup():
    rabbitmq.rabbit_conn = await aio_pika.connect_robust(RABBIT_URL)
    mongo.mongo_conn = AsyncIOMotorClient(MONGO_URI)


@app.on_event("shutdown")
async def shutdown():
    await rabbitmq.rabbit_conn.close()
    await mongo.mongo_conn.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888)
