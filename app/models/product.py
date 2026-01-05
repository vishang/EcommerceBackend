from sqlalchemy import Column, String, Float, Text, Integer
from app.core.database import Base

class Product(Base):
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    
    height = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    length = Column(Float, nullable=False)