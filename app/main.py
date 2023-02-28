from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from db.db_settings import get_db

from logging.config import dictConfig
import logging
from utils.log_conf import LogConfig 

dictConfig(LogConfig().dict())
logger = logging.getLogger("app")

logger.info("Dummy Info")
logger.error("Dummy Error")
logger.debug("Dummy Debug")
logger.warning("Dummy Warning")

app = FastAPI()


@app.on_event("startup")
async def startup():
    db = await get_db()
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    db = await get_db()
    await db.disconnect()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://localhost",
    "https://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {
    "status_code": 200,
    "detail": "ok",
    "result": "working"
}


