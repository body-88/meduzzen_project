from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.db.db_settings import get_db
from celery import Celery
from logging.config import dictConfig
import logging
from app.utils.log_conf import LogConfig 
from app.api.api import api_router
from app.core.config import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.servises.user import UserService, get_user_service
from app.servises.quiz import QuizService, get_quiz_service
from app.servises.company import CompanyService, get_company_service
from app.servises.notification import NotificationService, get_notification_service
import asyncio



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

celery = Celery('tasks', broker="redis://redis:6379")
scheduler = AsyncIOScheduler()


@celery.task
def check_quiz_notification_task():
    return asyncio.run(run_check_quiz_notification())

async def run_check_quiz_notification():
    notification_service = await get_notification_service()
    quiz_service = await get_quiz_service()
    user_service = await get_user_service()
    company_service = await get_company_service()

    await notification_service.check_quiz_notification(quiz_service, user_service, company_service)


def start_scheduler():
    scheduler.add_job(check_quiz_notification_task(), 'interval', minutes=5)
    scheduler.start()

@app.get("/")
def health_check():
    return {
    "status_code": 200,
    "detail": "ok",
    "result": "working"
}


app.include_router(api_router)