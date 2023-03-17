from app.db.base_class import Base
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.utils. constants import CompanyRole


class Members(Base):
    __tablename__ = 'members'

    company_id: int = Column(Integer, ForeignKey('companies.company_id'), primary_key=True)
    user_id: int = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role: CompanyRole = Column(Text, default = CompanyRole.MEMBER.value, index=True)
    
    company = relationship("Company", back_populates="members")
    user = relationship("User", back_populates="members")