from databases import Database
from app.models.question import Question
from app.schemas.question import QuestionBase, QuestionCreate, QuestionUpdate
from sqlalchemy import update, select, insert
from app.db.db_settings import get_db
from fastapi import Depends, HTTPException

from app.servises.company import CompanyService
from app.servises.quiz import QuizService


class QuestionService:
    def __init__(self, db: Database):
        self.db = db
        
        
    async def create_question(self, quiz_id: int, question: QuestionCreate,
                            company_service: CompanyService, current_user_id: int,
                            company_id: int, quiz_service: QuizService) -> QuestionBase:
        db_quiz = await quiz_service.get_quiz_by_id(quiz_id = quiz_id)
        member = await company_service.get_member_role(company_id=company_id, user_id=current_user_id)
        if len(question.answer_variants) < 2:
            raise HTTPException(status_code=400, detail="At least two answer variants are required for a question.")
        query = insert(Question).values(
            quiz_id = quiz_id,
            question = question.question,
            answer_variants = question.answer_variants,
            correct_answer = question.correct_answer,
        ).returning(Question)
        db_question = await self.db.fetch_one(query=query)
        
        return db_question
    
    
    async def get_question_by_id(self, question_id: int, skip: int = 0, limit: int = 100):
        query = select(Question).where(Question.id == question_id).offset(skip).limit(limit)
        result = await self.db.fetch_one(query=query)
        return result

    
    async def get_questions_by_quiz(self, quiz_id: int, current_user_id: int, skip: int = 0, limit: int = 100):
        query = select(Question).where(Question.quiz_id == quiz_id).offset(skip).limit(limit)
        result = await self.db.fetch_all(query=query)
        return result
    




async def get_question_service(db: Database = Depends(get_db)) -> QuestionService:
    return QuestionService(db)