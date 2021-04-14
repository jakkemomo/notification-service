import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from notification_api.src.api.v1 import notice
from notification_api.src.db import mongo
from notification_api.src.settings import MONGO_URI

app = FastAPI()
app.include_router(notice.notice_api)


@app.on_event("startup")
async def startup():
    mongo.mongo_conn = AsyncIOMotorClient(MONGO_URI)


@app.on_event("shutdown")
async def shutdown():
    mongo.mongo_conn.close()


@app.get("/")
async def index():
    return {"message": "Notification API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
