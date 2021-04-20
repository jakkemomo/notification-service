import logging

import uvicorn
from fastapi import FastAPI

from websocket_service.src import views

app = FastAPI()

app.include_router(views.ws_router, tags=["websocket"])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run("main:app", host="0.0.0.0", port=9000)
