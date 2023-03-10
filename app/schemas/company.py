from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime

class CompanyBase(BaseModel):
    company_id: int 
    company_name: str 
    company_description: Optional[str] 
    created_at: datetime
    updated_at: datetime
    company_owner_id: int
    hide_status: bool
    
    
class CompanyCreate(BaseModel):
    company_name: str 
    company_description: Optional[str] 
    
    @validator('company_name')
    def company_name_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Company name cannot be empty')
        return v
    

class CompanyUpdate(CompanyCreate):
    hide_status: Optional[bool] 
