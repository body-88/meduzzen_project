from typing import List, Optional,  TypeVar, Generic
from pydantic import BaseModel, validator, Field
from datetime import datetime
from fastapi import HTTPException
from pydantic.generics import GenericModel

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
    hide_status: bool
