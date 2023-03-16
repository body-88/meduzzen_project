from databases import Database
from app.models.company import Company
from app.schemas.company import CompanyBase, CompanyCreate, CompanyUpdate
from sqlalchemy import update, delete, select, insert
from app.db.db_settings import get_db
from fastapi import Depends, HTTPException
from app.models.members import Members
from app.models.invite_membership import Invitation
from typing import List
from app.models.user import User
from app.schemas.user import Result


class CompanyService:
    def __init__(self, db: Database):
        self.db = db
        
        
    async def create_company(self, company: CompanyCreate, current_user_id: int) -> CompanyBase:
        query = insert(Company).values(
            company_name = company.company_name,
            company_description = company.company_description,
            company_owner_id = current_user_id,
            hide_status = False
        ).returning(Company)
        db_company = await self.db.fetch_one(query=query)
        if db_company:
            query_company = insert(Members).values(
                                        user_id = current_user_id,
                                        company_id = db_company.company_id
                                        )
            await self.db.execute(query=query_company)
        return db_company
    
    
    async def get_companies(self, current_user_id: int, skip: int = 0, limit: int = 100):
        query = (select(Company).where((Company.hide_status == False) | (Company.company_owner_id == current_user_id)
        )
        .offset(skip)
        .limit(limit)
    )
        companies = await self.db.fetch_all(query=query)
        return companies
    
    
    async def get_company(self, company_id: int, current_user_id: int) -> CompanyBase:
        query = select(Company).where(Company.company_id == company_id)
        company = await self.db.fetch_one(query=query)
        if company is None or company.hide_status and (current_user_id is None or current_user_id != company.company_owner_id):
            raise HTTPException(status_code=404, detail="Company doesn't exist or You have no rights")
        return company
    
    
    async def update_company(self, company_id: int, company: CompanyUpdate, current_user_id: int) -> CompanyBase:
        db_company = await self.get_company(company_id=company_id, current_user_id=current_user_id)
        if db_company is None or db_company.company_owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="Company doesn't exist or You have no rights")
        company_dict = company.dict(exclude_unset=True)
        query = (
            update(Company)
            .where(Company.company_id == company_id)
            .values(**company_dict)
            .returning(Company)
        )
        result = await self.db.fetch_one(query=query)
        return result
    
    
    async def delete_company(self, company_id: int, current_user_id: int) -> Result:
        db_company=await self.get_company(company_id=company_id, current_user_id=current_user_id)
        if db_company.company_owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="You have no rights")
        async with self.db.transaction():

            members_query = delete(Members).where(Members.company_id == company_id)
            await self.db.execute(query=members_query)

            invitations_query = delete(Invitation).where(Invitation.from_company_id == company_id)
            await self.db.execute(query=invitations_query)
            
            company_query = delete(Company).where(Company.company_id == company_id)
            result = await self.db.execute(query=company_query)
        return result
    
    
    async def get_company_by_user(self, company_id: int, current_user_id: int) -> CompanyBase:
        query = select(Company).where(Company.company_id == company_id)
        company = await self.db.fetch_one(query=query)
        if company is None or company.hide_status:
            raise HTTPException(status_code=404, detail="Company does not exist")
        if current_user_id is None or current_user_id != company.company_owner_id:
            raise HTTPException(status_code=403, detail="it's not your company")
        return company
        
        
    async def get_company_by_id(self, company_id: int) -> CompanyBase:
        query = select(Company).where(Company.company_id == company_id)
        company = await self.db.fetch_one(query=query)
        if company is None:
            raise HTTPException(status_code=404, detail="Company does not exist")
        return company
    
    
    async def get_members(self, company_id: int) -> List[User]:
        query = select(User).join(Members).where(Members.company_id == company_id)
        result = await self.db.fetch_all(query=query)
        return result
    
    
    async def leave_company(self, current_user_id: int, company_id: int) -> Result:
        query = select(Members).where((Members.user_id == current_user_id) & (Members.company_id == company_id))
        member = await self.db.fetch_one(query=query)
        if not member:
            raise HTTPException(status_code=404, detail="You are not a member of this company")
        query = delete(Members).where((Members.user_id == current_user_id) & (Members.company_id == company_id))
        result = await self.db.execute(query=query)
        return result
    
    
    async def kick_member(self, company_id: int, user_id: int, current_user_id: int) -> Result:
        db_company = await self.get_company(company_id=company_id, current_user_id=current_user_id)
    
        query = select(Members).where((Members.company_id == company_id) & (Members.user_id == user_id))
        db_member = await self.db.fetch_one(query=query)
        if not db_member:
            raise HTTPException(status_code=404, detail="User is not a member of the company")
        
        query = delete(Members).where((Members.company_id == company_id) & (Members.user_id == user_id))
        result = await self.db.execute(query=query)
        return result

async def get_company_service(db: Database = Depends(get_db)) -> CompanyService:
    return CompanyService(db)