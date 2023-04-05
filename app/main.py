from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.db.db_settings import get_db, get_redis
from logging.config import dictConfig
import logging
from app.utils.log_conf import LogConfig 
from app.api.api import api_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.servises.user import UserService
from app.servises.quiz import QuizService
from app.servises.company import CompanyService
from app.servises.notification import NotificationService


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
    scheduler.start()

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

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('cron', hour=0)
async def send_notification():
    db = await get_db()
    redis = await get_redis()
    quiz_service = QuizService(db)
    user_service = UserService(db)
    company_service = CompanyService(db, redis)
    notification_service = NotificationService(db)
    await notification_service.check_quiz_notification(quiz_service, user_service, company_service)


@app.get("/")
def health_check():
    return {
    "status_code": 200,
    "detail": "ok",
    "result": "working"
}


app.include_router(api_router)