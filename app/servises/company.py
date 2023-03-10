from databases import Database
from app.models.company import Company
from app.schemas.company import CompanyBase, CompanyCreate
from sqlalchemy import update, delete, select, insert
from app.db.db_settings import get_db
from fastapi import Depends, HTTPException
from typing import List, Optional
from app.utils.hass_pass import get_hashed_password



class CompanyService:
    def __init__(self, db: Database):
        self.db = db
        
        
    async def create_company(self, company: CompanyCreate, user_id: int):
        query = insert(Company).values(
            company_name = company.company_name,
            company_description = company.company_description,
            company_owner_id = user_id,
            hide_status = False
        ).returning(Company)
        result = await self.db.fetch_one(query=query)
        return result
    
    
    async def get_companies(self, skip: int = 0, limit: int = 100):
        query = select(Company).offset(skip).limit(limit)
        result = await self.db.fetch_all(query=query)
        return result
    
    
    async def get_company(self, company_id: int) -> CompanyBase:
        query = select(Company).where(Company.company_id == company_id)
        company = await self.db.fetch_one(query=query)
        if company is None:
            raise HTTPException(status_code=404, detail="Company doesn't exist")
        return company
    
    
    async def update_company(self, company_id: int, company: CompanyCreate, current_user_id: int) -> CompanyBase:
        db_company = await self.get_company(company_id=company_id)
        if db_company is None:
            raise HTTPException(status_code=404, detail="Company doesn't exist")
        if db_company.company_owner_id != current_user_id:
            raise HTTPException(status_code=404, detail="This is not your company")
        query = (
            update(Company)
            .where(Company.company_id == company_id)
            .values(Company.company_description, Company.company_name, Company.hide_status)
            .returning(Company)
        )
        result = await self.db.fetch_one(query=query)
        return result
    
    
    async def delete_company(self, company_id: int, current_user_id: int) -> None:
        db_company=await self.get_company(company_id=company_id)
        if db_company.company_owner_id != current_user_id:
            raise HTTPException(status_code=404, detail="This is not your company")
            
        query = delete(Company).where(Company.company_id == company_id)
        result = await self.db.execute(query=query)
        return result

async def get_company_service(db: Database = Depends(get_db)) -> CompanyService:
    return CompanyService(db)