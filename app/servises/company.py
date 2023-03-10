from databases import Database
from app.models.company import Company
from app.schemas.company import CompanyBase, CompanyCreate, CompanyUpdate
from sqlalchemy import update, delete, select, insert
from app.db.db_settings import get_db
from fastapi import Depends, HTTPException


class CompanyService:
    def __init__(self, db: Database):
        self.db = db
        
        
    async def create_company(self, company: CompanyCreate, user_id: int) -> CompanyBase:
        query = insert(Company).values(
            company_name = company.company_name,
            company_description = company.company_description,
            company_owner_id = user_id,
            hide_status = False
        ).returning(Company)
        result = await self.db.fetch_one(query=query)
        return result
    
    
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
            raise HTTPException(status_code=404, detail="Company doesn't exist or You have no rights")
        company_dict = company.dict(exclude_unset=True)
        query = (
            update(Company)
            .where(Company.company_id == company_id)
            .values(**company_dict)
            .returning(Company)
        )
        result = await self.db.fetch_one(query=query)
        return result
    
    
    async def delete_company(self, company_id: int, current_user_id: int) -> None:
        db_company=await self.get_company(company_id=company_id, current_user_id=current_user_id)
        if db_company.company_owner_id != current_user_id:
            raise HTTPException(status_code=403, detail="You have no rights")
        query = delete(Company).where(Company.company_id == company_id)
        result = await self.db.execute(query=query)
        return result

async def get_company_service(db: Database = Depends(get_db)) -> CompanyService:
    return CompanyService(db)