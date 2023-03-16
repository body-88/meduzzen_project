from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import List

class InvitationBase(BaseModel):

    id: int
    to_user_id: int
    from_company_id: int
    invite_message: Optional[str]
    created_at: datetime
    updated_at: datetime


class InvitationCreate(BaseModel):
    invite_message: Optional[str]
    to_user_id: int
    from_company_id: int


class InvitationsListResponse(BaseModel):
    invites: List[InvitationBase]