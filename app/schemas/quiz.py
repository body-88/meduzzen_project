from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Union
from app.schemas.question import QuestionCreate, QuestionBase


class QuizBase(BaseModel):
    id: int 
    company_id: int 
    name: str 
    description: Optional[str] 
    frequency: str 
    created_at: datetime
    updated_at: datetime
    questions: Union[QuestionBase, None] = None

    class Config:
        orm_mode = True


class QuizUpdate(BaseModel):
    name: str 
    description: Optional[str] 
    frequency: str 
    
    
class QuizCreate(BaseModel):
    company_id: int 
    name: str 
    description: Optional[str] 
    frequency: str
    questions: List[QuestionCreate]
