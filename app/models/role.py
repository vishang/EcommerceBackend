from sqlalchemy import Integer, String, Column
from app.core.database import Base

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)