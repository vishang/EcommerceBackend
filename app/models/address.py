from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Address(Base):
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True)
    line1 = Column(String(255), nullable=False) #House/Building
    line2 = Column(String(255)) #Optional
    suburb = Column(String(100)) #Sector/Area
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    pincode = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    
    stores = relationship("Store", back_populates="address")