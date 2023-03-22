from fastapi import APIRouter, Depends
from app.schemas.user import Result, UserResponse
from app.servises.company import CompanyService, get_company_service
from app.servises.quiz import QuizService, get_quiz_service
from app.api.deps import get_current_user
from app.schemas.question import QuestionBase, QuestionCreate, QuestionUpdate
from app.servises.question import QuestionService, get_question_service

router = APIRouter()


@router.post("/quiz/{quiz_id}/", response_model=Result[QuestionBase], status_code=200, response_description="Question created")
async def create_question(question: QuestionCreate,
                    quiz_id: int,
                    service: QuestionService = Depends(get_question_service),
                    current_user: UserResponse = Depends(get_current_user),
                    quiz_service: QuizService = Depends(get_quiz_service),
                    company_service: CompanyService = Depends(get_company_service)) -> Result[QuestionBase]:
    result = await service.create_question(question=question,
                                            current_user_id=current_user.user_id,
                                            quiz_service=quiz_service,
                                            company_service=company_service, quiz_id=quiz_id)
    return Result(result=QuestionBase(**result), message="success")


@router.get("/{question_id}/quiz/{quiz_id}/", response_model=Result[QuestionBase], status_code=200, response_description="Question retrieved")
async def get_question(question_id: int,
                    quiz_id: int,
                    quiz_service: QuizService = Depends(get_quiz_service),
                    service: QuestionService = Depends(get_question_service),
                    current_user: UserResponse = Depends(get_current_user),
                    company_service: CompanyService = Depends(get_company_service)) -> Result[QuestionBase]:
    result = await service.get_question_validated(current_user_id=current_user.user_id,
                                        question_id=question_id, company_service=company_service,
                                        quiz_service=quiz_service,
                                        quiz_id=quiz_id)
    return Result[QuestionBase](result=result, message="success")


@router.put("/{question_id}/quiz/{quiz_id}/", response_model=Result[QuestionBase], status_code=200, response_description="Question updated")
async def update_question(question: QuestionUpdate,
                    question_id: int,
                    quiz_id: int,
                    quiz_service: QuizService = Depends(get_quiz_service),
                    service: QuestionService = Depends(get_question_service),
                    current_user: UserResponse = Depends(get_current_user),
                    company_service: CompanyService = Depends(get_company_service)) -> Result[QuestionBase]:
    result = await service.update_question(current_user_id=current_user.user_id, question=question,
                                        question_id=question_id, company_service=company_service,
                                        quiz_service=quiz_service,
                                        quiz_id=quiz_id)
    return Result[QuestionBase](result=result, message="success")


@router.delete("/{question_id}/quiz/{quiz_id}/", status_code=200, response_model=Result, response_description="Question delete")
async def delete_question(question_id: int,
                        quiz_id: int,
                        quiz_service: QuizService = Depends(get_quiz_service),
                        service: QuestionService = Depends(get_question_service),
                        company_service: CompanyService = Depends(get_company_service),
                        current_user: UserResponse = Depends(get_current_user)) -> Result:
    result=await service.delete_question(current_user_id=current_user.user_id,
                                        company_service=company_service,
                                        question_id=question_id,
                                        quiz_service=quiz_service,
                                        quiz_id=quiz_id)
    return Result(result=result, message="success")