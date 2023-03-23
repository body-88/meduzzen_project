from app.db.base_class import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, validates
from app.models.question import Question


class QuizResult(Base):
    __tablename__ = 'quiz_result'
    
    id: int = Column(Integer, primary_key=True, index=True)
    quiz_id: int = Column(Integer, ForeignKey('quizzes.id'))
    company_id: int = Column(Integer, ForeignKey('companies.company_id'))
    user_id: int = Column(Integer, ForeignKey('users.id'))
    average_result: float = Column(Float)
    questions_number: int = Column(Integer)
    answers_number: int = Column(Integer)
    date: datetime = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship('User', back_populates='quiz_results')
    company = relationship('Company', back_populates='quiz_results')
    quiz = relationship('Quiz', back_populates='quiz_results')