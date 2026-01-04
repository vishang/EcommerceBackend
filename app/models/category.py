from sqlalchemy import Integer, String, Float, Column
from app.core.database import Base

class Category(Base):
    
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    