from fastapi import APIRouter, Depends
from app.schemas.company import CompanyBase, CompanyCreate, CompanyUpdate
from app.schemas.user import Result, UserResponse
from app.servises.company import CompanyService, get_company_service
from app.servises.invitation import InvitationService, get_invitation_service
from app.api.deps import get_current_user
from app.schemas.member import MakeAdmin
from app.servises.quiz import QuizService, get_quiz_service
from app.schemas.quiz_result import QuizSubmit
from app.servises.question import QuestionService, get_question_service


router = APIRouter()
companies_router = APIRouter()

@router.post("/", response_model=Result[CompanyBase], status_code=201, response_description="Company created")
async def create_company(company: CompanyCreate,
                    service: CompanyService = Depends(get_company_service),
                    current_user: UserResponse = Depends(get_current_user),
                    invitation_service: InvitationService = Depends(get_invitation_service)) -> Result[CompanyBase]:
    db_company = await service.create_company(company=company, current_user_id=current_user.user_id)
    return Result(result=CompanyBase(**db_company))


@companies_router.get("/", response_model=Result, status_code=200, response_description="Companies returned")
async def read_companies(service: CompanyService = Depends(get_company_service), 
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    companies = await service.get_companies(current_user_id=current_user.user_id)
    return Result(result={"companies": companies})


@router.get("/{company_id}/", response_model=Result[CompanyBase], status_code=200, response_description="Company returned")
async def read_company(company_id: int,
                    service: CompanyService = Depends(get_company_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result[CompanyBase]:
    result = await service.get_company(company_id=company_id, current_user_id=current_user.user_id)
    return Result[CompanyBase](result=result)


@router.put("/{company_id}/", response_model=Result[CompanyBase], status_code=200, response_description="Company updated")
async def update_company(company: CompanyUpdate,
                    company_id: int,
                    service: CompanyService = Depends(get_company_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result[CompanyBase]:
    result = await service.update_company(current_user_id=current_user.user_id, company=company, company_id=company_id)
    return Result[CompanyBase](result=result, message="Company has been updated")


@router.delete("/{company_id}/", status_code=200, response_model=Result, response_description="Company delete")
async def delete_company(company_id: int,
                    service: CompanyService = Depends(get_company_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    db_user = await service.delete_company(company_id=company_id, current_user_id=current_user.user_id)
    return Result(result=db_user, message="Company deleted successfully")


@router.get("/{company_id}/members", response_model=Result, status_code=200, response_description="Company members")
async def get_company_members(company_id: int,
                    service: CompanyService = Depends(get_company_service), 
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.get_members(company_id=company_id)
    return Result(result={"users": result})


@router.delete("/{company_id}/leave", response_model=Result, status_code=200, response_description="Leave company")
async def leave_company(company_id: int,
                        service: CompanyService = Depends(get_company_service), 
                        current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.leave_company(current_user_id=current_user.user_id, company_id=company_id)
    return Result(result=result, message="You have left the company")


@router.delete("/{company_id}/member/{user_id}/", response_model=Result, status_code=200, response_description="Delete company member")
async def kick_company_member(company_id: int, user_id: int,
                    service: CompanyService = Depends(get_company_service), 
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.kick_member(company_id=company_id, user_id=user_id, current_user_id=current_user.user_id)
    return Result(result=result, message="User has been kicked")


@router.post("/{company_id}/admin/", response_model=Result, status_code=200, response_description="Make company admin")
async def make_admin(company_id: int, member: MakeAdmin,
                        service: CompanyService = Depends(get_company_service), 
                        current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.make_admin(current_user_id=current_user.user_id, member=member, company_id=company_id)
    return Result(result=result, message="success")


@router.get("/{company_id}/admins", response_model=Result, status_code=200, response_description="Company admins")
async def company_admins(company_id: int,
                    service: CompanyService = Depends(get_company_service), 
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.get_members_admins(company_id=company_id)
    return Result(result={"admin": result})


@router.delete("/{company_id}/admin/{admin_id}", response_model=Result, status_code=200, response_description="Remove company admin")
async def remove_admin(company_id: int, admin_id: int,
                        service: CompanyService = Depends(get_company_service), 
                        current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.remove_admin(current_user_id=current_user.user_id, admin_id=admin_id, company_id=company_id)
    return Result(result=result, message="success")


@router.get("/{company_id}/quizzes", response_model=Result, status_code=200)
async def company_invitations(company_id: int,
                            quiz_service: QuizService = Depends(get_quiz_service),
                            current_user: UserResponse = Depends(get_current_user),
                            company_service: CompanyService = Depends(get_company_service)
                            ) -> Result:
    quizzes = await quiz_service.get_quizzes(company_id=company_id, company_service=company_service)
    return Result(result={"quizzes": quizzes})


@router.post("/{company_id}/quiz/{quiz_id}/submit", response_model=Result, status_code=200, response_description="Pass quiz")
async def pass_quiz(company_id: int, quiz_id: int, quiz_submit: QuizSubmit,
                        service: CompanyService = Depends(get_company_service), 
                        current_user: UserResponse = Depends(get_current_user),
                        quiz_service: QuizService = Depends(get_quiz_service),
                        question_service: QuestionService = Depends(get_question_service)) -> Result:
    result = await service.pass_quiz(current_user_id=current_user.user_id,
                                    quiz_id=quiz_id,
                                    company_id=company_id,
                                    quiz_submit=quiz_submit,
                                    quiz_service=quiz_service,
                                    question_service=question_service,
                                )
    return Result(result=result, message="success")


@router.get("/{company_id}/rating", response_model=Result, status_code=200, response_description="Company rating returned")
async def read_company(company_id: int,
                    service: CompanyService = Depends(get_company_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.get_user_company_rating(company_id=company_id, user_id=current_user.user_id)
    return Result(result=result, message="success")