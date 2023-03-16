from fastapi import APIRouter, Depends
from app.schemas.invitation import InvitationBase, InvitationCreate
from app.schemas.user import Result, UserResponse
from app.servises.company import CompanyService, get_company_service
from app.api.deps import get_current_user
from app.servises.invitation import InvitationService, get_invitation_service
from app.servises.user import UserService, get_user_service


router = APIRouter()


@router.post("/", response_model=Result[InvitationBase], status_code=200)
async def create_invitation(invitation: InvitationCreate, 
                    service: InvitationService = Depends(get_invitation_service),
                    current_user: UserResponse = Depends(get_current_user),
                    company_service: CompanyService = Depends(get_company_service),
                    user_service: UserService = Depends(get_user_service)) -> Result[InvitationBase]:
    result = await service.create_invitation(invitation=invitation,
                                            current_user_id=current_user.user_id,
                                            company_service=company_service,
                                            user_service=user_service)
    return Result(result=InvitationBase(**result), message="success")


@router.delete("/{invitation_id}/", status_code=200, response_model=Result)
async def cancel_invitation(invitation_id: int,
                    service: InvitationService = Depends(get_invitation_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.cancel_invitation(invitation_id=invitation_id,
                                            current_user_id=current_user.user_id)
    return Result(result=result, message="success")


@router.get("/my", response_model=Result, status_code=200)
async def my_invitations(service: InvitationService = Depends(get_invitation_service), 
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.get_invitations_by_user(current_user_id=current_user.user_id)
    return Result(result=result)


@router.get("/company/{company_id}/", response_model=Result, status_code=200)
async def company_invitations(company_id: int,
                            service: InvitationService = Depends(get_invitation_service),
                            current_user: UserResponse = Depends(get_current_user),
                            company_service: CompanyService = Depends(get_company_service)) -> Result:
    result = await service.get_invitations_by_company(current_user_id=current_user.user_id,
                                                    company_id=company_id,
                                                    company_service=company_service)
    return Result(result=result)


@router.get("/{invitation_id}/accept/", response_model=Result, status_code=200, response_description="Invitation accepted")
async def accept_invitation(invitation_id: int,
                    service: InvitationService = Depends(get_invitation_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.accept_invitation(invitation_id=invitation_id,
                                            current_user_id=current_user.user_id)
    return Result(result=result, message="success")


@router.get("/{invitation_id}/decline/", response_model=Result, status_code=200, response_description="Invitation declined")
async def decline_invitation(invitation_id: int,
                    service: InvitationService = Depends(get_invitation_service),
                    current_user: UserResponse = Depends(get_current_user)) -> Result:
    result = await service.decline_invitation(invitation_id=invitation_id,
                                            current_user_id=current_user.user_id)
    return Result(result=result, message="success")