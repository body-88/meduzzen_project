from fastapi import APIRouter, Depends, Query
from app.schemas.company import CompanyBase, CompanyCreate, CompanyUpdate
from app.schemas.user import Result, UserResponse
from app.servises.company import CompanyService, get_company_service
from app.api.deps import get_current_user
from app.api.exceptions import raise_not_authenticated

router = APIRouter()
companies_router = APIRouter()

@router.post("", response_model=Result[CompanyBase], status_code=201, response_description="Company created")
async def create_company(company: CompanyCreate,
                    service: CompanyService = Depends(get_company_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result[CompanyBase]:
    if not current_user:
        raise_not_authenticated()
    db_company = await service.create_company(company=company, user_id = current_user.user_id)
    return Result(result=CompanyBase(**db_company))


@companies_router.get("", response_model=Result, status_code=200, response_description="Companies returned")
async def read_companies(service: CompanyService = Depends(get_company_service), 
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    if not current_user:
        raise_not_authenticated()
    companies = await service.get_companies(current_user_id=current_user.user_id)
    return Result(result={"companies": companies})


@router.get("/{company_id}", response_model=Result[CompanyBase], status_code=200, response_description="Company returned")
async def read_company(company_id: int = Query(..., description="The ID of the company to retrieve"),
                    service: CompanyService = Depends(get_company_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result[CompanyBase]:
    if not current_user:
        raise_not_authenticated()
    result = await service.get_company(company_id=company_id, current_user_id=current_user.user_id)
    return Result[CompanyBase](result=result)


@router.put("/{company_id}", response_model=Result[CompanyBase], status_code=200, response_description="Company updated")
async def update_company(company: CompanyUpdate,
                    company_id: int = Query(..., description="The ID of the user to update"),
                    service: CompanyService = Depends(get_company_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result[CompanyBase]:
    if not current_user:
        raise_not_authenticated()
        
    result = await service.update_company(current_user_id=current_user.user_id, company=company, company_id=company_id)
    return Result[CompanyBase](result=result, message="company has been updated")


@router.delete("/{company_id}", status_code=200)
async def delete_company(company_id: int = Query(..., description="The ID of the company to delete"),
                    service: CompanyService = Depends(get_company_service),
                    current_user: UserResponse = Depends(get_current_user))-> Result:
    if not current_user:
        raise_not_authenticated()
    db_user = await service.delete_company(company_id=company_id, current_user_id = current_user.user_id)
    return Result(result=db_user, message="Company deleted successfully")