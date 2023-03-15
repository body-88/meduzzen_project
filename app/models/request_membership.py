from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import Optional


class Request(Base):
    __tablename__ = "requests"
    
    id: int = Column(Integer, primary_key=True, index=True)
    from_user_id: int = Column(Integer, ForeignKey("users.id"))
    to_company_id: int = Column(Integer, ForeignKey("companies.company_id"))
    request_message: Optional[str] = Column(String, nullable=True)
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: datetime = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    to_company = relationship("Company", back_populates="requests_received")
    from_user = relationship("User", back_populates="requests_sent")