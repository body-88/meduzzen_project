from fastapi import APIRouter, Depends
from app.schemas.user import Result, UserResponse
from app.servises.company import CompanyService, get_company_service
from app.servises.quiz import QuizService, get_quiz_service
from app.api.deps import get_current_user
from app.schemas.question import QuestionBase, QuestionCreate
from app.servises.question import QuestionService, get_question_service

router = APIRouter()


@router.post("/{quiz_id}/company/{company_id}", response_model=Result[QuestionBase], status_code=200)
async def create_question(question: QuestionCreate,
                    company_id: int,
                    quiz_id: int,
                    service: QuestionService = Depends(get_question_service),
                    current_user: UserResponse = Depends(get_current_user),
                    quiz_service: QuizService = Depends(get_quiz_service),
                    company_service: CompanyService = Depends(get_company_service)) -> Result[QuestionBase]:
    result = await service.create_question(question=question,
                                            current_user_id=current_user.user_id,
                                            quiz_service=quiz_service,
                                            company_service=company_service, company_id=company_id, quiz_id=quiz_id)
    return Result(result=QuestionBase(**result), message="success")
