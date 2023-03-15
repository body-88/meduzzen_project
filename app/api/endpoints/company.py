from fastapi import APIRouter, Depends
from app.schemas.company import CompanyBase, CompanyCreate, CompanyUpdate
from app.schemas.user import Result, UserResponse, UsersListResponse
from app.servises.company import CompanyService, get_company_service
from app.servises.invitation import InvitationService, get_invitation_service
from app.api.deps import get_current_user


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


@router.delete("/{company_id}/", status_code=200)
async def delete_company(company_id: int,
                    service: CompanyService = Depends(get_company_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    db_user = await service.delete_company(company_id=company_id, current_user_id=current_user.user_id)
    return Result(result=db_user, message="Company deleted successfully")


@router.get("/{company_id}/members", response_model=Result[UsersListResponse], status_code=200, response_description="Company members")
async def get_company_members(company_id: int,
                    service: InvitationService = Depends(get_invitation_service), 
                    current_user: UserResponse = Depends(get_current_user)) -> Result[UsersListResponse]:
    result = await service.get_members(company_id=company_id)
    return Result[UsersListResponse](result={"users": result})


@router.delete("/{company_id}", response_model=Result, status_code=200)
async def leave_company(company_id: int,
    service: InvitationService = Depends(get_invitation_service), 
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.leave_company(current_user_id=current_user.user_id, company_id=company_id)
    return Result(result=result, message="You have left the company")