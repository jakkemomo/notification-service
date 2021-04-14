import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from notification_api.src.api.v1 import notice, service_notice, user_notice
from notification_api.src.db import mongo
from notification_api.src.settings import MONGO_URI

app = FastAPI()

app.include_router(notice.notice_api, prefix="/admin", tags=["admin"])
app.include_router(user_notice.user_notice_api, prefix="/user", tags=["user"])
app.include_router(service_notice.service_api, prefix="/service", tags=["service"])


@app.on_event("startup")
async def startup():
    mongo.mongo_conn = AsyncIOMotorClient(MONGO_URI)


@app.on_event("shutdown")
async def shutdown():
    mongo.mongo_conn.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
