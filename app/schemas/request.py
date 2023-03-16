from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import List

class RequestBase(BaseModel):

    id: int
    from_user_id: int
    to_company_id: int
    request_message: Optional[str]
    created_at: datetime
    updated_at: datetime


class RequestCreate(BaseModel):
    request_message: Optional[str]
    to_company_id: int


class RequestListResponse(BaseModel):
    invites: List[RequestBase]