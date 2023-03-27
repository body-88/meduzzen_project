from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, validates
from app.models.question import Question

class Quiz(Base):
    __tablename__ = 'quizzes'
    
    id: int = Column(Integer, primary_key=True, index=True)
    company_id: int = Column(Integer, ForeignKey('companies.company_id'))
    name: str = Column(String, index=True)
    description: str = Column(String)
    frequency: str = Column(String)
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: datetime = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    questions = relationship("Question", back_populates="quiz")
    company = relationship("Company", back_populates="quizzes")
    quiz_results = relationship("QuizResult", back_populates="quiz")
