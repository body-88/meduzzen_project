from databases import Database
from app.models.quiz import Quiz
from app.schemas.quiz import QuizBase, QuizCreate, QuizUpdate, QuizBaseResponse
from sqlalchemy import update, delete, select, insert
from app.db.db_settings import get_db
from fastapi import Depends, HTTPException
from app.servises.company import CompanyService
from app.models.question import Question
from fastapi.encoders import jsonable_encoder
from app.schemas.user import Result
from typing import List

class QuizService:
    def __init__(self, db: Database):
        self.db = db
        
        
    async def create_quiz(self, quiz: QuizCreate, current_user_id: int, company_service: CompanyService) -> QuizBase:
        member = await company_service.get_member_role(company_id=quiz.company_id, user_id=current_user_id)
        query = insert(Quiz).values(
            company_id = quiz.company_id,
            name = quiz.name,
            description = quiz.description,
            frequency = quiz.frequency
        ).returning(Quiz)
        db_quiz = await self.db.fetch_one(query=query)
        
        questions = []
        for question in quiz.questions:
            if len(question.answer_variants) < 2:
                await self.db.execute(delete(Question).where(Question.quiz_id == db_quiz.id))
                await self.db.execute(delete(Quiz).where(Quiz.id == db_quiz.id))
                
                raise HTTPException(status_code=400, detail="At least two answer variants are required for a question.")
            question_query = insert(Question).values(
                quiz_id=db_quiz.id,
                question=question.question,
                answer_variants=question.answer_variants,
                correct_answer=question.correct_answer
            ).returning(Question)
            db_question = await self.db.fetch_one(query=question_query)
            questions.append(db_question)
        if len(questions) < 2:
            await self.db.execute(delete(Question).where(Question.quiz_id == db_quiz.id))
            await self.db.execute(delete(Quiz).where(Quiz.id == db_quiz.id))
            
            raise HTTPException(status_code=400, detail="At least two questions are required for a quiz.")
        db_quiz.questions = questions
        return db_quiz
    
    
    async def get_quizzes(self, company_id: int, company_service: CompanyService, skip: int = 0, limit: int = 100) -> List[QuizBase]:
        db_company= await company_service.get_company_by_id(company_id=company_id)
        query = select(Quiz).where(Quiz.company_id == company_id).offset(skip).limit(limit)
        result = await self.db.fetch_all(query=query)
        return result
    
    
    async def update_quiz(self, quiz_id: int,
                        company_id: int, 
                        quiz: QuizUpdate, 
                        current_user_id: int, 
                        company_service: CompanyService) -> QuizBase:
        db_member = await company_service.get_member_role(company_id=company_id, user_id=current_user_id)
        db_quiz = await self.get_quiz_by_id(quiz_id=quiz_id)
        quiz_dict = quiz.dict(exclude_unset=True)
        query = (
            update(Quiz)
            .where(Quiz.id == quiz_id)
            .values(**quiz_dict)
            .returning(Quiz)
        )
        result = await self.db.fetch_one(query=query)
        return result
    
    
    async def delete_quiz(self, quiz_id: int, company_id: int, current_user_id: int, company_service: CompanyService) -> Result:
        db_quiz = await self.get_quiz_by_id(quiz_id=quiz_id)
        db_member = await company_service.get_member_role(company_id=company_id, user_id=current_user_id)
        
        async with self.db.transaction():

            question_query = delete(Question).where(Question.quiz_id == quiz_id)
            await self.db.execute(query=question_query)

            query = delete(Quiz).where(Quiz.id == quiz_id)
            result = await self.db.execute(query=query)
        return result
    
    
    async def get_quiz_by_id(self, quiz_id: int) -> QuizBase:
        query = select(Quiz).where(Quiz.id == quiz_id)
        quiz = await self.db.fetch_one(query=query)
        if quiz is None:
            raise HTTPException(status_code=404, detail="Quiz does not exist")
        return quiz
    

    async def get_quiz_with_companies(self, quiz_id: int,
                                    company_id: int,
                                    current_user_id,
                                    company_service: CompanyService ) -> QuizBaseResponse:
        db_member = await company_service.get_member_role(company_id=company_id, user_id=current_user_id)
        query = select(Quiz).where(Quiz.id == quiz_id)
        quiz = await self.db.fetch_one(query=query)
        if quiz is None:
            raise HTTPException(status_code=404, detail="Quiz does not exist")
        query = select(Question).where(Question.quiz_id == quiz_id)
        questions = await self.db.fetch_all(query=query)
        quiz_base = jsonable_encoder(quiz)
        quiz_base['questions'] = [jsonable_encoder(question) for question in questions]
        return QuizBaseResponse(**quiz_base)
    



async def get_quiz_service(db: Database = Depends(get_db)) -> QuizService:
    return QuizService(db)