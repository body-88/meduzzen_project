from pydantic import BaseModel
from typing import  List
    
    
    
class QuestionBase(BaseModel):
    id: int
    quiz_id: int
    question: str
    answer_variants: List[str]
    correct_answer: int
        
    class Config:
        orm_mode = True


class QuestionCreate(BaseModel):
    question: str
    correct_answer: int
    answer_variants: List[str]
    

    
class QuestionUpdate(QuestionCreate):
    pass