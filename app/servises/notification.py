from databases import Database
from app.models.notifications import Notification
from sqlalchemy import update, select
from app.db.db_settings import get_db
from fastapi import Depends, HTTPException
from typing import List


class NotificationService:
    def __init__(self, db: Database):
        self.db = db


    async def get_all_notifications(self, current_user_id: int, status: bool) -> List[Notification]:
        if status == False:
            query = select(Notification).where((Notification.user_id==current_user_id) & (Notification.status==status))
            result = await self.db.fetch_all(query=query)
        query = select(Notification).where((Notification.user_id==current_user_id) & (Notification.status==status))
        result = await self.db.fetch_all(query=query)
        return result
    
    
    async def get_my_notification(self, current_user_id: int, notification_id: int) -> Notification:
        query = select(Notification).where(
            (Notification.user_id==current_user_id) & 
            (Notification.id==notification_id))
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=404, detail="Notification doesn't exist")
        return result
    
    
    async def manage_notification(self, notification_id: int, current_user_id: int) -> Notification:
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


async def get_notification_service(db: Database = Depends(get_db)) -> NotificationService:
    return NotificationService(db)