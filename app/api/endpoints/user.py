from fastapi import APIRouter, Depends, Response
from app.schemas.user import SignUpRequest, UserResponse, UsersListResponse, UserUpdateRequest, Result, UserUpdateResponse
from app.servises.user import UserService, get_user_service
from app.api.deps import get_current_user
from app.api.exceptions import wrong_account
from app.servises.company import CompanyService, get_company_service
from app.servises.quiz import QuizService, get_quiz_service
from io import StringIO
from typing import Optional
from app.schemas.quiz_result import QuizAnaliticsResponse


router = APIRouter()
users_router = APIRouter()


@users_router.get("/", response_model=Result[UsersListResponse], status_code=200, response_description="Users returned")
async def read_users(service: UserService = Depends(get_user_service), 
                    current_user: UserResponse = Depends(get_current_user)) -> Result[UsersListResponse]:
    users = await service.get_users()
    return Result[UsersListResponse](result={"users":users})


@router.post("/", response_model=Result[UserResponse], status_code=200, response_description="User created")
async def create_user(user: SignUpRequest,
                    service: UserService = Depends(get_user_service)) -> Result[UserResponse]:
    db_user = await service.create_user(user=user)
    return Result(result=UserResponse(**db_user))
    

@router.get("/{user_id}/", response_model=Result[UserResponse], status_code=200, response_description="User returned")
async def read_user(user_id: int,
                    service: UserService = Depends(get_user_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result[UserResponse]:
    db_user = await service.get_user(user_id=user_id)
    return Result[UserResponse](result=db_user)


@router.put("/{user_id}/", response_model=Result[UserUpdateResponse], status_code=200, response_description="User updated")
async def update_user(user: UserUpdateRequest,
                    user_id: int,
                    service: UserService = Depends(get_user_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result[UserUpdateResponse]:
    if current_user.user_id != user_id:
        wrong_account()
    db_user = await service.update_user(user_id=user_id, user=user)
    return Result[UserUpdateResponse](result=db_user, message="User has been updated")


@router.delete("/{user_id}/", status_code=200)
async def delete_user(user_id: int,
                    service: UserService = Depends(get_user_service),
                    current_user: UserResponse = Depends(get_current_user))-> Result:
    if current_user.user_id != user_id:
        wrong_account()
    db_user = await service.delete_user(user_id=user_id)
    return Result(result=db_user, message="User deleted successfully")


@router.get("/system_rating", response_model=Result, status_code=200, response_description="System rating")
async def read_system_rating(current_user: UserResponse = Depends(get_current_user),
                    company_service: CompanyService = Depends(get_company_service)) -> Result:
    system_rating = await company_service.get_user_overall_rating(user_id=current_user.user_id)
    return Result(result=system_rating, message="success")


@router.get("/compnay/{company_id}/quiz/{quiz_id}/my_results/", response_model=Result, status_code=200, response_description="My results")
async def get_result(company_id: int,
                    quiz_id: int,
                    format: Optional[str] = "json",
                    current_user: UserResponse = Depends(get_current_user),
                    company_service: CompanyService = Depends(get_company_service),
                    quiz_service: QuizService = Depends(get_quiz_service)) -> Result:
    if format == "csv":
        csv_file = StringIO()
        my_results = await company_service.get_my_result_to_csv(user_id=current_user.user_id,
                                                                    quiz_id=quiz_id,
                                                                    company_id=company_id,
                                                                    quiz_service=quiz_service,
                                                                    csv_file=csv_file)
        response = csv_file.getvalue()
        headers = {
                "Content-Disposition": "attachment; filename=quiz_results.csv",
                "Content-Type": "text/csv",
            }
        return Response(content=response, headers=headers)
    my_results = await company_service.get_my_result(user_id=current_user.user_id,
                                                    company_id=company_id,
                                                    quiz_id=quiz_id,
                                                    quiz_service=quiz_service)
    return Result(result=my_results, message="success")


@router.get("/me/average_results", response_model=Result, status_code=200, response_description="Average results")
async def get_average_results(current_user: UserResponse = Depends(get_current_user),
                    company_service: CompanyService = Depends(get_company_service)) -> Result:
    result = await company_service.get_user_average_results(user_id=current_user.user_id)
    return Result(result=result, message="success")


@router.get("/me/quizzes", response_model=Result, status_code=200, response_description="Get user passed quizzes")
async def get_user_passed_quizzes(current_user: UserResponse = Depends(get_current_user),
                    company_service: CompanyService = Depends(get_company_service)) -> Result:
    result = await company_service.get_user_passed_quizzes(user_id=current_user.user_id)
    return Result(result=result, message="success")