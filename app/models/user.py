from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from typing import Optional
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    password: str = Column(String, nullable=False)
    first_name: Optional[str] = Column(String, nullable=True)
    last_name: Optional[str] = Column(String, nullable=True)
    status: Optional[bool] = Column(Boolean, default=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    description: Optional[str] = Column(String, nullable=True)