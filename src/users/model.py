from database import Base
from sqlalchemy import Column, String, DateTime, func, Boolean

class UserModel(Base):
    __tablename__ = "user"
    id = Column(String(50), primary_key=True, nullable=False)
    name = Column(String(20), nullable=False)
    email = Column(String(50), nullable= False)
    password = Column(String(50), nullable= False)
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

