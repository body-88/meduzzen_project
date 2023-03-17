from databases import Database
from app.schemas.request import RequestBase, RequestCreate
from sqlalchemy import delete, select, insert
from app.db.db_settings import get_db
from fastapi import Depends, HTTPException
from app.servises.company import CompanyService
from app.models.company import Company
from app.models.members import Members
from app.models.request_membership import Request
from app.schemas.user import Result
from app.utils.constants import CompanyRole


class RequestService:
    def __init__(self, db: Database):
        self.db = db
        
        
    async def create_request(self, request: RequestCreate,
                                current_user_id: int,
                                company_service: CompanyService,
                                ) -> RequestBase:
        db_company = await company_service.get_company_by_id(company_id=request.to_company_id)
        query = select(Members).where(
            (Members.company_id == request.to_company_id) & 
            (Members.user_id == current_user_id)
            )
        existing_request = await self.db.fetch_one(query=query)
        if existing_request:
            raise HTTPException(status_code=400, detail="User is already a member of the company")
        
        query = select(Request).where(
            (Request.to_company_id == request.to_company_id) & 
            (Request.from_user_id == current_user_id)
            )
        existing_request = await self.db.fetch_one(query=query)
        if existing_request:
            raise HTTPException(status_code=400, detail="Request already sent")

        query = insert(Request).values(
                                        to_company_id = request.to_company_id,
                                        from_user_id = current_user_id,
                                        request_message = request.request_message,
                                        ).returning(Request)
        db_request = await self.db.fetch_one(query=query)
        return db_request
        
    
    async def get_requests_by_user(self, current_user_id: int) -> Request:
        query = select(Request).where(Request.from_user_id == current_user_id)
        result = await self.db.fetch_all(query=query)
        return result
    
    
    async def get_requests_by_company(self, company_id: int,
                                        current_user_id: int,
                                        company_service: CompanyService) -> Request:
        query = (
        select(Request, Company.company_owner_id)
        .join(Company, Request.to_company_id == Company.company_id)
        .where((Request.to_company_id == company_id) & (Company.company_owner_id == current_user_id)
        )
    )
        company = await company_service.get_company_by_user(company_id=company_id,
                                                    current_user_id=current_user_id)
        result = await self.db.fetch_all(query=query)
        if not result:
            raise HTTPException(status_code=404, detail="No requests found for this company.")
        return result
        
    
    async def get_request_by_id(self, request_id: int) -> Request:
        query = select(Request).where(Request.id == request_id)
        db_request = await self.db.fetch_one(query=query)
        if db_request is None:
            raise HTTPException(status_code=404, detail="Request not found")
        return db_request
        
        
    async def cancel_request(self, request_id: int, current_user_id: int) -> Result:
        db_request = await self.get_request_by_id(request_id=request_id)
        if db_request.from_user_id != current_user_id:
            raise HTTPException(status_code=403, detail="It's not your request")
        delete_query = delete(Request).where(Request.id == request_id)
        result = await self.db.execute(delete_query)
        return result

    
    async def accept_request(self, current_user_id: int, request_id: int, company_service: CompanyService) -> Result:
        db_request = await self.get_request_by_id(request_id=request_id)
        db_company = await company_service.get_company_by_id(company_id=db_request.to_company_id)
        if not current_user_id == db_company.company_owner_id:
            raise HTTPException(status_code=403, detail="Only the owner of the company can accept requests")
        query = insert(Members).values(
                                        user_id = db_request.from_user_id,
                                        company_id = db_request.to_company_id,
                                        role = CompanyRole.MEMBER.value
                                        ).returning(Members)
        result = await self.db.fetch_one(query=query)
        delete_query = delete(Request).where(Request.id == request_id)
        await self.db.execute(query=delete_query)
        return result
    
    
    async def decline_request(self, current_user_id: int, request_id: int, company_service: CompanyService) -> Result:
        db_request = await self.get_request_by_id(request_id=request_id)
        db_company = await company_service.get_company_by_id(company_id=db_request.to_company_id)
        if not current_user_id == db_company.company_owner_id:
            raise HTTPException(status_code=403, detail="Only the owner of the company can decline requests")
        query = delete(Request).where(Request.id == request_id)
        result = await self.db.execute(query=query)
        return result        
        
        
async def get_request_service(db: Database = Depends(get_db)) -> RequestService:
    return RequestService(db)