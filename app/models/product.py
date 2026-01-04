from sqlalchemy import Column, String, Float, Text, Integer
from app.core.database import Base

class Product(Base):
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text(100), nullable=False)
    
    height = Column(Float(1000), nullable=False)
    width = Column(Float(1000), nullable=False)
    length = Column(Float(1000), nullable=False)