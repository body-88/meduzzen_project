from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.quiz import Quiz


class Company(Base):
    __tablename__ = "companies"
    
    company_id: int = Column(Integer, primary_key=True, index=True)
    company_name: str = Column(String, unique=True)
    company_description: str = Column(String)
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_at: datetime = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    company_owner_id: int = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="companies")
    hide_status: bool = Column(Boolean, default=False, server_default="false", nullable=False)
    
    invitations_received = relationship("Invitation", back_populates="to_company")
    requests_received = relationship("Request", back_populates="to_company")
    members = relationship("Members", back_populates="company")
    quizzes = relationship("Quiz", back_populates="company")