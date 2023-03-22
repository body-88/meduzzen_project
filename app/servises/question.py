from databases import Database
from app.models.question import Question
from app.schemas.question import QuestionBase, QuestionCreate, QuestionUpdate
from sqlalchemy import update, delete, select, insert
from app.db.db_settings import get_db
from fastapi import Depends, HTTPException
from app.servises.company import CompanyService
from app.servises.quiz import QuizService
from app.schemas.user import Result
from typing import List



class QuestionService:
    def __init__(self, db: Database):
        self.db = db
        
        
    async def create_question(self, quiz_id: int, question: QuestionCreate,
                            company_service: CompanyService, current_user_id: int,
                            quiz_service: QuizService) -> QuestionBase:
        db_quiz = await quiz_service.get_quiz_by_id(quiz_id = quiz_id)
        member = await company_service.get_member_role(company_id=db_quiz.company_id, user_id=current_user_id)
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
    
    
    
    async def get_question_validated(self, question_id: int, quiz_id: int,
                            current_user_id: int, company_service: CompanyService, quiz_service: QuizService) -> QuestionBase:
        db_question= await self.get_question_by_id(question_id=question_id)
        db_quiz = await quiz_service.get_quiz_by_id(quiz_id=quiz_id)
        db_member = await company_service.get_member_role(company_id=db_quiz.company_id, user_id=current_user_id)
        query = select(Question).where(Question.id == question_id)
        
        return db_question
    
    
    async def update_question(self, question_id: int, question: QuestionUpdate, quiz_id: int,
                            current_user_id: int, company_service: CompanyService, quiz_service: QuizService) -> QuestionBase:
        db_question = await self.get_question_by_id(question_id=question_id)
        db_quiz = await quiz_service.get_quiz_by_id(quiz_id=quiz_id)
        db_member = await company_service.get_member_role(company_id=db_quiz.company_id, user_id=current_user_id)
        if len(question.answer_variants) < 2:
            raise HTTPException(status_code=400, detail="At least two answer variants are required for a question.")
        question_dict = question.dict(exclude_unset=True)
        query = (
            update(Question)
            .where(Question.id == question_id)
            .values(**question_dict)
            .returning(Question)
        )
        result = await self.db.fetch_one(query=query)
        return result


    async def delete_question(self, question_id: int, current_user_id: int, quiz_id: int,
                            company_service: CompanyService, quiz_service: QuizService) -> Result:
        db_question = await self.get_question_by_id(question_id=question_id)
        db_quiz = await quiz_service.get_quiz_by_id(quiz_id=quiz_id)
        db_member = await company_service.get_member_role(company_id=db_quiz.company_id, user_id=current_user_id)
        question_query = delete(Question).where(Question.id == question_id)
        result = await self.db.execute(query=question_query)
        return result

    
    async def get_question_by_id(self, question_id: int) -> QuestionBase:
        query = select(Question).where(Question.id == question_id)
        db_question = await self.db.fetch_one(query=query)
        if db_question is None:
            raise HTTPException(status_code=404, detail="Question does not exist")
        return db_question

    
    async def get_questions_by_quiz(self, quiz_id: int, skip: int = 0, limit: int = 100) -> List[QuestionBase]:
        query = select(Question).where(Question.quiz_id == quiz_id).offset(skip).limit(limit)
        result = await self.db.fetch_all(query=query)
        return result
    




async def get_question_service(db: Database = Depends(get_db)) -> QuestionService:
    return QuestionService(db)