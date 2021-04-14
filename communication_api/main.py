import aio_pika
import uvicorn
from fastapi import FastAPI
from notification_api.db import rabbitmq
from notification_api.settings import RABBIT_URL

app = FastAPI()


@app.on_event("startup")
async def startup():
    rabbitmq.rabbit_conn = await aio_pika.connect_robust(RABBIT_URL)


@app.on_event("shutdown")
async def shutdown():
    await rabbitmq.rabbit_conn.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
