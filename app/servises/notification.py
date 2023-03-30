from databases import Database
from app.models.notifications import Notification
from sqlalchemy import update, select, insert
from app.db.db_settings import get_db
from fastapi import Depends, HTTPException
from app.servises.user import UserService, get_user_service
from app.servises.quiz import QuizService, get_quiz_service
from app.servises.company import CompanyService, get_company_service
from datetime import datetime, timedelta
import pytz


class NotificationService:
    def __init__(self, db: Database):
        self.db = db


    async def get_all_notifications_unread(self, current_user_id: int):
        query = select(Notification).where((Notification.user_id==current_user_id) & (Notification.status==False))
        result = await self.db.fetch_all(query=query)
        return result
    
    
    async def get_all_notifications_read(self, current_user_id: int):
        query = select(Notification).where((Notification.user_id==current_user_id) & (Notification.status==True))
        result = await self.db.fetch_all(query=query)
        return result
    
    
    async def get_my_notification(self, current_user_id: int, notification_id: int):
        query = select(Notification).where(
            (Notification.user_id==current_user_id) & 
            (Notification.id==notification_id))
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=404, detail="Notification doesn't exist")
        return result
    
    
    async def manage_notification(self, notification_id: int, current_user_id: int):
        db_notification = await self.get_my_notification(notification_id=notification_id, current_user_id=current_user_id)
        if db_notification.status == False:
            query = (
                update(Notification)
                .where(Notification.id == notification_id)
                .values(
                        status = True
                        )
                .returning(Notification)
            )
        else:
            query = (
                update(Notification)
                .where(Notification.id == notification_id)
                .values(
                        status = False
                        )
                .returning(Notification)
            )
        result = await self.db.fetch_one(query=query)    
        return result
    
    
    async def check_quiz_notification(self, quiz_service: QuizService = Depends(get_quiz_service), user_service: UserService = Depends(get_user_service), company_service: CompanyService = Depends(get_company_service)):
        db_users = await user_service.get_users()
        now = datetime.now(pytz.utc)
        for user in db_users:
            last_passed_quizzes = await  company_service.get_user_passed_quizzes(user.id)
            for quiz in last_passed_quizzes:
                quiz_id = quiz.quiz_id
                last_date = quiz.date
                db_quiz = await quiz_service.get_quiz_by_id(quiz_id=quiz_id)
                if db_quiz and db_quiz.frequency is not None:
                    frequency = db_quiz.frequency
                    difference = now - last_date
                    if difference > timedelta(days=int(frequency)):
                        query = insert(Notification).values(
                        text = f"Dear user:{user.id} now you can pass again quiz:{db_quiz.id} in company{db_quiz.company_id}",
                        quiz_id = db_quiz.id,
                        company_id = db_quiz.company_id,
                        user_id = user.id,
                        status = False
                        )
                        await self.db.fetch_one(query=query)



async def get_notification_service(db: Database = Depends(get_db)) -> NotificationService:
    return NotificationService(db)