from database import Base
from sqlalchemy import Column, String, Integer, Float, DateTime, func, Boolean, ForeignKey

class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(String(100),primary_key=True)
    product_id = Column(String(50), ForeignKey('products.id'), nullable=False)
    user_id = Column(String(50),ForeignKey("user.id"), nullable=False)
    quantity_ordered = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)