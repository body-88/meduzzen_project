
from databases import Database
from app.models.invite_membership import Invitation
from app.schemas.invitation import InvitationCreate, InvitationBase
from sqlalchemy import delete, select, insert
from app.db.db_settings import get_db
from fastapi import Depends, HTTPException
from app.servises.company import CompanyService
from app.servises.user import UserService
from app.schemas.user import Result
from app.models.company import Company
from app.models.members import Members


class InvitationService:
    def __init__(self, db: Database):
        self.db = db
        
        
    async def create_invitation(self, invitation: InvitationCreate,
                                current_user_id: int,
                                company_service: CompanyService,
                                user_service: UserService) -> InvitationBase:
        db_user = await user_service.get_user(user_id=invitation.to_user_id)
        user_company = await company_service.get_company_by_user(current_user_id=current_user_id,
                                                                company_id=invitation.from_company_id)
        query = insert(Invitation).values(
                                        to_user_id = invitation.to_user_id,
                                        from_company_id = invitation.from_company_id,
                                        invite_message = invitation.invite_message,
                                        ).returning(Invitation)
        result = await self.db.fetch_one(query=query)
        return result


    async def get_invitation_by_id(self, invitation_id: int, current_user_id: int) -> Invitation:
        query = select(Invitation).where(Invitation.id == invitation_id)
        invitation = await self.db.fetch_one(query=query)
        if invitation is None:
            raise HTTPException(status_code=404, detail="Invite not found")
        return invitation


    async def get_invitations_by_user(self, current_user_id: int) -> Invitation:
        query = select(Invitation).where(Invitation.to_user_id == current_user_id)
        result = await self.db.fetch_all(query=query)
        return result


    async def get_invitations_by_company(self, company_id: int,
                                        current_user_id: int,
                                        company_service: CompanyService) -> Invitation:
        query = (
        select(Invitation, Company.company_owner_id)
        .join(Company, Invitation.from_company_id == Company.company_id)
        .where((Invitation.from_company_id == company_id) & (Company.company_owner_id == current_user_id)
        )
    )
        company = await company_service.get_company_by_user(company_id=company_id,
                                                    current_user_id=current_user_id)
        result = await self.db.fetch_all(query=query)
        if not result:
            raise HTTPException(status_code=404, detail="No invitations found for this company.")
        return result
    
    
    async def cancel_invitation(self, invitation_id: int, current_user_id: int) -> Result:
        query = (
        select(Invitation, Company.company_owner_id)
        .join(Company, Invitation.from_company_id == Company.company_id)
        .where(Invitation.id == invitation_id)
    )
        db_invitation = await self.db.fetch_one(query=query)
        if db_invitation is None:
            raise HTTPException(status_code=404, detail="Invite not found")
        if db_invitation.company_owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="it's not your company")
        query = delete(Invitation).where(Invitation.id == invitation_id)
        result = await self.db.execute(query=query)
        return result

    
    async def accept_invitation(self, current_user_id: int, invitation_id: int) -> Result:
        db_invitation = await self.get_invitation_by_id(invitation_id=invitation_id,
                                                        current_user_id=current_user_id)
        if not current_user_id == db_invitation.to_user_id:
            raise HTTPException(status_code=400, detail="It is not your invite")
        query = insert(Members).values(
                                        user_id = current_user_id,
                                        company_id = db_invitation.from_company_id
                                        
                                        ).returning(Members)
        result = await self.db.fetch_one(query=query)
        delete_query = delete(Invitation).where(Invitation.id == invitation_id)
        await self.db.execute(query=delete_query)
        return result
    
    
    async def decline_invitation(self, current_user_id: int, invitation_id: int) -> Result:
        db_invitation = await self.get_invitation_by_id(invitation_id=invitation_id,
                                                        current_user_id=current_user_id)
        if not current_user_id == db_invitation.to_user_id:
            raise HTTPException(status_code=400, detail="User does not have an invite to the company")
        query = delete(Invitation).where(Invitation.id == invitation_id)
        result = await self.db.execute(query=query)
        return result


async def get_invitation_service(db: Database = Depends(get_db)) -> InvitationService:
    return InvitationService(db)