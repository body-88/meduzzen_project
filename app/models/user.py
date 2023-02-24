from db.base_class import Base
from sqlalchemy import Column, Integer, String
from typing import Optional

class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, unique=True, index=True)
    password: str = Column(String)
    full_name: Optional[str] = Column(String)