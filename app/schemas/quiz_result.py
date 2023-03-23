from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Union, Dict
from app.schemas.question import QuestionCreate, QuestionBase



class QuizResultAnswer(BaseModel):
    id: int
    correct_answer: int

    
class QuizSubmit(BaseModel):
    answers: List[QuizResultAnswer]
    
