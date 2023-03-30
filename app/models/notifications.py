from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Notification(Base):
    __tablename__ = "notifications"
    
    id: int = Column(Integer, primary_key=True, index=True)
    status: bool = Column(Boolean, default=False, server_default="false", nullable=False)
    text: str = Column(String)
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())
    user_id: int = Column(Integer, ForeignKey("users.id"))
    quiz_id: int = Column(Integer, ForeignKey("quizzes.id"))
    company_id: int = Column(Integer, ForeignKey("companies.company_id"))
    
    user = relationship("User", back_populates="notification")
    company = relationship("Company", back_populates="notification")
    quiz = relationship("Quiz", back_populates="notification")