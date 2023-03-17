from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.utils.constants import CompanyRole

class MemberBase(BaseModel):
    company_id: int 
    user_id: int
    role: CompanyRole
    
    
class MakeAdmin(BaseModel):
    user_id: int