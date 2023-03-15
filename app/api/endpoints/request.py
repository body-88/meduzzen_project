from fastapi import APIRouter, Depends
from app.schemas.request import RequestBase, RequestCreate
from app.schemas.user import Result, UserResponse
from app.servises.company import CompanyService, get_company_service
from app.api.deps import get_current_user
from app.servises.request import RequestService, get_request_service

router = APIRouter()


@router.post("/", response_model=Result[RequestBase], status_code=200)
async def create_request(request: RequestCreate, 
                    service: RequestService = Depends(get_request_service),
                    current_user: UserResponse = Depends(get_current_user),
                    company_service: CompanyService = Depends(get_company_service)
                    ) -> Result[RequestBase]:
    result = await service.create_request(request=request,
                                            current_user_id=current_user.user_id, company_service=company_service)
    return Result(result=RequestBase(**result), message="success")


@router.get("/my", response_model=Result, status_code=200)
async def my_request(service: RequestService = Depends(get_request_service), 
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.get_requests_by_user(current_user_id=current_user.user_id)
    return Result(result=result)


@router.get("/company/{company_id}/", response_model=Result, status_code=200)
async def company_request(company_id: int,
                            service: RequestService = Depends(get_request_service),
                            current_user: UserResponse = Depends(get_current_user),
                            company_service: CompanyService = Depends(get_company_service)) -> Result:
    result = await service.get_requests_by_company(current_user_id=current_user.user_id,
                                                    company_id=company_id,
                                                    company_service=company_service)
    return Result(result=result, message="success")


@router.delete("/{request_id}/", status_code=200, response_model=Result)
async def cancel_request(request_id: int,
                    service: RequestService = Depends(get_request_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.cancel_request(request_id=request_id,
                                            current_user_id=current_user.user_id)
    return Result(result=result, message="success")


@router.get("/{request_id}/accept/", response_model=Result, status_code=200, response_description="request accepted")
async def accept_request(request_id: int,
                    service: RequestService = Depends(get_request_service),
                    current_user: UserResponse = Depends(get_current_user),
                    company_service: CompanyService = Depends(get_company_service)) -> Result:
    result = await service.accept_request(request_id=request_id,
                                            current_user_id=current_user.user_id, company_service=company_service)
    return Result(result=result, message="success")


@router.get("/{request_id}/decline/", response_model=Result, status_code=200, response_description="request declined")
async def decline_request(request_id: int,
                    service: RequestService = Depends(get_request_service),
                    current_user: UserResponse = Depends(get_current_user),
                    company_service: CompanyService = Depends(get_company_service)) -> Result:
    result = await service.decline_request(request_id=request_id,
                                            current_user_id=current_user.user_id, company_service=company_service)
    return Result(result=result, message="success")