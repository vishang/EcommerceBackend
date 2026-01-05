from sqlalchemy import Column, Integer, ForeignKey
from app.core.database import Base

class CategoryProduct(Base):
    
    __tablename__ = "category_products"
    
    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)