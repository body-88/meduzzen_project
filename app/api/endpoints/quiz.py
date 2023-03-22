from fastapi import APIRouter, Depends
from app.schemas.user import Result, UserResponse
from app.servises.company import CompanyService, get_company_service
from app.servises.quiz import QuizService, get_quiz_service
from app.api.deps import get_current_user
from app.schemas.quiz import QuizCreate, QuizBase, QuizUpdate, QuizBaseResponse



router = APIRouter()

@router.post("/", response_model=Result[QuizBase], status_code=201, response_description="Quiz created")
async def create_quiz(quiz: QuizCreate,
                    service: QuizService = Depends(get_quiz_service),
                    current_user: UserResponse = Depends(get_current_user),
                    company_service: CompanyService = Depends(get_company_service),
                    ) -> Result[QuizBase]:
    db_quiz = await service.create_quiz(quiz=quiz,
                                        current_user_id=current_user.user_id,
                                        company_service=company_service)
    return Result(result=QuizBase(**db_quiz), message="success")


@router.put("/{quiz_id}/company/{company_id}/", response_model=Result[QuizBase], status_code=200, response_description="Quiz updated")
async def update_quiz(quiz: QuizUpdate,
                    company_id: int,
                    quiz_id: int,
                    service: QuizService = Depends(get_quiz_service),
                    current_user: UserResponse = Depends(get_current_user),
                    company_service: CompanyService = Depends(get_company_service)) -> Result[QuizBase]:
    result = await service.update_quiz(current_user_id=current_user.user_id,
                                    quiz=quiz,
                                    company_id=company_id,
                                    quiz_id=quiz_id,
                                    company_service=company_service)
    return Result[QuizBase](result=result, message="Quiz has been updated")


@router.delete("/{quiz_id}/company/{company_id}/", status_code=200, response_model=Result, response_description="Quiz delete")
async def delete_quiz(company_id: int,
                    quiz_id:int,
                    service: QuizService = Depends(get_quiz_service),
                    company_service: CompanyService = Depends(get_company_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    result= await service.delete_quiz(company_id=company_id,
                                    current_user_id=current_user.user_id,
                                    company_service=company_service,
                                    quiz_id=quiz_id)
    return Result(result=result, message="success")


@router.get("/{quiz_id}/company/{company_id}/", response_model=Result[QuizBaseResponse], status_code=200, response_description="Quiz returned")
async def get_quiz(quiz_id: int,
                    company_id: int,
                    service: QuizService = Depends(get_quiz_service),
                    company_service: CompanyService = Depends(get_company_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result[QuizBaseResponse]:
    result = await service.get_quiz_with_companies(quiz_id=quiz_id,
                                        current_user_id=current_user.user_id,
                                        company_service=company_service,
                                        company_id=company_id)
    return Result[QuizBaseResponse](result=result)