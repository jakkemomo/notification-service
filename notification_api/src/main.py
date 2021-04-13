import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


@app.get("/")
async def index():
    return {"message": "Notification API"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
