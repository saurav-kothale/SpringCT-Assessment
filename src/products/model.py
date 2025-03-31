from database import Base
from sqlalchemy import Column, String, Integer, Float, DateTime, func, Boolean

class ProductModel(Base):
    __tablename__ = "products"
    id = Column(String(100),primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    price = Column(Float, nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)