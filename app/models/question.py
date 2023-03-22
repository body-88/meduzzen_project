from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from typing import List
from sqlalchemy.orm import relationship


class Question(Base):
    __tablename__ = 'questions'

    id: int = Column(Integer, primary_key=True, index=True)
    quiz_id: int = Column(Integer, ForeignKey('quizzes.id'))
    question: str = Column(String)
    answer_variants: List[str] = Column(ARRAY(String))
    correct_answer: int = Column(Integer, index=True)
    
    quiz = relationship("Quiz", back_populates="questions")